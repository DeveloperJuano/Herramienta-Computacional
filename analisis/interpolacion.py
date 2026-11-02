# ===========================================================
# IMPORTS
# ===========================================================

import pandas as pd

# ===========================================================
# FUNCION: INTERPOLACION LINEAL
# ===========================================================

def interpolacion_lineal(
    df: pd.DataFrame,
    columna: str,
    columna_orden: str = None,
    columnas_grupo: list = None
) -> pd.DataFrame:

    # VALIDAR COLUMNA A INTERPOLAR
    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe.")
    if not pd.api.types.is_numeric_dtype(df[columna]):
        raise ValueError("La columna debe ser numérica.")

    # VALIDAR COLUMNA DE ORDEN
    if columna_orden is not None:
        if columna_orden not in df.columns:
            raise ValueError("La columna de orden no existe.")

    # VALIDAR COLUMNAS DE AGRUPACION
    if columnas_grupo is None:
        columnas_grupo = []

    for nombre in columnas_grupo:
        if nombre not in df.columns:
            raise ValueError(
                f"La columna de agrupación '{nombre}' no existe."
            )

    if columna in columnas_grupo or columna_orden in columnas_grupo:
        raise ValueError(
            "La columna a interpolar y la columna de orden "
            "no pueden utilizarse como columnas de agrupación."
        )

    # CREAR COPIA
    df_interpolado = df.copy()

    # ORDENAR SI SE INDICA UNA COLUMNA
    if columna_orden is not None:

        df_interpolado = df_interpolado.sort_values(
            columnas_grupo + [columna_orden]
        )

    # INTERPOLAR POR GRUPOS O TODA LA COLUMNA
    if columnas_grupo:

        df_interpolado[columna] = (
            df_interpolado
            .groupby(columnas_grupo, dropna=False)[columna]
            .transform(
                lambda serie: serie.interpolate(
                    method="linear",
                    limit_area="inside"
                )
            )
        )

    else:

        df_interpolado[columna] = (
            df_interpolado[columna].interpolate(
                method="linear",
                limit_area="inside"
            )
        )

    # RECUPERAR ORDEN ORIGINAL
    df_interpolado = df_interpolado.sort_index()

    return df_interpolado

# ===========================================================
# FUNCION: COMPARAR INTERPOLACION 
# ===========================================================


def comparar_interpolacion(
    df_original: pd.DataFrame,
    df_interpolado: pd.DataFrame,
    columna: str
) -> dict:

    # VALIDAR COLUMNAS
    if columna not in df_original.columns:
        raise ValueError("La columna no existe en los datos originales.")

    if columna not in df_interpolado.columns:
        raise ValueError("La columna no existe en los datos interpolados.")

    # CONTAR VALORES NULOS
    nulos_originales = int(df_original[columna].isna().sum())
    nulos_finales = int(df_interpolado[columna].isna().sum())

    # CALCULAR VALORES COMPLETADOS
    valores_completados = nulos_originales - nulos_finales

    # ORGANIZAR RESULTADOS
    return {
        "columna": columna,
        "filas_originales": len(df_original),
        "filas_finales": len(df_interpolado),
        "nulos_originales": nulos_originales,
        "nulos_finales": nulos_finales,
        "valores_completados": valores_completados
    }

