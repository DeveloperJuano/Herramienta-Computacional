
from analisis.carga_datos import cargar_csv
from analisis.limpieza import (
    eliminar_filas_nulas,
    rellenar_nulos_mediana,
    rellenar_nulos_media,
    rellenar_nulos_moda,
    eliminar_duplicados,
    comparar_datos
)

df = cargar_csv("datos/originales/panel_ciudades_2012_2025 .csv")

df_sin_nulos = eliminar_filas_nulas(df)
df_mediana = rellenar_nulos_mediana(df)
df_media = rellenar_nulos_media(df)
df_moda = rellenar_nulos_moda(df)
df_sin_duplicados = eliminar_duplicados(df)
resumen = comparar_datos(df, df_mediana)

print("\n=== COMPARACIÓN DE DATOS ===")
for indicador, valor in resumen.items():
    print(f"{indicador}: {valor}")

print("\n=== ELIMINAR DUPLICADOS ===")
print("Filas originales:", len(df))
print("Filas después:", len(df_sin_duplicados))
print("Duplicados eliminados:", len(df) - len(df_sin_duplicados))

print("=== ELIMINAR FILAS ===")
print("Filas:", len(df_sin_nulos))
print("Nulos:", int(df_sin_nulos.isna().sum().sum()))

print("\n=== MEDIANA ===")
print("Filas:", len(df_mediana))
print("Nulos:", int(df_mediana.isna().sum().sum()))

print("\n=== MEDIA ===")
print("Filas:", len(df_media))
print("Nulos:", int(df_media.isna().sum().sum()))

print("\n=== MODA ===")
print("Filas:", len(df_moda))
print("Nulos:", int(df_moda.isna().sum().sum()))

print("\n=== DATASET ORIGINAL ===")
print("Filas:", len(df))
print("Nulos:", int(df.isna().sum().sum()))
