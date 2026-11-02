
import pandas as pd

from analisis.clustering import clustering_jerarquico


# CREAR DATASET DE PRUEBA
datos = {
    "ventas": [
        100, 110, 120,
        500, 520, 510,
        1000, 1050, 1100
    ],
    "visitas": [
        10, 12, 11,
        50, 52, 49,
        100, 105, 110
    ],
    "categoria": [
        "A", "A", "A",
        "B", "B", "B",
        "C", "C", "C"
    ]
}

df = pd.DataFrame(datos)

print("\nDATOS ORIGINALES:")
print(df)


# APLICAR CLUSTERING
resultados = clustering_jerarquico(
    df,
    columnas=["ventas", "visitas"],
    n_clusters=3,
    metodo="ward"
)


# MOSTRAR RESULTADOS
print("\nRESULTADOS DEL CLUSTERING:")

print("Columnas:", resultados["columnas_utilizadas"])
print("Observaciones agrupadas:", resultados["observaciones_agrupadas"])
print("Cantidad de grupos:", resultados["cantidad_clusters"])
print("Distribución:", resultados["distribucion_clusters"])

print("\nDATAFRAME CON GRUPOS:")
print(resultados["dataframe"])
