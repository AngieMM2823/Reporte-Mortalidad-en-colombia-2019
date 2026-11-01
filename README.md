# Mortalidad en Colombia – 2019

Aplicación web dinámica en **Python (Dash + Plotly)** para explorar las defunciones no fetales registradas en Colombia durante 2019, con base en las Estadísticas Vitales del DANE.

- **Integrantes:** <<NOMBRE COMPLETO 1>>, <<NOMBRE COMPLETO 2>>, <<NOMBRE COMPLETO 3>>, <<NOMBRE COMPLETO 4>>
- **Aplicación desplegada:** <<https://tu-app.onrender.com>>
- **Repositorio:** <<https://github.com/TU_USUARIO/TU_REPOSITORIO>>

---

## Introducción

Este proyecto presenta un tablero interactivo (dashboard) que integra siete visualizaciones sobre la mortalidad en Colombia en 2019: un mapa por departamento, la evolución mensual, las ciudades con más homicidios, las ciudades con menor mortalidad, las principales causas de muerte, la comparación por sexo y la distribución por grupos de edad. Los datos proceden de tres archivos del DANE (mortalidad no fetal, códigos de causas de muerte CIE-10 y división político-administrativa, Divipola), que se limpian y unen en un único archivo liviano para que la aplicación cargue rápido.

## Objetivo

Facilitar la identificación de patrones **demográficos** (sexo y edad) y **regionales** (departamentos y ciudades) de la mortalidad en Colombia en 2019, mediante informes gráficos interactivos que permitan una exploración visual intuitiva. La aplicación incluye un filtro por departamento que actualiza el gráfico de líneas, el histograma de edades y la tabla de causas.

## Estructura del proyecto

```
.
├── app.py                      # Aplicación Dash (layout, gráficos y callbacks)
├── prepare_data.py             # Une los 3 Excel del DANE y genera el CSV de trabajo
├── requirements.txt            # Librerías y versiones
├── .gitignore                  # Excluye venv/, data_raw/ y archivos temporales
├── README.md                   # Este documento
├── data/
│   ├── mortalidad_2019.csv.gz  # Datos procesados (244.355 registros)
│   └── colombia.geo.json       # Polígonos de los 33 departamentos (para el mapa)
└── images/                     # Capturas de pantalla usadas en este README
```

Los Excel originales (`data_raw/`) no se incluyen en el repositorio por su tamaño; pueden descargarse de la página del DANE (Estadísticas Vitales – EEVV 2019).

## Requisitos

| Librería | Versión |
|---|---|
| Python | 3.10 o superior |
| dash | 2.18.2 |
| plotly | 5.24.1 |
| pandas | 2.2.3 |
| openpyxl | 3.1.5 |
| gunicorn | 23.0.0 |

## Software

- **Python**: lenguaje de programación.
- **Dash**: framework para la aplicación web.
- **Plotly Express**: gráficos interactivos.
- **pandas / openpyxl**: lectura y transformación de datos.
- **Visual Studio Code**: editor de código.
- **Git y GitHub**: control de versiones y repositorio.
- **Render**: plataforma como servicio (PaaS) para el despliegue.
- **gunicorn**: servidor web para producción.

## Instalación

Para clonar el repositorio y ejecutar la aplicación localmente:

```bash
# 1. Clonar el repositorio
git clone <<https://github.com/TU_USUARIO/TU_REPOSITORIO.git>>
cd <<TU_REPOSITORIO>>

# 2. Crear y activar un entorno virtual
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac / Linux

# 3. Instalar las dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python app.py
```

Luego abrir http://127.0.0.1:8050 en el navegador.

**(Opcional) Regenerar los datos desde los Excel originales:** crear la carpeta `data_raw/`, copiar allí los tres archivos del DANE (`Anexo1_NoFetal2019_CE_15-03-23.xlsx`, `Anexo2_CodigosDeMuerte_CE_15-03-23.xlsx` y `Divipola_CE_.xlsx`) y ejecutar `python prepare_data.py`.

## Despliegue (Render)

