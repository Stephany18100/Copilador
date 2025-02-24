import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import re

# Expresiones regulares para validar la sintaxis del lenguaje
patrones = {
    "Variable": r'@\s*(\w+)\s*=\s*(?:(int|float|"str")\s*;[\s\n]*|(?:"[^"\d]*[^\d"]*"|(?<!")\d+(?:\.\d+)?(?!"));)',  # oki

    "Lectura":  r'^\?->\s*(\w+|".*");$', #oki

    "Impresion":  r'^! \s*(?:"[^"]*"|\w+)(?:\s*\+\s*(?:"[^"]*"|\w+))*;$', #oki

    "Condicional IF": r'^\?->\s*(\w+)\s*(>=|<=|==|!=|<|>)\s*(\d+|\w+)\s*->\s*"([^"]*)";\s*(?:else\s*->\s*"([^"]*)";)?$', #oki

    "Bucle FOR": r'^#\s*(\d+)\s*->\s*(\d+)\s*\{\s*!(.*)\s*\}\s*$', #oki

    "Bucle WHILE": r'^@ (\w+)\s*=\s*(\d+); \s*\* (.*) \s*\{ \s*! (.*); \s*@ (\w+)\s*=\s*(.*); \s*\}$', #oki
}

# Función para analizar el código y resaltar errores
def analizar_codigo():
    codigo = editor.get("1.0", tk.END).strip()
    errores = []

    # Limpiar resaltados previos
    limpiar_resaltados()

    lineas = codigo.split("\n")
    for i, linea in enumerate(lineas, start=1):
        linea = linea.strip()

        # Si la línea no está vacía y no coincide con ningún patrón válido, se considera error
        if linea and not any(re.fullmatch(patron, linea) for patron in patrones.values()):
            errores.append(f"Error en línea {i}: Sintaxis incorrecta - {linea}")
            resaltar_error(i)

    # Limpiar el área de resultados antes de mostrar nuevos mensajes
    area_resultados.config(state=tk.NORMAL)
    area_resultados.delete("1.0", tk.END)

    if errores:
        area_resultados.insert(tk.END, "Errores detectados:\n\n", "error")
        for error in errores:
            area_resultados.insert(tk.END, f"• {error}\n", "error")
    else:
        area_resultados.insert(tk.END, "✅ Análisis completado: No se encontraron errores.", "correcto")

    area_resultados.config(state=tk.DISABLED)

# Función para resaltar una línea con error en el editor
def resaltar_error(linea_numero):
    inicio = f"{linea_numero}.0"
    fin = f"{linea_numero}.end"
    editor.tag_add("error_line", inicio, fin)
    editor.tag_configure("error_line", background="#ff4d4d", foreground="white")

# Función para limpiar los resaltados previos
def limpiar_resaltados():
    editor.tag_remove("error_line", "1.0", tk.END)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Compilador Visual Pro")
root.geometry("950x750")
root.configure(bg="#1e1e2f")  # Fondo oscuro moderno

# Paleta de colores
COLOR_FONDO = "#1e1e2f"
COLOR_TEXTO = "#ffffff"
COLOR_BOTONES = "#6c5ce7"
COLOR_EXITO = "#2ecc71"
COLOR_ERROR = "#e74c3c"
COLOR_MARCOS = "#27273f"
COLOR_LINEA_ERROR = "#ff4d4d"

# Estilos globales
fuente_titulo = ("Segoe UI", 16, "bold")
fuente_principal = ("Consolas", 12)  # Fuente monoespaciada para el editor
fuente_botones = ("Segoe UI", 10, "bold")

# Marco principal
main_frame = tk.Frame(root, bg=COLOR_FONDO)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Título
titulo = tk.Label(main_frame, text="Compilador", font=fuente_titulo, bg=COLOR_FONDO, fg=COLOR_TEXTO)
titulo.pack(pady=(0, 15))

# Editor de código
editor_frame = tk.Frame(main_frame, bg=COLOR_MARCOS, bd=0, relief=tk.FLAT)
editor_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

editor_label = tk.Label(editor_frame, text="Editor de Código", font=fuente_principal, bg=COLOR_MARCOS, fg=COLOR_TEXTO)
editor_label.pack(pady=(10, 0), padx=10, anchor="w")

editor = scrolledtext.ScrolledText(
    editor_frame,
    width=80,
    height=15,
    font=fuente_principal,
    bg="#2d2d3d",
    fg=COLOR_TEXTO,
    insertbackground=COLOR_TEXTO,  # Cursor de texto
    bd=0,
    highlightthickness=0,
    wrap=tk.NONE
)
editor.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Botón de análisis
btn_analizar = tk.Button(
    main_frame,
    text="Analizar Código",
    command=analizar_codigo,
    font=fuente_botones,
    bg=COLOR_BOTONES,
    fg="white",
    activebackground="#5a4ac9",
    activeforeground="white",
    bd=0,
    padx=20,
    pady=10,
    cursor="hand2"
)
btn_analizar.pack(pady=(0, 15))

# Área de resultados
resultados_frame = tk.Frame(main_frame, bg=COLOR_MARCOS, bd=0, relief=tk.FLAT)
resultados_frame.pack(fill=tk.BOTH, expand=True)

area_resultados_label = tk.Label(
    resultados_frame,
    text="Resultados del Análisis",
    font=fuente_principal,
    bg=COLOR_MARCOS,
    fg=COLOR_TEXTO
)
area_resultados_label.pack(pady=(10, 0), padx=10, anchor="w")

area_resultados = scrolledtext.ScrolledText(
    resultados_frame,
    width=80,
    height=10,
    font=fuente_principal,
    bg="#2d2d3d",
    fg=COLOR_TEXTO,
    bd=0,
    highlightthickness=0,
    state=tk.DISABLED
)
area_resultados.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Configuración de tags para el área de resultados
area_resultados.tag_configure("error", foreground=COLOR_ERROR, font=("Consolas", 12, "bold"))
area_resultados.tag_configure("correcto", foreground=COLOR_EXITO, font=("Consolas", 12, "bold"))

# Ejecutar la aplicación
root.mainloop()
