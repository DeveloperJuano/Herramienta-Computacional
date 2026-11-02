# ===========================================================
# IMPORTS
# ===========================================================

import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, dendrogram

# ===========================================================
# FUNCION: INTERPOLACION LINEAL
# ===========================================================
def clustering_jerarquico(
    df: pd.DataFrame,
    columnas: list,
    n_clusters: int = 3,
    metodo: str = "ward"
) -> dict:
    # VALIDAR COLUMNAS
    if not columnas:
        raise ValueError("Debes seleccionar al menos una columna.")

    if len(columnas) != len(set(columnas)):
        raise ValueError("No puedes repetir columnas.")

    for columna in columnas:

        if columna not in df.columns:
            raise ValueError(f"La columna '{columna}' no existe.")

        if not pd.api.types.is_numeric_dtype(df[columna]):
            raise ValueError(
                f"La columna '{columna}' debe ser numérica."
            )
      # VALIDAR CANTIDAD DE GRUPOS
    if not isinstance(n_clusters, int) or isinstance(n_clusters, bool):
        raise ValueError("La cantidad de grupos debe ser un entero.")

    if n_clusters < 2:
        raise ValueError("Debes solicitar al menos 2 grupos.")

    # VALIDAR METODO
    metodos_validos = ["ward", "complete", "average", "single"]

    if metodo not in metodos_validos:
        raise ValueError("El método de agrupamiento no es válido.")

    # PREPARAR LOS DATOS
    datos = df[columnas].dropna().copy()

    if not datos.apply(
        lambda columna: columna.map(
            lambda valor: abs(valor) != float("inf")
        ).all()
    ).all():
        raise ValueError("Los datos contienen valores infinitos.")

    if len(datos) < 2:
        raise ValueError("Se necesitan al menos dos observaciones.")

    if n_clusters >= len(datos):
        raise ValueError(
            "La cantidad de grupos debe ser menor "
            "que el número de observaciones."
        )

    # ESTANDARIZAR LOS DATOS
    escalador = StandardScaler()
    datos_escalados = escalador.fit_transform(datos)

    # CALCULAR AGRUPAMIENTO
    modelo = AgglomerativeClustering(
        n_clusters=n_clusters,
        linkage=metodo
    )

    etiquetas = modelo.fit_predict(datos_escalados)

    # CREAR COPIA CON LOS RESULTADOS
    df_resultado = df.copy()

    df_resultado["cluster"] = pd.Series(
        pd.NA,
        index=df.index,
        dtype="Int64"
    )

    df_resultado.loc[datos.index, "cluster"] = etiquetas

    # CONSTRUIR DENDROGRAMA
    matriz_enlace = linkage(
        datos_escalados,
        method=metodo
    )

    plt.figure(figsize=(12, 7))

    dendrogram(
        matriz_enlace,
        no_labels=True
    )

    plt.title("Dendrograma - Clustering jerárquico")
    plt.xlabel("Observaciones")
    plt.ylabel("Distancia")
    plt.tight_layout()

    # GUARDAR GRAFICA
    carpeta = Path("resultados/graficas")
    carpeta.mkdir(parents=True, exist_ok=True)

    ruta = carpeta / "dendrograma_clustering.png"

    plt.savefig(ruta, dpi=300, bbox_inches="tight")

    plt.show()
    plt.close()

    # ORGANIZAR RESULTADOS
    return {
        "dataframe": df_resultado,
        "columnas_utilizadas": columnas,
        "observaciones_agrupadas": len(datos),
        "observaciones_excluidas": len(df) - len(datos),
        "cantidad_clusters": n_clusters,
        "metodo": metodo,
        "distribucion_clusters": {
            int(cluster): int(cantidad)
            for cluster, cantidad in (
                df_resultado["cluster"].value_counts().sort_index().items()
            )
        },
        "grafica": str(ruta)
    }

    