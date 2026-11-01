#CODIGO PARA UNIR LA DATA
from pathlib import Path
import pandas as pd

RAW = Path("data_raw")
OUT = Path("data")
OUT.mkdir(exist_ok=True)

F_MORT = RAW / "Anexo1_NoFetal2019_CE_15-03-23.xlsx"
F_COD = RAW / "Anexo2_CodigosDeMuerte_CE_15-03-23.xlsx"
F_DIV = RAW / "Divipola_CE_.xlsx"

# Mortalidad no fetal 2019
mort = pd.read_excel(F_MORT, sheet_name="No_Fetales_2019",
                     dtype={"COD_DANE": str, "COD_DEPARTAMENTO": str, "COD_MUNICIPIO": str})
mort = mort[["COD_DANE", "COD_DEPARTAMENTO", "MES", "SEXO", "GRUPO_EDAD1",
             "MANERA_MUERTE", "COD_MUERTE"]].copy()
mort["COD_MUERTE"] = mort["COD_MUERTE"].astype(str).str.strip().str.upper()

# Divipola 
div = pd.read_excel(F_DIV, sheet_name="Hoja3", header=None, skiprows=2, dtype=str)
div = div.iloc[:, :4]
div.columns = ["COD_DEPTO", "DEPARTAMENTO", "COD_DANE", "MUNICIPIO"]
nombres_depto = div.drop_duplicates("COD_DEPTO").set_index("COD_DEPTO")["DEPARTAMENTO"]

df = mort.merge(div[["COD_DANE", "MUNICIPIO"]], on="COD_DANE", how="left")
df["COD_DEPTO"] = df["COD_DANE"].str[:2]
df["DEPARTAMENTO"] = df["COD_DEPTO"].map(nombres_depto)
df["MUNICIPIO"] = df["MUNICIPIO"].fillna("SIN INFORMACIÓN")

# Nombres de causas
cod = pd.read_excel(F_COD, header=8, dtype=str)
cod.columns = ["CAP", "NOM_CAP", "C3", "D3", "C4", "D4"]
for c in ("C3", "C4"):
    cod[c] = cod[c].str.strip().str.upper()
n4 = cod.drop_duplicates("C4").set_index("C4")["D4"]
n3 = cod.drop_duplicates("C3").set_index("C3")["D3"]
df["CAUSA"] = df["COD_MUERTE"].map(n4).fillna(df["COD_MUERTE"].map(n3))

# Variables derivadas
df["SEXO"] = df["SEXO"].map({1: "Hombre", 2: "Mujer", 3: "Indeterminado"}).fillna("Indeterminado")

bins = [-1, 4, 6, 8, 10, 11, 13, 16, 19, 24, 28, 29]
labels = ["Mortalidad neonatal", "Mortalidad infantil", "Primera infancia", "Niñez",
          "Adolescencia", "Juventud", "Adultez temprana", "Adultez intermedia",
          "Vejez", "Longevidad / Centenarios", "Edad desconocida"]
df["CATEGORIA_EDAD"] = pd.cut(df["GRUPO_EDAD1"], bins=bins, labels=labels).astype(str)

df = df[["COD_DEPTO", "DEPARTAMENTO", "MUNICIPIO", "MES", "SEXO", "GRUPO_EDAD1",
         "CATEGORIA_EDAD", "MANERA_MUERTE", "COD_MUERTE", "CAUSA"]]
df.to_csv(OUT / "mortalidad_2019.csv.gz", index=False, compression="gzip")

print(f"Listo: {len(df):,} registros -> data/mortalidad_2019.csv.gz")
print("Registros sin departamento:", df["DEPARTAMENTO"].isna().sum())
print("Registros sin nombre de causa:", df["CAUSA"].isna().sum())
print("Registros sin edad clasificada:", (df["CATEGORIA_EDAD"] == "nan").sum())
