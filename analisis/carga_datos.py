import pandas as pd
from pathlib import Path


def cargar_csv(ruta: str) -> pd.DataFrame:
    archivo = Path(ruta)

    if not archivo.exists():
        raise FileNotFoundError("El archivo seleccionado no existe.")

    if archivo.suffix.lower() != ".csv":
        raise ValueError("El archivo debe tener formato CSV.")

    df = pd.read_csv(archivo)

    return df