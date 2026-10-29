# ===========================================================
# IMPORTS
# ===========================================================

from interfaz.ventana_principal import VentanaPrincipal
from analisis.carga_datos import cargar_csv

ruta = "datos/originales/panel_ciudades_2012_2025 .csv"

df = cargar_csv(ruta)

print(df.head())
print("Dimensiones:", df.shape)
print("Columnas:", df.columns.tolist())

# ===========================================================
# FUNCION PRINCIPAL
# ===========================================================
def main():
    app = VentanaPrincipal() #creacion de instancia
    app.mainloop() #ciclo de eventos interfaz

# ===========================================================
# CONDICIONAL DE  INICIO DE APLICACION
# ===========================================================
# comprobacion de ejecucion directa

if __name__  == "__main__":
    main()

