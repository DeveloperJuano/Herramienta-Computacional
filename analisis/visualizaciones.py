# ===========================================================
# IMPORTS
# ===========================================================
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ==========================================
# FUNCION: CREAR HISTOGRAMA
# ==========================================

def crear_histograma(
    df: pd.DataFrame,
    columna: str
) -> None:

    # VALIDAR QUE LA COLUMNA EXISTA
    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe.")

    # VALIDAR QUE SEA NUMERICA
    if not pd.api.types.is_numeric_dtype(df[columna]):
        raise ValueError("La columna seleccionada debe ser numérica.")

    # ELIMINAR VALORES FALTANTES PARA LA GRAFICA
    datos = df[columna].dropna()

    if datos.empty:
        raise ValueError("La columna no contiene datos numéricos válidos.")

    # CREAR CARPETA PARA GUARDAR GRAFICAS
    carpeta = Path("resultados/graficas")
    carpeta.mkdir(parents=True, exist_ok=True)

    # CONSTRUIR HISTOGRAMA
    plt.figure(figsize=(8, 5))
    plt.hist(datos, bins=15, edgecolor="black")

    plt.title(f"Distribución de {columna}")
    plt.xlabel(columna)
    plt.ylabel("Frecuencia")

    plt.tight_layout()

    # GUARDAR GRAFICA
    ruta = carpeta / f"histograma_{columna}.png"
    plt.savefig(ruta, dpi=300, bbox_inches="tight")

    # MOSTRAR GRAFICA
    plt.show()
    plt.close()

# ==========================================
# FUNCION: CREAR BARRAS
# ==========================================

def crear_grafico_barras(
    df: pd.DataFrame,
    columna_categoria: str,
    columna_valor: str
) -> None:

    # VALIDAR QUE LAS COLUMNAS EXISTAN
    if columna_categoria not in df.columns:
        raise ValueError(
            f"La columna '{columna_categoria}' no existe."
        )

    if columna_valor not in df.columns:
        raise ValueError(
            f"La columna '{columna_valor}' no existe."
        )

    # VALIDAR QUE LA COLUMNA DEL VALOR SEA NUMERICA
    if not pd.api.types.is_numeric_dtype(df[columna_valor]):
        raise ValueError(
            "La columna de valores debe ser numérica."
        )

    # PREPARAR LOS DATOS
    datos = df[[columna_categoria, columna_valor]].dropna()

    if datos.empty:
        raise ValueError("No hay datos válidos para graficar.")

    # AGRUPAR Y CALCULAR EL PROMEDIO
    resumen = datos.groupby(columna_categoria)[columna_valor].mean()

    # CREAR GRAFICA
    plt.figure(figsize=(10, 5))

    plt.bar(
        resumen.index.astype(str),
        resumen.values,
        edgecolor="black"
    )

    plt.title(f"Promedio de {columna_valor} por {columna_categoria}")
    plt.xlabel(columna_categoria)
    plt.ylabel(f"Promedio de {columna_valor}")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # GUARDAR GRAFICA
    carpeta = Path("resultados/graficas")
    carpeta.mkdir(parents=True, exist_ok=True)

    ruta = carpeta / f"barras_{columna_valor}_por_{columna_categoria}.png"

    plt.savefig(ruta, dpi=300, bbox_inches="tight")

    # MOSTRAR Y CERRAR
    plt.show()
    plt.close()

# ==========================================
# FUNCION: CREAR DISPERCION
# ==========================================
def crear_grafico_dispersion(
    df: pd.DataFrame,
    columna_x: str,
    columna_y: str
) -> None:

    # VALIDAR QUE LAS COLUMNAS EXISTAN
    if columna_x not in df.columns:
        raise ValueError(f"La columna '{columna_x}' no existe.")

    if columna_y not in df.columns:
        raise ValueError(f"La columna '{columna_y}' no existe.")

    # VALIDAR QUE AMBAS COLUMNAS SEAN NUMERICAS
    if not pd.api.types.is_numeric_dtype(df[columna_x]):
        raise ValueError("La columna X debe ser numérica.")

    if not pd.api.types.is_numeric_dtype(df[columna_y]):
        raise ValueError("La columna Y debe ser numérica.")

    # PREPARAR LOS DATOS
    datos = df[[columna_x, columna_y]].dropna()

    if datos.empty:
        raise ValueError("No hay datos válidos para graficar.")

    # CREAR GRAFICA
    plt.figure(figsize=(8, 5))

    plt.scatter(
        datos[columna_x],
        datos[columna_y],
        alpha=0.7
    )

    plt.title(f"Relación entre {columna_x} y {columna_y}")
    plt.xlabel(columna_x)
    plt.ylabel(columna_y)

    plt.tight_layout()

    # GUARDAR GRAFICA
    carpeta = Path("resultados/graficas")
    carpeta.mkdir(parents=True, exist_ok=True)

    ruta = carpeta / f"dispersion_{columna_x}_{columna_y}.png"

    plt.savefig(ruta, dpi=300, bbox_inches="tight")

    # MOSTRAR Y CERRAR
    plt.show()
    plt.close()

