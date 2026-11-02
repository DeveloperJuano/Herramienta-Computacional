# ===========================================================
# IMPORTS
# ===========================================================

from interfaz.ventana_principal import VentanaPrincipal
from analisis.carga_datos import cargar_csv

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

