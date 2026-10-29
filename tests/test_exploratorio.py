
import pandas as pd

from analisis.exploratorio import *

# ===========================================================
# FUNCION DE ANALISIS DE ARCHIVO
# ===========================================================
def test_resumen_datos():
    # 1. PREPARAR DATOS DE PRUEBA
    df = pd.DataFrame({
        "nombre": ["Ana", "Luis", "Carlos"],
        "edad": [20, 25, 30]
    })

    # 2. EJECUTAR LA FUNCIÓN
    resultado = resumen_datos(df)

    # 3. COMPROBAR EL RESULTADO
    assert resultado["filas"] == 3
    assert resultado["columnas"] == 2
    assert resultado["nombres_columnas"] == ["nombre", "edad"]

# ===========================================================
#DECTAR VALORES NULOS
# ===========================================================
def test_nulos ():

    df = pd.DataFrame({
            "nombre": ["Ana", "Luis", None],
            "edad": [20, None, 30]
        })
    
    resultado = analizar_nulos(df)

    assert resultado["nulos_por_columna"] == {
        "nombre": 1,
        "edad": 1
    }
    assert resultado["total_nulos"] == 2
    
    assert resultado["porcentaje_nulos"] == {
        "nombre": 33.33,
        "edad": 33.33
    }

# ===========================================================
# ESTADISTICA DESCRIPTIVA
# ===========================================================

def test_estadisticas_descriptivas():
    df = pd.DataFrame({
        "edad": [10, 20, 30],
        "nombre": ["Ana", "Luis", "Carlos"]
    })

    resultado = estadisticas_descriptivas(df)

    assert "edad" in resultado
    assert "nombre" not in resultado
    assert resultado["edad"]["mean"] == 20  

# ===========================================================
# ANALIZAR DUPLICADOS
# ===========================================================

def test_analizar_duplicados():
    df = pd.DataFrame({
        "nombre": ["Ana", "Luis", "Ana"],
        "edad": [20, 25, 20]
    })

    resultado = analizar_duplicados(df)

    assert resultado["total_duplicados"] == 1