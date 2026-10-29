# ===========================================================
# IMPORTS
# ===========================================================
import customtkinter as ctk

# ===========================================================
# CLASE PRINCIPAL
# ===========================================================

class VentanaPrincipal(ctk.CTk):
    def __init__(self): #metodo iniciador
        super().__init__() #inicia la clase CTk 

        # TITULO DE VENTANA JUNTO A CONFIGURACION DE LA MISMA
        self.title("Herramienta Computacional")
        self.geometry("1000x650")
        self.minsize(800, 550)
        
        # COLOR DE FONDO
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        # TITULO 
        titulo = ctk.CTkLabel(
            self,
            text="Herramienta de Análisis Estadístico",
            font=("Arial", 26, "bold")
        )
        titulo.pack(pady=30)
        # DESCRIPCION 
        descripcion = ctk.CTkLabel(
            self,
            text="Análisis de datos, regresión, interpolación y clustering",
            font=("Arial", 15)
        )
        descripcion.pack(pady=10)
