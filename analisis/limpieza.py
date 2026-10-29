# ===========================================================
# IMPORTS
# ===========================================================
import pandas as pd

# ===========================================================
# ELIMINA DUPLICADOS
# ===========================================================
def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    df_limpio = df.drop_duplicates().copy()
    return df_limpio

# ===========================================================
# ELIMINA FILAS CON VALORES FALTANTES
# ===========================================================
def eliminar_filas_nulas(df: pd.DataFrame) -> pd.DataFrame:
    df_limpio = df.dropna().copy()
    return df_limpio

# ===========================================================
# REMPLAZA VALORES FALTANTES POR LA MEDIANA
# ===========================================================
def rellenar_nulos_mediana(df: pd.DataFrame) -> pd.DataFrame:
    # crea una copia
    df_limpio = df.copy()

    columnas_numericas = df_limpio.select_dtypes(include="number").columns
    # recorre cada columna
    for columna in columnas_numericas: 
        # calcula la mediana de cada columna 
        mediana = df_limpio[columna].median()
        # reemplaza valores faltantes por la mmediana
        df_limpio[columna] = df_limpio[columna].fillna(mediana)

    # devuelve la  tabla procesada
    return df_limpio

# ===========================================================
# REMPLAZA VALORES FALTANTES POR LA MEDIA
# ===========================================================
def rellenar_nulos_media(df: pd.DataFrame) -> pd.DataFrame:

    df_limpio = df.copy()

    columnas_numericas = df_limpio.select_dtypes(include="number").columns

    for columna in columnas_numericas:
        # calcula la media de cada columna 
        media = df_limpio[columna].mean()
        # reemplaza valores faltantes por la mmedia
        df_limpio[columna] = df_limpio[columna].fillna(media)

    return df_limpio

# ===========================================================
# REMPLAZA VALORES FALTANTES POR LA MODA    
# ===========================================================
def rellenar_nulos_moda(df: pd.DataFrame) -> pd.DataFrame:
    df_limpio = df.copy()

    for columna in df_limpio.columns:
        modas = df_limpio[columna].mode()

        if not modas.empty:
            df_limpio[columna] = df_limpio[columna].fillna(modas.iloc[0])

    return df_limpio

# ================================================================================================
# COMPARA DATOS =================================== ORIGINAL------------ MODIFICADOS
# ====================================================================================================
def comparar_datos(
    df_original: pd.DataFrame,
    df_limpio: pd.DataFrame
) -> dict:
    return {
        "filas_originales": len(df_original),
        "filas_finales": len(df_limpio),
        "columnas_originales": len(df_original.columns),
        "columnas_finales": len(df_limpio.columns),
        "nulos_originales": int(df_original.isna().sum().sum()),
        "nulos_finales": int(df_limpio.isna().sum().sum()),
        "duplicados_originales": int(df_original.duplicated().sum()),
        "duplicados_finales": int(df_limpio.duplicated().sum()),
    }
