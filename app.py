import json
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table, Input, Output

# Dataframe de data consolidada
df = pd.read_csv("data/mortalidad_2019.csv.gz", dtype={"COD_DEPTO": str})
df["DEPARTAMENTO"] = df["DEPARTAMENTO"].fillna("SIN INFORMACIÓN")
df["CIUDAD"] = df["MUNICIPIO"].fillna("SIN INFORMACIÓN") + " (" + df["DEPARTAMENTO"] + ")"

with open("data/colombia.geo.json", encoding="utf-8") as f:
    geojson = json.load(f)

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
         "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
ORDEN_EDAD = ["Mortalidad neonatal", "Mortalidad infantil", "Primera infancia", "Niñez",
              "Adolescencia", "Juventud", "Adultez temprana", "Adultez intermedia",
              "Vejez", "Longevidad / Centenarios", "Edad desconocida"]

# Gráfico estáticos 
# Mapa
por_depto = (df.groupby(["COD_DEPTO", "DEPARTAMENTO"]).size()
               .reset_index(name="Muertes"))
fig_mapa = px.choropleth_map(
    por_depto, geojson=geojson, locations="COD_DEPTO",
    featureidkey="properties.DPTO_CCDGO", color="Muertes",
    hover_name="DEPARTAMENTO", color_continuous_scale="Reds",
    map_style="carto-positron", zoom=4.3, center={"lat": 4.6, "lon": -74.1},
    opacity=0.8, title="Total de muertes por departamento (2019)")
fig_mapa.update_layout(margin=dict(l=0, r=0, t=40, b=0))

# 5 ciudades más violentas (homicidios con arma de fuego, Codigo: X95)
CODIGOS_HOMICIDIO = ("X95",)
homicidios = (df[df["COD_MUERTE"].str.startswith(CODIGOS_HOMICIDIO)]
              .groupby("CIUDAD").size().nlargest(5)
              .reset_index(name="Homicidios"))
fig_violentas = px.bar(homicidios, x="CIUDAD", y="Homicidios", text="Homicidios",
                       title="5 ciudades con más homicidios (X95)",
                       color="Homicidios", color_continuous_scale="Reds")
fig_violentas.update_layout(xaxis_title="", coloraxis_showscale=False)

# Diagrama de torta: ciudades con menor mortalidad (con al menos 1 muerte, se desempata por nombre)
menores = (df.groupby("CIUDAD").size().reset_index(name="Muertes")
             .sort_values(["Muertes", "CIUDAD"]).head(10))
fig_menores = px.pie(menores, names="CIUDAD", values="Muertes",
                     title="10 ciudades con menor mortalidad (2019)")

# Barras apiladas: muertes por sexo
sexo_depto = df.groupby(["DEPARTAMENTO", "SEXO"]).size().reset_index(name="Muertes")
fig_sexo = px.bar(sexo_depto, x="DEPARTAMENTO", y="Muertes", color="SEXO",
                  barmode="stack", title="Muertes por sexo y departamento",
                  color_discrete_map={"Hombre": "#1f77b4", "Mujer": "#e377c2",
                                      "Indeterminado": "#7f7f7f"})
fig_sexo.update_layout(xaxis_title="", xaxis_tickangle=-60)

# Organización de la pagina Web
app = Dash(__name__)
server = app.server  

CARD = {"background": "white", "borderRadius": "10px", "padding": "10px",
        "boxShadow": "0 1px 4px rgba(0,0,0,.15)", "margin": "8px"}

deptos = ["TODOS"] + sorted(df["DEPARTAMENTO"].unique())

app.layout = html.Div(style={"fontFamily": "Arial", "background": "#f2f4f7",
                             "padding": "10px"}, children=[
    html.H1("Reporte de Mortalidad en Colombia – 2019", style={"textAlign": "center"}),
    html.P("Fuente: DANE – Estadísticas Vitales (defunciones no fetales).",
           style={"textAlign": "center"}),
    html.Div([
            html.P("Presentado por: Angie Vanesa Medina Montero"),
            html.P("Materia: Aplicaciones 1"),
            html.P("Universidad: La Salle")
        ], style={
            "textAlign": "right",
            "marginTop": "30px"
    }),

    html.Div(style=CARD, children=[
        html.Label("Filtrar por departamento (afecta línea, tabla e histograma):"),
        dcc.Dropdown(id="dd-depto", options=deptos, value="TODOS", clearable=False),
    ]),

    html.Div(style=CARD, children=[dcc.Graph(figure=fig_mapa)]),

    html.Div(style={"display": "flex", "flexWrap": "wrap"}, children=[
        html.Div(style={**CARD, "flex": "1 1 480px"},
                 children=[dcc.Graph(id="g-lineas")]),
        html.Div(style={**CARD, "flex": "1 1 480px"},
                 children=[dcc.Graph(id="g-hist")]),
    ]),

    html.Div(style={"display": "flex", "flexWrap": "wrap"}, children=[
        html.Div(style={**CARD, "flex": "1 1 480px"},
                 children=[dcc.Graph(figure=fig_violentas)]),
        html.Div(style={**CARD, "flex": "1 1 480px"},
                 children=[dcc.Graph(figure=fig_menores)]),
    ]),

    html.Div(style=CARD, children=[
        html.H3("10 principales causas de muerte"),
        dash_table.DataTable(
            id="tabla",
            columns=[{"name": "Código", "id": "Código"},
                     {"name": "Causa", "id": "Causa"},
                     {"name": "Total de casos", "id": "Total"}],
            style_header={"fontWeight": "bold", "backgroundColor": "#e9ecef"},
            style_cell={"textAlign": "left", "padding": "6px",
                        "whiteSpace": "normal", "height": "auto"},
        ),
    ]),

    html.Div(style=CARD, children=[dcc.Graph(figure=fig_sexo)]),
])


# MAIN (llamadas)
@app.callback(
    Output("g-lineas", "figure"),
    Output("g-hist", "figure"),
    Output("tabla", "data"),
    Input("dd-depto", "value"),
)
def actualizar(depto):
    d = df if depto == "TODOS" else df[df["DEPARTAMENTO"] == depto]
    titulo = "Colombia" if depto == "TODOS" else depto.title()

    mensual = (d.groupby("MES").size().reindex(range(1, 13), fill_value=0)
                 .reset_index(name="Muertes"))
    mensual["Mes"] = MESES
    fig_lineas = px.line(mensual, x="Mes", y="Muertes", markers=True,
                         title=f"Muertes por mes – {titulo}")

    fig_hist = px.histogram(d, x="CATEGORIA_EDAD",
                            category_orders={"CATEGORIA_EDAD": ORDEN_EDAD},
                            title=f"Distribución de muertes por grupo de edad – {titulo}")
    fig_hist.update_layout(xaxis_title="", yaxis_title="Muertes", bargap=0.05,
                           xaxis_tickangle=-40)

    top = (d.groupby(["COD_MUERTE", "CAUSA"], dropna=False).size()
             .reset_index(name="Total")
             .sort_values("Total", ascending=False).head(10))
    top = top.rename(columns={"COD_MUERTE": "Código", "CAUSA": "Causa"})
    top["Causa"] = top["Causa"].fillna("Sin descripción")
    return fig_lineas, fig_hist, top.to_dict("records")


if __name__ == "__main__":
    app.run(debug=True)
