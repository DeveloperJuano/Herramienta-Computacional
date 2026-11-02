
import pandas as pd

from analisis.interpolacion import *


# DATASET DE PRUEBA
datos = {
    "producto": ["A", "A", "A", "B", "B", "B"],
    "anio": [2021, 2022, 2023, 2021, 2022, 2023],
    "ventas": [100, None, 300, 200, None, 400]
}

df = pd.DataFrame(datos)

print("\nDATOS ORIGINALES:")
print(df)


# APLICAR INTERPOLACION
df_resultado = interpolacion_lineal(
    df,
    columna="ventas",
    columna_orden="anio",
    columnas_grupo=["producto"]
)
comparacion = comparar_interpolacion(
    df,
    df_resultado,
    "ventas"
)

print("\nINFORME DE INTERPOLACION:")

for clave, valor in comparacion.items():
    print(f"{clave}: {valor}")

print("\nDATOS INTERPOLADOS:")
print(df_resultado)


# COMPARAR NULOS
print("\nCOMPARACION:")
print("Nulos originales:", df["ventas"].isna().sum())
print("Nulos finales:", df_resultado["ventas"].isna().sum())
