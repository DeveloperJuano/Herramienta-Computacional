
# ============================================================
# IMPORTS
# ============================================================

import customtkinter as ctk
import pandas as pd

from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from PIL import Image

from analisis.carga_datos import cargar_csv

from analisis.exploratorio import (
    resumen_datos,
    analizar_nulos,
    estadisticas_descriptivas,
    analizar_duplicados
)

from analisis.limpieza import (
    eliminar_filas_nulas,
    rellenar_nulos_mediana,
    rellenar_nulos_media,
    rellenar_nulos_moda,
    eliminar_duplicados,
    comparar_datos
)

from analisis.visualizaciones import (
    crear_histograma,
    crear_grafico_barras,
    crear_grafico_dispersion,
    crear_boxplot,
    crear_mapa_calor
)

from analisis.regresion import regresion_lineal

from analisis.interpolacion import (
    interpolacion_lineal,
    comparar_interpolacion
)

from analisis.clustering import clustering_jerarquico


# ============================================================
# CONFIGURACION GENERAL
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class VentanaPrincipal(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Herramienta Computacional | Análisis Estadístico")
        self.geometry("1350x850")
        self.minsize(1050, 700)

        # Datos
        self.df = None
        self.df_procesado = None
        self.archivo_actual = None

        # Elementos dinámicos
        self.botones = {}
        self.imagen_actual = None
        self.checkboxes_clustering = {}

        # Configuración de la ventana
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Construcción de la interfaz
        self.crear_menu_lateral()
        self.crear_area_trabajo()

        self.mostrar_inicio()

    # ========================================================
    # ESTRUCTURA PRINCIPAL
    # ========================================================

    def crear_menu_lateral(self):

        self.menu_lateral = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0
        )

        self.menu_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.menu_lateral.grid_propagate(False)

        # Nombre del programa
        ctk.CTkLabel(
            self.menu_lateral,
            text="HERRAMIENTA\nCOMPUTACIONAL",
            font=("Arial", 19, "bold"),
            justify="left"
        ).pack(anchor="w", padx=22, pady=(30, 8))

        ctk.CTkLabel(
            self.menu_lateral,
            text="ANÁLISIS ESTADÍSTICO",
            font=("Arial", 10, "bold"),
            text_color="gray"
        ).pack(anchor="w", padx=22, pady=(0, 25))

        # Opciones de navegación
        opciones = [
            ("Inicio", self.mostrar_inicio),
            ("Carga de datos", self.mostrar_carga),
            ("Análisis exploratorio", self.mostrar_exploratorio),
            ("Limpieza de datos", self.mostrar_limpieza),
            ("Visualizaciones", self.mostrar_visualizaciones),
            ("Regresión lineal", self.mostrar_regresion),
            ("Interpolación", self.mostrar_interpolacion),
            ("Clustering", self.mostrar_clustering)
        ]

        for nombre, funcion in opciones:

            boton = ctk.CTkButton(
                self.menu_lateral,
                text=nombre,
                anchor="w",
                height=42,
                corner_radius=8,
                fg_color="transparent",
                hover_color=("gray75", "gray25"),
                text_color=("gray15", "gray90"),
                command=lambda f=funcion, n=nombre: self.navegar(f, n)
            )

            boton.pack(fill="x", padx=12, pady=3)

            self.botones[nombre] = boton

        # Información inferior
        ctk.CTkLabel(
            self.menu_lateral,
            text="Herramienta de análisis\nestadístico de datos",
            font=("Arial", 10),
            text_color="gray"
        ).pack(side="bottom", anchor="w", padx=20, pady=25)

    def crear_area_trabajo(self):

        self.area = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
        )

        self.area.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=20,
            pady=15
        )

        self.area.grid_columnconfigure(0, weight=1)
        self.area.grid_rowconfigure(1, weight=1)

        # Encabezado
        self.encabezado = ctk.CTkFrame(
            self.area,
            fg_color="transparent"
        )

        self.encabezado.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        self.encabezado.grid_columnconfigure(0, weight=1)

        self.titulo_pagina = ctk.CTkLabel(
            self.encabezado,
            text="Inicio",
            font=("Arial", 26, "bold")
        )

        self.titulo_pagina.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.estado_archivo = ctk.CTkLabel(
            self.encabezado,
            text="Sin archivo cargado",
            text_color="gray",
            font=("Arial", 12)
        )

        self.estado_archivo.grid(
            row=0,
            column=1,
            sticky="e",
            padx=10
        )

        # Área de contenido
        self.contenido = ctk.CTkScrollableFrame(
            self.area,
            corner_radius=12
        )

        self.contenido.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

    # ========================================================
    # NAVEGACIÓN Y COMPONENTES GENERALES
    # ========================================================

    def navegar(self, funcion, nombre):

        for boton in self.botones.values():
            boton.configure(
                fg_color="transparent",
                text_color=("gray15", "gray90")
            )

        self.botones[nombre].configure(
            fg_color=("#dbeafe", "#1e3a5f"),
            text_color=("#1e3a8a", "#ffffff")
        )

        funcion()

    def limpiar_area(self):

        for widget in self.contenido.winfo_children():
            widget.destroy()

        self.imagen_actual = None

    def crear_encabezado(self, titulo, descripcion=""):

        self.limpiar_area()

        self.titulo_pagina.configure(text=titulo)

        if descripcion:

            ctk.CTkLabel(
                self.contenido,
                text=descripcion,
                font=("Arial", 13),
                text_color="gray"
            ).pack(anchor="w", padx=15, pady=(5, 15))

    def crear_seccion(self, titulo, descripcion=None):

        contenedor = ctk.CTkFrame(
            self.contenido,
            fg_color="transparent"
        )

        contenedor.pack(
            fill="x",
            padx=15,
            pady=(20, 8)
        )

        ctk.CTkLabel(
            contenedor,
            text=titulo,
            font=("Arial", 19, "bold")
        ).pack(anchor="w")

        if descripcion:

            ctk.CTkLabel(
                contenedor,
                text=descripcion,
                font=("Arial", 12),
                text_color="gray"
            ).pack(anchor="w", pady=(4, 0))

        return contenedor

    def crear_panel(self, padre=None):

        if padre is None:
            padre = self.contenido

        panel = ctk.CTkFrame(
            padre,
            corner_radius=12
        )

        panel.pack(
            fill="x",
            padx=15,
            pady=6
        )

        return panel

    def crear_boton(self, padre, texto, comando, color=None):

        boton = ctk.CTkButton(
            padre,
            text=texto,
            command=comando,
            height=40,
            corner_radius=8,
            fg_color=color
        )

        boton.pack(
            anchor="w",
            padx=15,
            pady=12
        )

        return boton

    def crear_etiqueta(self, padre, texto):

        ctk.CTkLabel(
            padre,
            text=texto,
            font=("Arial", 13, "bold")
        ).pack(anchor="w", padx=15, pady=(12, 5))

    def crear_selector(self, padre, valores, placeholder="Seleccionar"):

        selector = ctk.CTkComboBox(
            padre,
            values=valores if valores else ["Sin opciones"],
            width=300,
            height=38,
            state="readonly"
        )

        selector.pack(
            anchor="w",
            padx=15,
            pady=(0, 10)
        )

        selector.set(placeholder if valores else "Sin opciones")

        return selector

    def crear_entrada(self, padre, valor="", placeholder="Escribir"):

        entrada = ctk.CTkEntry(
            padre,
            width=300,
            height=38,
            placeholder_text=placeholder
        )

        entrada.pack(
            anchor="w",
            padx=15,
            pady=(0, 10)
        )

        if valor != "":
            entrada.insert(0, str(valor))

        return entrada

    def mostrar_resultado(self, texto, padre=None):

        if padre is None:
            padre = self.contenido

        cuadro = ctk.CTkTextbox(
            padre,
            height=150,
            wrap="word"
        )

        cuadro.pack(
            fill="x",
            padx=15,
            pady=10
        )

        cuadro.insert("1.0", str(texto))
        cuadro.configure(state="disabled")

        return cuadro

    # ========================================================
    # TARJETAS DE INDICADORES
    # ========================================================

    def crear_tarjeta(self, padre, titulo, valor):

        tarjeta = ctk.CTkFrame(
            padre,
            corner_radius=12
        )

        tarjeta.grid(
            row=0,
            column=len(padre.winfo_children()),
            sticky="nsew",
            padx=5,
            pady=5
        )

        tarjeta.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=("Arial", 12),
            text_color="gray"
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        ctk.CTkLabel(
            tarjeta,
            text=f"{valor:,}",
            font=("Arial", 25, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 15)
        )

        return tarjeta

    # ========================================================
    # TABLAS
    # ========================================================

    def crear_tabla(self, padre, dataframe, altura=9):

        contenedor = ctk.CTkFrame(
            padre,
            corner_radius=10
        )

        contenedor.pack(
            fill="x",
            padx=15,
            pady=10
        )

        columnas = [str(col) for col in dataframe.columns]

        tabla = ttk.Treeview(
            contenedor,
            columns=columnas,
            show="headings",
            height=altura
        )

        estilo = ttk.Style()

        estilo.theme_use("default")

        estilo.configure(
            "Treeview",
            background="#242424",
            foreground="white",
            fieldbackground="#242424",
            rowheight=30,
            borderwidth=0
        )

        estilo.configure(
            "Treeview.Heading",
            background="#1f2937",
            foreground="white",
            font=("Arial", 10, "bold"),
            relief="flat"
        )

        estilo.map(
            "Treeview",
            background=[("selected", "#1d4ed8")],
            foreground=[("selected", "white")]
        )

        for columna in columnas:

            tabla.heading(
                columna,
                text=columna
            )

            tabla.column(
                columna,
                width=125,
                minwidth=90,
                anchor="center"
            )

        for _, fila in dataframe.iterrows():

            valores = []

            for valor in fila:

                if pd.isna(valor):
                    valores.append("")
                elif isinstance(valor, float):
                    valores.append(f"{valor:,.2f}")
                else:
                    valores.append(str(valor))

            tabla.insert(
                "",
                "end",
                values=valores
            )

        scroll_vertical = ttk.Scrollbar(
            contenedor,
            orient="vertical",
            command=tabla.yview
        )

        scroll_horizontal = ttk.Scrollbar(
            contenedor,
            orient="horizontal",
            command=tabla.xview
        )

        tabla.configure(
            yscrollcommand=scroll_vertical.set,
            xscrollcommand=scroll_horizontal.set
        )

        tabla.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scroll_vertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        scroll_horizontal.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        contenedor.grid_columnconfigure(0, weight=1)

        return tabla

    # ========================================================
    # DATOS Y VALIDACIONES
    # ========================================================

    def obtener_df(self):

        if self.df_procesado is None:
            raise ValueError("Primero debes cargar un archivo CSV.")

        return self.df_procesado

    def columnas_numericas(self):

        df = self.obtener_df()

        return df.select_dtypes(
            include="number"
        ).columns.tolist()

    def validar_archivo(self):

        if self.df is None:
            messagebox.showwarning(
                "Archivo requerido",
                "Primero debes cargar un archivo CSV."
            )
            return False

        return True

    def actualizar_estado_archivo(self):

        if self.archivo_actual:

            self.estado_archivo.configure(
                text=f"Archivo: {Path(self.archivo_actual).name}"
            )

        else:

            self.estado_archivo.configure(
                text="Sin archivo cargado"
            )

    def mostrar_imagen_reciente(self, fecha_anterior=0):

        carpeta = Path("resultados/graficas")

        if not carpeta.exists():
            return

        imagenes = list(carpeta.glob("*.png"))

        imagenes = [
            imagen for imagen in imagenes
            if imagen.stat().st_mtime >= fecha_anterior
        ]

        if not imagenes:
            return

        imagen = max(
            imagenes,
            key=lambda archivo: archivo.stat().st_mtime
        )

        try:

            original = Image.open(imagen)

            ancho_maximo = 850
            alto_maximo = 480

            original.thumbnail(
                (ancho_maximo, alto_maximo)
            )

            imagen_ctk = ctk.CTkImage(
                light_image=original,
                dark_image=original,
                size=original.size
            )

            self.imagen_actual = imagen_ctk

            panel = self.crear_panel()

            ctk.CTkLabel(
                panel,
                text=imagen.name,
                font=("Arial", 13, "bold")
            ).pack(
                anchor="w",
                padx=15,
                pady=10
            )

            ctk.CTkLabel(
                panel,
                text="",
                image=imagen_ctk
            ).pack(
                padx=15,
                pady=10
            )

        except Exception as error:

            messagebox.showerror(
                "Error al mostrar gráfica",
                str(error)
            )

    # ========================================================
    # INICIO
    # ========================================================

    def mostrar_inicio(self):

        self.crear_encabezado(
            "Inicio",
            "Bienvenido a la herramienta de análisis estadístico."
        )

        panel = self.crear_panel()

        ctk.CTkLabel(
            panel,
            text="Analiza tus datos de forma sencilla",
            font=("Arial", 24, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(30, 10)
        )

        ctk.CTkLabel(
            panel,
            text=(
                "Carga un archivo CSV y utiliza las herramientas "
                "disponibles para explorar, limpiar y analizar "
                "la información."
            ),
            font=("Arial", 14),
            text_color="gray",
            wraplength=700,
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 25)
        )

        self.crear_seccion("Módulos disponibles")

        modulos = [
            ("01", "Carga de datos", "Importación y vista previa de archivos CSV."),
            ("02", "Análisis exploratorio", "Resumen, tipos de datos, nulos y estadísticas."),
            ("03", "Limpieza", "Tratamiento de valores nulos y duplicados."),
            ("04", "Visualizaciones", "Gráficas para comprender los datos."),
            ("05", "Regresión lineal", "Análisis de relaciones entre variables."),
            ("06", "Interpolación", "Estimación de valores faltantes."),
            ("07", "Clustering", "Agrupamiento jerárquico de observaciones.")
        ]

        for numero, nombre, descripcion in modulos:

            panel = self.crear_panel()

            ctk.CTkLabel(
                panel,
                text=numero,
                font=("Arial", 18, "bold"),
                text_color="#60a5fa"
            ).pack(
                side="left",
                padx=20,
                pady=18
            )

            bloque = ctk.CTkFrame(
                panel,
                fg_color="transparent"
            )

            bloque.pack(
                side="left",
                fill="x",
                expand=True,
                pady=12
            )

            ctk.CTkLabel(
                bloque,
                text=nombre,
                font=("Arial", 14, "bold")
            ).pack(anchor="w")

            ctk.CTkLabel(
                bloque,
                text=descripcion,
                font=("Arial", 11),
                text_color="gray"
            ).pack(anchor="w")

        if self.archivo_actual:

            self.crear_seccion("Archivo cargado")

            self.mostrar_resultado(
                f"Archivo: {self.archivo_actual}\n"
                f"Filas: {len(self.obtener_df())}\n"
                f"Columnas: {len(self.obtener_df().columns)}"
            )

    # ========================================================
    # CARGA DE DATOS
    # ========================================================

    def mostrar_carga(self):

        self.crear_encabezado(
            "Carga de datos",
            "Selecciona un archivo CSV para comenzar el análisis."
        )

        panel = self.crear_panel()

        ctk.CTkLabel(
            panel,
            text="Importar archivo CSV",
            font=("Arial", 18, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            panel,
            text="Selecciona un archivo con extensión .csv.",
            text_color="gray"
        ).pack(
            anchor="w",
            padx=20,
            pady=5
        )

        self.crear_boton(
            panel,
            "Seleccionar archivo",
            self.seleccionar_archivo
        )

        if self.df is not None:

            self.crear_seccion("Información del archivo")

            resumen = resumen_datos(self.obtener_df())

            panel = self.crear_panel()

            ctk.CTkLabel(
                panel,
                text=f"Nombre: {Path(self.archivo_actual).name}",
                font=("Arial", 13)
            ).pack(anchor="w", padx=15, pady=6)

            ctk.CTkLabel(
                panel,
                text=f"Filas: {resumen['filas']} | Columnas: {resumen['columnas']}",
                font=("Arial", 13)
            ).pack(anchor="w", padx=15, pady=6)

            self.crear_seccion("Vista previa")

            self.crear_tabla(
                self.contenido,
                self.obtener_df().head(30),
                altura=10
            )

    def seleccionar_archivo(self):

        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[
                ("Archivos CSV", "*.csv"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not ruta:
            return

        try:

            df = cargar_csv(ruta)

            self.df = df.copy()
            self.df_procesado = df.copy()
            self.archivo_actual = ruta

            self.actualizar_estado_archivo()

            messagebox.showinfo(
                "Carga exitosa",
                f"Archivo cargado correctamente.\n\n"
                f"Filas: {len(df)}\n"
                f"Columnas: {len(df.columns)}"
            )

            self.mostrar_carga()

        except Exception as error:

            messagebox.showerror(
                "Error al cargar archivo",
                str(error)
            )

    # ========================================================
    # ANÁLISIS EXPLORATORIO
    # ========================================================

    def mostrar_exploratorio(self):

        self.crear_encabezado(
            "Análisis exploratorio",
            "Examina la estructura, calidad y distribución de tus datos."
        )

        panel = self.crear_panel()

        ctk.CTkLabel(
            panel,
            text="Análisis general del conjunto de datos",
            font=("Arial", 16, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        ctk.CTkLabel(
            panel,
            text="Se analizará el archivo actualmente cargado o procesado.",
            text_color="gray"
        ).pack(
            anchor="w",
            padx=15
        )

        self.crear_boton(
            panel,
            "Ejecutar análisis exploratorio",
            self.ejecutar_exploratorio
        )

    def ejecutar_exploratorio(self):

        if not self.validar_archivo():
            return

        try:

            df = self.obtener_df()

            resumen = resumen_datos(df)
            nulos = analizar_nulos(df)
            estadisticas = estadisticas_descriptivas(df)
            duplicados = analizar_duplicados(df)

            self.limpiar_area()

            # ------------------------------------------------
            # 1. INDICADORES PRINCIPALES
            # ------------------------------------------------

            self.crear_seccion(
                "Resumen general",
                "Indicadores principales del conjunto de datos."
            )

            tarjetas = ctk.CTkFrame(
                self.contenido,
                fg_color="transparent"
            )

            tarjetas.pack(
                fill="x",
                padx=10,
                pady=5
            )

            for i in range(4):
                tarjetas.grid_columnconfigure(i, weight=1)

            datos_tarjetas = [
                ("Total de filas", resumen["filas"]),
                ("Total de columnas", resumen["columnas"]),
                ("Valores nulos", nulos["total_nulos"]),
                ("Duplicados", duplicados["total_duplicados"])
            ]

            for i, (titulo, valor) in enumerate(datos_tarjetas):

                tarjeta = self.crear_tarjeta(
                    tarjetas,
                    titulo,
                    valor
                )

                tarjeta.grid(
                    row=0,
                    column=i,
                    sticky="nsew",
                    padx=5
                )

            # ------------------------------------------------
            # 2. TIPOS DE DATOS
            # ------------------------------------------------

            self.crear_seccion(
                "Distribución de tipos de datos",
                "Clasificación de las columnas según su tipo de información."
            )

            tipos = {}

            for columna, tipo in df.dtypes.items():

                if pd.api.types.is_bool_dtype(tipo):
                    categoria = "Booleanos"

                elif pd.api.types.is_integer_dtype(tipo):
                    categoria = "Enteros"

                elif pd.api.types.is_float_dtype(tipo):
                    categoria = "Decimales"

                elif pd.api.types.is_datetime64_any_dtype(tipo):
                    categoria = "Fechas"

                elif (
                    pd.api.types.is_object_dtype(tipo)
                    or pd.api.types.is_string_dtype(tipo)
                ):
                    categoria = "Texto"

                else:
                    categoria = "Otros"

                tipos.setdefault(categoria, []).append(columna)

            contenedor_tipos = ctk.CTkFrame(
                self.contenido,
                fg_color="transparent"
            )

            contenedor_tipos.pack(
                fill="x",
                padx=10
            )

            for i in range(2):
                contenedor_tipos.grid_columnconfigure(i, weight=1)

            for i, (categoria, columnas) in enumerate(tipos.items()):

                tarjeta = ctk.CTkFrame(
                    contenedor_tipos,
                    corner_radius=10
                )

                tarjeta.grid(
                    row=i // 2,
                    column=i % 2,
                    sticky="nsew",
                    padx=5,
                    pady=5
                )

                ctk.CTkLabel(
                    tarjeta,
                    text=categoria,
                    font=("Arial", 15, "bold")
                ).pack(
                    anchor="w",
                    padx=15,
                    pady=(12, 2)
                )

                ctk.CTkLabel(
                    tarjeta,
                    text=f"{len(columnas)} columnas",
                    font=("Arial", 21, "bold"),
                    text_color="#60a5fa"
                ).pack(
                    anchor="w",
                    padx=15,
                    pady=3
                )

                ctk.CTkLabel(
                    tarjeta,
                    text=", ".join(columnas),
                    wraplength=450,
                    justify="left",
                    text_color="gray"
                ).pack(
                    anchor="w",
                    padx=15,
                    pady=(2, 12)
                )

            # ------------------------------------------------
            # 3. VALORES NULOS
            # ------------------------------------------------

            self.crear_seccion(
                "Valores nulos por columna",
                "Cantidad de datos ausentes y porcentaje respecto al total de filas."
            )

            nulos_columnas = nulos["nulos_por_columna"]
            porcentajes = nulos["porcentaje_nulos"]

            columnas_con_nulos = {
                columna: cantidad
                for columna, cantidad in nulos_columnas.items()
                if cantidad > 0
            }

            if columnas_con_nulos:

                for columna, cantidad in columnas_con_nulos.items():

                    porcentaje = porcentajes[columna]

                    panel = self.crear_panel()

                    ctk.CTkLabel(
                        panel,
                        text=columna,
                        font=("Arial", 13, "bold")
                    ).pack(
                        anchor="w",
                        padx=15,
                        pady=(10, 2)
                    )

                    ctk.CTkLabel(
                        panel,
                        text=f"{cantidad} valores nulos  |  {porcentaje}%",
                        text_color="gray"
                    ).pack(
                        anchor="w",
                        padx=15
                    )

                    barra = ctk.CTkProgressBar(
                        panel,
                        height=12
                    )

                    barra.pack(
                        fill="x",
                        padx=15,
                        pady=(8, 12)
                    )

                    barra.set(porcentaje / 100)

            else:

                panel = self.crear_panel()

                ctk.CTkLabel(
                    panel,
                    text="No se encontraron valores nulos.",
                    text_color="#22c55e",
                    font=("Arial", 14, "bold")
                ).pack(padx=15, pady=20)

            # ------------------------------------------------
            # 4. ESTADÍSTICA DESCRIPTIVA
            # ------------------------------------------------

            self.crear_seccion(
                "Estadística descriptiva",
                "Resumen numérico de las variables cuantitativas."
            )

            if estadisticas:

                df_estadisticas = pd.DataFrame(
                    estadisticas
                ).T.round(2)

                df_estadisticas.index.name = "Variable"

                self.crear_tabla(
                    self.contenido,
                    df_estadisticas.reset_index(),
                    altura=min(12, max(4, len(df_estadisticas)))
                )

            else:

                panel = self.crear_panel()

                ctk.CTkLabel(
                    panel,
                    text="No hay columnas numéricas para calcular estadísticas.",
                    text_color="gray"
                ).pack(padx=15, pady=20)

        except Exception as error:

            messagebox.showerror(
                "Error en análisis exploratorio",
                str(error)
            )

    # ========================================================
    # LIMPIEZA DE DATOS
    # ========================================================

    def mostrar_limpieza(self):

        self.crear_encabezado(
            "Limpieza de datos",
            "Aplica técnicas para tratar valores ausentes y duplicados."
        )

        if not self.validar_archivo():
            return

        panel = self.crear_panel()

        self.crear_etiqueta(
            panel,
            "Selecciona el método de limpieza"
        )

        opciones = [
            "Eliminar filas con nulos",
            "Rellenar nulos con mediana",
            "Rellenar nulos con media",
            "Rellenar nulos con moda",
            "Eliminar duplicados"
        ]

        self.selector_limpieza = self.crear_selector(
            panel,
            opciones,
            opciones[0]
        )

        self.crear_boton(
            panel,
            "Ejecutar limpieza",
            self.ejecutar_limpieza
        )

        self.crear_seccion(
            "Comparación de datos",
            "Compara el conjunto original con el resultado procesado."
        )

        self.panel_limpieza = ctk.CTkFrame(
            self.contenido,
            fg_color="transparent"
        )

        self.panel_limpieza.pack(fill="x")

        self.mostrar_comparacion_limpieza()

    def mostrar_comparacion_limpieza(self):

        for widget in self.panel_limpieza.winfo_children():
            widget.destroy()

        if self.df is None or self.df_procesado is None:
            return

        comparacion = comparar_datos(
            self.df,
            self.df_procesado
        )

        dataframe = pd.DataFrame([
            {
                "Indicador": "Filas",
                "Original": comparacion["filas_originales"],
                "Procesado": comparacion["filas_finales"]
            },
            {
                "Indicador": "Columnas",
                "Original": comparacion["columnas_originales"],
                "Procesado": comparacion["columnas_finales"]
            },
            {
                "Indicador": "Valores nulos",
                "Original": comparacion["nulos_originales"],
                "Procesado": comparacion["nulos_finales"]
            },
            {
                "Indicador": "Duplicados",
                "Original": comparacion["duplicados_originales"],
                "Procesado": comparacion["duplicados_finales"]
            }
        ])

        self.crear_tabla(
            self.panel_limpieza,
            dataframe,
            altura=4
        )

        self.crear_boton(
            self.panel_limpieza,
            "Descargar datos procesados",
            self.exportar_datos
        )

    def ejecutar_limpieza(self):

        if not self.validar_archivo():
            return

        try:

            df = self.obtener_df()

            metodo = self.selector_limpieza.get()

            if metodo == "Eliminar filas con nulos":

                resultado = eliminar_filas_nulas(df)

            elif metodo == "Rellenar nulos con mediana":

                resultado = rellenar_nulos_mediana(df)

            elif metodo == "Rellenar nulos con media":

                resultado = rellenar_nulos_media(df)

            elif metodo == "Rellenar nulos con moda":

                resultado = rellenar_nulos_moda(df)

            elif metodo == "Eliminar duplicados":

                resultado = eliminar_duplicados(df)

            else:
                raise ValueError("Método de limpieza no válido.")

            self.df_procesado = resultado

            self.mostrar_comparacion_limpieza()

            messagebox.showinfo(
                "Limpieza completada",
                f"Se aplicó el método:\n{metodo}"
            )

        except Exception as error:

            messagebox.showerror(
                "Error de limpieza",
                str(error)
            )

    def exportar_datos(self):

        if self.df_procesado is None:
            return

        ruta = filedialog.asksaveasfilename(
            title="Guardar datos procesados",
            defaultextension=".csv",
            filetypes=[("Archivo CSV", "*.csv")]
        )

        if not ruta:
            return

        try:

            self.df_procesado.to_csv(
                ruta,
                index=False,
                encoding="utf-8-sig"
            )

            messagebox.showinfo(
                "Exportación exitosa",
                f"Archivo guardado en:\n{ruta}"
            )

        except Exception as error:

            messagebox.showerror(
                "Error al exportar",
                str(error)
            )

    # ========================================================
    # VISUALIZACIONES
    # ========================================================

    def mostrar_visualizaciones(self):

        self.crear_encabezado(
            "Visualizaciones",
            "Genera gráficas para explorar patrones y relaciones en los datos."
        )

        if not self.validar_archivo():
            return

        panel = self.crear_panel()

        opciones = [
            "Histograma",
            "Gráfico de barras",
            "Gráfico de dispersión",
            "Diagrama de caja",
            "Mapa de calor"
        ]

        self.crear_etiqueta(panel, "Tipo de visualización")

        self.selector_visualizacion = self.crear_selector(
            panel,
            opciones,
            opciones[0]
        )

        self.crear_etiqueta(panel, "Variable numérica")

        self.selector_variable = self.crear_selector(
            panel,
            self.columnas_numericas()
        )

        self.crear_etiqueta(panel, "Variable X / categoría")

        self.selector_x = self.crear_selector(
            panel,
            self.obtener_df().columns.tolist()
        )

        self.crear_etiqueta(panel, "Variable Y / valor")

        self.selector_y = self.crear_selector(
            panel,
            self.columnas_numericas()
        )

        self.crear_boton(
            panel,
            "Generar visualización",
            self.ejecutar_visualizacion
        )

    def ejecutar_visualizacion(self):

        try:

            df = self.obtener_df()

            tipo = self.selector_visualizacion.get()

            variable = self.selector_variable.get()
            x = self.selector_x.get()
            y = self.selector_y.get()

            fecha_anterior = 0

            carpeta = Path("resultados/graficas")
            carpeta.mkdir(parents=True, exist_ok=True)

            if tipo == "Histograma":

                if variable not in self.columnas_numericas():
                    raise ValueError("Selecciona una variable numérica válida.")

                funcion = crear_histograma
                argumentos = (df, variable)

            elif tipo == "Gráfico de barras":

                if x not in df.columns or y not in self.columnas_numericas():
                    raise ValueError("Selecciona una categoría y una variable numérica válidas.")

                funcion = crear_grafico_barras
                argumentos = (df, x, y)

            elif tipo == "Gráfico de dispersión":

                if x not in self.columnas_numericas() or y not in self.columnas_numericas():
                    raise ValueError("Selecciona dos variables numéricas.")

                funcion = crear_grafico_dispersion
                argumentos = (df, x, y)

            elif tipo == "Diagrama de caja":

                if variable not in self.columnas_numericas():
                    raise ValueError("Selecciona una variable numérica válida.")

                funcion = crear_boxplot
                argumentos = (df, variable)

            elif tipo == "Mapa de calor":

                funcion = crear_mapa_calor
                argumentos = (df,)

            else:
                raise ValueError("Tipo de gráfica no válido.")

            fecha_anterior = max(
                (archivo.stat().st_mtime for archivo in carpeta.glob("*.png")),
                default=0
            )

            funcion(*argumentos)

            self.mostrar_imagen_reciente(fecha_anterior)

        except Exception as error:

            messagebox.showerror(
                "Error al generar visualización",
                str(error)
            )

    # ========================================================
    # REGRESIÓN LINEAL
    # ========================================================

    def mostrar_regresion(self):

        self.crear_encabezado(
            "Regresión lineal",
            "Estudia la relación lineal entre dos variables numéricas."
        )

        if not self.validar_archivo():
            return

        columnas = self.columnas_numericas()

        panel = self.crear_panel()

        self.crear_etiqueta(
            panel,
            "Variable independiente (X)"
        )

        self.selector_regresion_x = self.crear_selector(
            panel,
            columnas
        )

        self.crear_etiqueta(
            panel,
            "Variable dependiente (Y)"
        )

        self.selector_regresion_y = self.crear_selector(
            panel,
            columnas
        )

        self.crear_boton(
            panel,
            "Ejecutar regresión",
            self.ejecutar_regresion
        )

    def ejecutar_regresion(self):

        try:

            df = self.obtener_df()

            x = self.selector_regresion_x.get()
            y = self.selector_regresion_y.get()

            if x not in self.columnas_numericas():
                raise ValueError("Selecciona una variable X numérica.")

            if y not in self.columnas_numericas():
                raise ValueError("Selecciona una variable Y numérica.")

            if x == y:
                raise ValueError("Las variables X e Y deben ser diferentes.")

            carpeta = Path("resultados/graficas")
            carpeta.mkdir(parents=True, exist_ok=True)

            fecha_anterior = max(
                (archivo.stat().st_mtime for archivo in carpeta.glob("*.png")),
                default=0
            )

            resultado = regresion_lineal(
                df,
                x,
                y
            )

            self.crear_seccion("Resultados de la regresión")

            if isinstance(resultado, dict):

                datos = {
                    clave: valor
                    for clave, valor in resultado.items()
                    if not isinstance(valor, (pd.DataFrame, pd.Series))
                }

                self.mostrar_resultado(
                    "\n".join(
                        f"{clave}: {valor}"
                        for clave, valor in datos.items()
                    )
                )

            self.mostrar_imagen_reciente(fecha_anterior)

        except Exception as error:

            messagebox.showerror(
                "Error en regresión",
                str(error)
            )

    # ========================================================
    # INTERPOLACIÓN
    # ========================================================

    def mostrar_interpolacion(self):

        self.crear_encabezado(
            "Interpolación lineal",
            "Estima valores faltantes utilizando los valores conocidos."
        )

        if not self.validar_archivo():
            return

        df = self.obtener_df()

        columnas_numericas = self.columnas_numericas()
        columnas = df.columns.tolist()

        panel = self.crear_panel()

        self.crear_etiqueta(
            panel,
            "Variable que se desea interpolar"
        )

        self.selector_interpolacion = self.crear_selector(
            panel,
            columnas_numericas
        )

        self.crear_etiqueta(
            panel,
            "Columna para ordenar (opcional)"
        )

        self.selector_orden = self.crear_selector(
            panel,
            ["(Sin ordenar)"] + columnas
        )

        self.crear_etiqueta(
            panel,
            "Columna para agrupar (opcional)"
        )

        self.selector_grupo = self.crear_selector(
            panel,
            ["(Sin agrupación)"] + columnas
        )

        self.crear_boton(
            panel,
            "Ejecutar interpolación",
            self.ejecutar_interpolacion
        )

    def ejecutar_interpolacion(self):

        try:

            df = self.obtener_df()

            columna = self.selector_interpolacion.get()
            orden = self.selector_orden.get()
            grupo = self.selector_grupo.get()

            if columna not in self.columnas_numericas():
                raise ValueError("Selecciona una columna numérica válida.")

            columna_orden = None if orden == "(Sin ordenar)" else orden
            columnas_grupo = None if grupo == "(Sin agrupación)" else [grupo]

            resultado = interpolacion_lineal(
                df,
                columna,
                columna_orden,
                columnas_grupo
            )

            comparacion = comparar_interpolacion(
                df,
                resultado,
                columna
            )

            self.df_procesado = resultado

            self.crear_seccion("Resultados de interpolación")

            self.mostrar_resultado(
                "\n".join(
                    f"{clave}: {valor}"
                    for clave, valor in comparacion.items()
                )
            )

            self.crear_seccion("Vista previa de los datos interpolados")

            self.crear_tabla(
                self.contenido,
                resultado.head(20),
                altura=10
            )

            self.crear_boton(
                self.contenido,
                "Descargar datos procesados",
                self.exportar_datos
            )

        except Exception as error:

            messagebox.showerror(
                "Error de interpolación",
                str(error)
            )

    # ========================================================
    # CLUSTERING JERÁRQUICO
    # ========================================================

    def mostrar_clustering(self):

        self.crear_encabezado(
            "Clustering jerárquico",
            "Agrupa observaciones según sus similitudes en variables numéricas."
        )

        if not self.validar_archivo():
            return

        columnas = self.columnas_numericas()

        panel = self.crear_panel()

        self.crear_etiqueta(
            panel,
            "Selecciona las variables para agrupar"
        )

        self.checkboxes_clustering = {}

        for columna in columnas:

            variable = ctk.BooleanVar(value=False)

            checkbox = ctk.CTkCheckBox(
                panel,
                text=columna,
                variable=variable
            )

            checkbox.pack(
                anchor="w",
                padx=20,
                pady=5
            )

            self.checkboxes_clustering[columna] = variable

        self.crear_etiqueta(
            panel,
            "Cantidad de grupos"
        )

        self.entrada_clusters = self.crear_entrada(
            panel,
            valor="3",
            placeholder="Número de grupos"
        )

        self.crear_etiqueta(
            panel,
            "Método de agrupamiento"
        )

        self.selector_metodo = self.crear_selector(
            panel,
            ["ward", "complete", "average", "single"],
            "ward"
        )

        self.crear_boton(
            panel,
            "Ejecutar clustering",
            self.ejecutar_clustering
        )

    def ejecutar_clustering(self):

        try:

            df = self.obtener_df()

            columnas = [
                columna
                for columna, variable in self.checkboxes_clustering.items()
                if variable.get()
            ]

            if not columnas:
                raise ValueError("Selecciona al menos una variable.")

            try:
                n_clusters = int(self.entrada_clusters.get())
            except ValueError:
                raise ValueError("La cantidad de grupos debe ser un entero.")

            metodo = self.selector_metodo.get()

            carpeta = Path("resultados/graficas")
            carpeta.mkdir(parents=True, exist_ok=True)

            fecha_anterior = max(
                (archivo.stat().st_mtime for archivo in carpeta.glob("*.png")),
                default=0
            )

            resultado = clustering_jerarquico(
                df,
                columnas,
                n_clusters,
                metodo
            )

            self.df_procesado = resultado["dataframe"]

            self.crear_seccion("Resultados del clustering")

            datos = {
                "Variables utilizadas": ", ".join(resultado["columnas_utilizadas"]),
                "Observaciones agrupadas": resultado["observaciones_agrupadas"],
                "Observaciones excluidas": resultado["observaciones_excluidas"],
                "Cantidad de grupos": resultado["cantidad_clusters"],
                "Método": resultado["metodo"]
            }

            self.mostrar_resultado(
                "\n".join(
                    f"{clave}: {valor}"
                    for clave, valor in datos.items()
                )
            )

            self.crear_seccion("Distribución de grupos")

            distribucion = pd.DataFrame(
                list(resultado["distribucion_clusters"].items()),
                columns=["Grupo", "Cantidad de observaciones"]
            )

            self.crear_tabla(
                self.contenido,
                distribucion,
                altura=5
            )

            self.mostrar_imagen_reciente(fecha_anterior)

            self.crear_boton(
                self.contenido,
                "Descargar datos con grupos",
                self.exportar_datos
            )

        except Exception as error:

            messagebox.showerror(
                "Error en clustering",
                str(error)
            )
