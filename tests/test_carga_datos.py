import pandas as pd
import pytest
from analisis.carga_datos import cargar_csv


def test_cargar_csv(tmp_path):
    archivo = tmp_path / "datos.csv"

    df_original = pd.DataFrame({
        "nombre": ["Ana", "Luis"],
        "edad": [20, 25]
    })

    df_original.to_csv(archivo, index=False)

    resultado = cargar_csv(str(archivo))

    assert resultado.shape == (2, 2)
    assert resultado["nombre"].tolist() == ["Ana", "Luis"]
    assert resultado["edad"].tolist() == [20, 25]


def test_cargar_csv_archivo_inexistente(tmp_path):
    archivo = tmp_path / "inexistente.csv"

    with pytest.raises(FileNotFoundError):
        cargar_csv(str(archivo))


def test_cargar_csv_extension_incorrecta(tmp_path):
    archivo = tmp_path / "datos.txt"
    archivo.write_text("contenido de prueba", encoding="utf-8")

    with pytest.raises(ValueError):
        cargar_csv(str(archivo))