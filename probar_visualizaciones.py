
from analisis.carga_datos import cargar_csv
from analisis.visualizaciones import *
from analisis.regresion import regresion_lineal
# CARGAR LOS DATOS
df = cargar_csv(
    "datos/originales/panel_ciudades_2012_2025 .csv"
)

# CREAR EL HISTOGRAMA
# crear_histograma(df, "ingreso_pc_pesos")


# crear_grafico_barras(df,"unidad","incidencia_pobreza_pct")

# crear_grafico_dispersion(df,"ingreso_pc_pesos","incidencia_pobreza_pct" )

# crear_boxplot(df, "ingreso_pc_pesos")

# crear_mapa_calor(df)

resultados = regresion_lineal(df,"ingreso_pc_pesos","incidencia_pobreza_pct")

print("\nRESULTADOS DE REGRESION")
for clave, valor in resultados.items():
    print(f"{clave}: {valor}")