# ==========================================
# FUNCION: CREAR BOXPLOT
# ==========================================

def crear_boxplot(
    df: pd.DataFrame,
    columna: str
) -> None:

    # VALIDAR QUE LA COLUMNA EXISTA
    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe.")

    # VALIDAR QUE SEA NUMERICA
    if not pd.api.types.is_numeric_dtype(df[columna]):
        raise ValueError("La columna debe ser numérica.")

    # PREPARAR LOS DATOS
    datos = df[columna].dropna()
    # 
    # 
    # 
    # print("Mediana:", datos.median())
    # print("Primer cuartil:", datos.quantile(0.25))
    # print("Tercer cuartil:", datos.quantile(0.75))
    # print("Valor mínimo:", datos.min())
    # print("Valor máximo:", datos.max())
    # 
    # 
    if datos.empty:
        raise ValueError("No hay datos válidos para graficar.")

    # CREAR GRAFICA
    plt.figure(figsize=(8, 5))

    plt.boxplot(
        datos,
        vert=True,
        patch_artist=True
    )

    plt.title(f"Distribución de {columna}")
    plt.ylabel(columna)
    plt.xticks([1], [columna])

    plt.tight_layout()

    # GUARDAR GRAFICA
    carpeta = Path("resultados/graficas")
    carpeta.mkdir(parents=True, exist_ok=True)

    ruta = carpeta / f"boxplot_{columna}.png"

    plt.savefig(ruta, dpi=300, bbox_inches="tight")

    # MOSTRAR Y CERRAR
    plt.show()
    plt.close()

# ==========================================
# FUNCION: CREAR MAPA DE CALOR
# ==========================================

def crear_mapa_calor(df: pd.DataFrame) -> None:

    # SELECCIONAR COLUMNAS NUMERICAS
    datos = df.select_dtypes(include="number")

    # VALIDAR QUE EXISTAN SUFICIENTES COLUMNAS
    if datos.shape[1] < 2:
        raise ValueError(
            "Se necesitan al menos dos columnas numéricas."
        )

    # CALCULAR MATRIZ DE CORRELACION
    correlacion = datos.corr()
    # 
    # 
    # print("\nMATRIZ DE CORRELACIONES:")
    # print(correlacion.round(2).to_string())
    # 
    # 
    # CREAR GRAFICA
    plt.figure(figsize=(12, 9))

    imagen = plt.imshow(
        correlacion,
        cmap="coolwarm",
        vmin=-1,
        vmax=1
    )

    # AGREGAR NOMBRES DE LAS VARIABLES
    plt.xticks(
        range(len(correlacion.columns)),
        correlacion.columns,
        rotation=90
    )

    plt.yticks(
        range(len(correlacion.columns)),
        correlacion.columns
    )

    # AGREGAR VALORES A LAS CELDAS
    for fila in range(len(correlacion.columns)):
        for columna in range(len(correlacion.columns)):

            valor = correlacion.iloc[fila, columna]

            plt.text(
                columna,
                fila,
                f"{valor:.2f}",
                ha="center",
                va="center",
                fontsize=8
            )

    # BARRA DE COLOR
    plt.colorbar(imagen, label="Correlación")

    plt.title("Mapa de calor de correlaciones")

    plt.tight_layout()

    # GUARDAR GRAFICA
    carpeta = Path("resultados/graficas")
    carpeta.mkdir(parents=True, exist_ok=True)

    ruta = carpeta / "mapa_calor_correlaciones.png"

    plt.savefig(ruta, dpi=300, bbox_inches="tight")

    # MOSTRAR Y CERRAR
    plt.show()
    plt.close()


