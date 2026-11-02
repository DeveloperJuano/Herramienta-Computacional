# ===========================================================
# IMPORTS
# ===========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# ===========================================================
# FUNCION: REGRESION LINEAL
# ===========================================================
def regresion_lineal(
    df: pd.DataFrame,
    columna_x: str,
    columna_y: str
) -> dict:

    # VALIDAR QUE LAS COLUMNAS EXISTAN
    if columna_x not in df.columns:
        raise ValueError(f"La columna X '{columna_x}' no existe.")
    if columna_y not in df.columns:
        raise ValueError(f"La columna Y '{columna_y}' no existe.")

    # VALIDAR QUE LAS COLUMNAS SEAN NUMERICAS
    if not pd.api.types.is_numeric_dtype(df[columna_x]):
        raise ValueError("La variable X debe ser numérica.")
    if not pd.api.types.is_numeric_dtype(df[columna_y]):
        raise ValueError("La variable Y debe ser numérica.")

    # PREPARAR LOS DATOS
    datos = df[[columna_x, columna_y]].dropna().copy()
    if len(datos) < 2:
        raise ValueError("Se necesitan al menos dos observaciones válidas.")

    
    # SEPARAR VARIABLES
    X = datos[[columna_x]]
    y = datos[columna_y]

    # CREAR MODELO
    modelo = LinearRegression()

    # ENTRENAR MODELO
    modelo.fit(X, y)

    # REALIZAR PREDICCIONES
    predicciones = modelo.predict(X)

    
    # CALCULAR METRICAS
    r2 = r2_score(y, predicciones)
    error = mean_squared_error(y, predicciones)

    # OBTENER COEFICIENTES
    pendiente = float(modelo.coef_[0])
    intercepto = float(modelo.intercept_)

    # ORGANIZAR RESULTADOS
    resultados = {
        "variable_x": columna_x,
        "variable_y": columna_y,
        "observaciones": len(datos),
        "pendiente": pendiente,
        "intercepto": intercepto,
        "r2": float(r2),
        "error_cuadratico_medio": float(error)
    }

    # ===========================================================
    # CREAR GRAFICA
    # ===========================================================
    
    # ORDENAR LOS VALORES PARA DIBUJAR LA LINEA
    orden = np.argsort(X[columna_x].to_numpy())

    x_ordenado = X[columna_x].to_numpy()[orden]
    predicciones_ordenadas = predicciones[orden]

    # CREAR GRAFICA
    plt.figure(figsize=(9, 6))

    plt.scatter(
        X[columna_x],
        y,
        alpha=0.6,
        label="Datos reales"
    )

    plt.plot(
        x_ordenado,
        predicciones_ordenadas,
        label="Regresión lineal",
        linewidth=2
    )

    plt.xlabel(columna_x)
    plt.ylabel(columna_y)
    plt.title("Modelo de regresión lineal")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    # GUARDAR GRAFICA
    carpeta = Path("resultados/graficas")
    carpeta.mkdir(parents=True, exist_ok=True)

    ruta = carpeta / f"regresion_{columna_x}_{columna_y}.png"

    plt.savefig(ruta, dpi=300, bbox_inches="tight")

    plt.show()
    plt.close()

    resultados["grafica"] = str(ruta)

    return resultados


