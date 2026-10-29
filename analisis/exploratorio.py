# ===========================================================
# IMPORTS
# ===========================================================
import pandas as pd

# ===========================================================
# FUNCION DE ANALISIS DE ARCHIVO
# ===========================================================

def resumen_datos(df: pd.DataFrame) -> dict:

    # OBTENER DIMENCIONES
    # devuelve 2 numeros
    # 1 numero de filas
    # 2 numero de columnas
    total_filas, total_columnas = df.shape
    
    # NOMBRES DE COLUMNAS
    # df.columns obtiene los nombres de las columnas.
    # .tolist() los convierte en una lista de Python.
    nombres_columnas = df.columns.to_list()

    # OBTENER TIPO DE DATO

    tipos_datos = df.dtypes.astype(str).to_dict()

    return{
        "filas": total_filas,
        "columnas": total_columnas,
        "nombres_columnas": nombres_columnas,
        "tipos_datos": tipos_datos,
    }
# ===========================================================
#DECTAR VALORES NULOS
# ===========================================================

def analizar_nulos (df: pd.DataFrame) -> dict:

    # CONTAR LOS VALORES NULLOS POR COLUMNA
    # df.isna() decta si es nula 
    # .sum() suma los valores nulos
    nulos_por_columna =  df.isna().sum().to_dict()

    # CALCULAR PORCENTAJES NULOS
    if len(df) > 0 :
        porcentaje_nulos = (df.isna().mean() * 100).round(2).to_dict()
    else:
        porcentaje_nulos = {
            columna: 0.0 for columna in df.columns
        }   
    # CONTAR TODOS LOS VALORES NULOS
    total_nulos = int(df.isna().sum().sum())

    return {
        "nulos_por_columna": nulos_por_columna,
        "porcentaje_nulos": porcentaje_nulos,
        "total_nulos": total_nulos,
    }

# ===========================================================
# ESTADISTICA DESCRIPTIVA
# ===========================================================

def estadisticas_descriptivas(df: pd.DataFrame) -> dict:
    
    columnas_numericas = df.select_dtypes(include="number")

    estadisticas = columnas_numericas.describe().to_dict()

    return estadisticas
# ===========================================================
# ANALIZAR DUPLICADOS
# ===========================================================
def analizar_duplicados(df: pd.DataFrame) -> dict:
    total_duplicados = int(df.duplicated().sum())

    return {
        "total_duplicados": total_duplicados
    }
