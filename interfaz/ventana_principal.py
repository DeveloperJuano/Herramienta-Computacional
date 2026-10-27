
import customtkinter as ctk


class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Herramienta Computacional")
        self.geometry("1000x650")
        self.minsize(800, 550)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        titulo = ctk.CTkLabel(
            self,
            text="Herramienta de Análisis Estadístico",
            font=("Arial", 26, "bold")
        )
        titulo.pack(pady=30)

        descripcion = ctk.CTkLabel(
            self,
            text="Análisis de datos, regresión, interpolación y clustering",
            font=("Arial", 15)
        )
        descripcion.pack(pady=10)