1. Subir el proyecto a un repositorio público de GitHub (`git init`, `git add .`, `git commit`, `git remote add origin ...`, `git push -u origin main`).
2. Crear una cuenta en [render.com](https://render.com) e iniciar sesión con GitHub.
3. Seleccionar **New + → Web Service** y elegir el repositorio.
4. Configurar el servicio:
   - **Language:** Python 3
   - **Branch:** main
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:server`
   - **Instance Type:** Free
   - **Environment Variable:** `PYTHON_VERSION` = `3.11.9`
5. Pulsar **Create Web Service** y esperar a que el estado sea **Live**. Render entrega la URL pública de la aplicación.

> Nota: en el plan gratuito de Render la aplicación se suspende tras un periodo sin visitas, por lo que la primera carga puede tardar cerca de un minuto.

## Visualizaciones con explicaciones de los resultados

En 2019 se registraron **244.355 defunciones no fetales** en Colombia. Los porcentajes y cifras de abajo se calcularon con los datos de la aplicación.

### 1. Mapa: muertes por departamento

![Mapa de muertes por departamento](images/01_mapa.png)

Mapa coroplético donde el tono de rojo indica el total de muertes de cada departamento; al pasar el cursor se muestra el nombre y la cifra exacta. Tres territorios concentran cerca del 42 % de las muertes: **Bogotá D.C. (38.760, 15,9 %)**, **Antioquia (34.473, 14,1 %)** y **Valle del Cauca (28.443, 11,6 %)**. Les siguen Atlántico (14.804) y Santander (11.894). En el extremo opuesto están Vaupés (87), Guainía (115), Vichada (188) y Amazonas (190). Estas cifras son absolutas, así que reflejan en gran parte el tamaño de la población y no necesariamente un mayor riesgo de morir.

### 2. Gráfico de líneas: muertes por mes

![Muertes por mes](images/02_lineas.png)

Muestra la evolución mensual (y cambia al elegir un departamento en el filtro). A nivel nacional el comportamiento es bastante estable, con un promedio de unas 20.400 muertes al mes. Los meses con más muertes son **diciembre (21.678)**, **julio (21.372)** y **enero (21.354)**, y el más bajo es **febrero (17.974)**, algo explicable en parte porque tiene menos días.

### 3. Gráfico de barras: 5 ciudades con más homicidios (X95)

![Ciudades con más homicidios](images/03_barras_homicidios.png)

Cuenta las muertes por agresión con disparo de arma de fuego (códigos X95, incluidos los no especificados). Las cinco ciudades con más casos son **Cali (971)**, **Bogotá (601)**, **Medellín (428)**, **Barranquilla (260)** y **Cúcuta (206)**. En total el país registró 9.273 muertes con este código. Como son cifras absolutas, las ciudades más grandes aparecen primero; para comparar el nivel de violencia entre ciudades habría que calcular tasas por cada 100.000 habitantes.

### 4. Gráfico circular: 10 ciudades con menor mortalidad

![Ciudades con menor mortalidad](images/04_circular.png)

Se muestran los 10 municipios con menos defunciones registradas (al menos una). Como al menos 12 municipios tienen una sola muerte, existen empates y todas las porciones resultan iguales; para tener un resultado reproducible se desempató por orden alfabético. Se trata en su mayoría de municipios pequeños y apartados (por ejemplo Alto Baudó, Nuquí o Taraira), por lo que este gráfico refleja poca población o posible subregistro, y no un bajo riesgo de mortalidad.

### 5. Tabla: 10 principales causas de muerte

![Tabla de causas](images/05_tabla.png)

La tabla muestra código, nombre y total de casos, de mayor a menor. La causa principal es el **infarto agudo del miocardio (I219) con 35.088 casos**, cerca del 14 % de todas las muertes. Le siguen la enfermedad pulmonar obstructiva crónica no especificada (J449, 7.210), la EPOC con infección aguda de las vías respiratorias inferiores (J440, 6.445), la neumonía (J189, 5.798), el tumor maligno de estómago (C169, 5.125) y el de bronquios o pulmón (C349, 4.438). En el séptimo lugar aparece una causa externa, la **agresión con disparo de armas de fuego (X954, 4.396)**. Completan el listado el tumor de mama (C509), el de próstata (C61) y la hipertensión esencial (I10). Predominan las enfermedades del sistema circulatorio, las respiratorias y los tumores.

### 6. Barras apiladas: muertes por sexo en cada departamento

![Muertes por sexo y departamento](images/06_barras_sexo.png)

Cada barra es un departamento, dividido en hombres y mujeres. A nivel nacional el **55,1 % de las muertes corresponden a hombres (134.573)** y el 44,9 % a mujeres (109.689), además de 93 casos con sexo indeterminado. Las diferencias son pequeñas en las zonas urbanas más grandes (Bogotá 51,8 % hombres, Atlántico 52,5 %) y mucho mayores en departamentos de baja población como Guaviare (77,1 %) y Guainía (67,8 %), donde el número de casos es reducido y pesan más las muertes violentas y accidentales.

### 7. Histograma: distribución de muertes por grupo de edad

![Histograma por grupo de edad](images/07_histograma.png)

Agrupa la variable `GRUPO_EDAD1` en las categorías del DANE y cambia al seleccionar un departamento. La mortalidad se concentra al final de la vida: **Vejez (60 a 84 años) reúne 115.453 muertes (47,2 %)** y **Longevidad (85 años o más) 56.061 (22,9 %)**, es decir, cerca del 70 % de las defunciones ocurre desde los 60 años. Le siguen Adultez intermedia (29.105) y Adultez temprana (17.276). En las edades tempranas, la mortalidad neonatal (4.520) supera a la infantil (2.771) y a la de la primera infancia (1.518), lo que indica que el mayor riesgo del primer año de vida se concentra en el primer mes. También se nota un aumento en Juventud (11.840) frente a Niñez (1.993), asociado en buena parte a muertes violentas y accidentes.

## Conclusiones

- La mortalidad en Colombia en 2019 se concentra geográficamente en Bogotá, Antioquia y Valle del Cauca, y demográficamente en la población de 60 años o más.
- Las enfermedades del corazón (en especial el infarto) son la primera causa de muerte, seguidas de enfermedades respiratorias y tumores.
- Los hombres tienen mayor participación en las muertes (55 %), y la brecha es más marcada en departamentos de baja población.
- Las muertes por arma de fuego se concentran en las grandes ciudades, con Cali a la cabeza.
- Las cifras son absolutas (no tasas), por lo que las comparaciones entre territorios deben interpretarse considerando su población.

## Fuentes

- DANE – Estadísticas Vitales (EEVV) 2019: defunciones no fetales, códigos de causas de muerte (CIE-10) y Divipola.
- Polígonos departamentales (GeoJSON): repositorio `caticoa3/colombia_mapa` (GitHub), basado en el Marco Geoestadístico Nacional del DANE.
