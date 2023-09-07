import tkinter as tk
import pandas as pd 
import numpy as np


# Función para cambiar el tamaño de los puntos en el Canvas
def cambiar_tamanio_punto():
    nuevo_tamanio = float(entry_tamanio.get())
    canvas.itemconfig(lapiz, width=nuevo_tamanio)

# Función para cambiar el color de los puntos en el Canvas
def cambiar_color_punto():
    nuevo_color = color_var.get()
    canvas.itemconfig(lapiz, fill=nuevo_color)

# Función para dibujar en el Canvas cuando se hace clic en él
def dibujar(event):
    global numeroPuntos  # Declarar la variable global
    x, y = event.x, event.y
    # Para dibujar las líneas
    coordenadas.append([x, y])
    numeroPuntos += 1

    tamanio = float(canvas.itemcget(lapiz, "width"))
    color = canvas.itemcget(lapiz, "fill")
    canvas.create_oval(x - tamanio, y - tamanio, x + tamanio, y + tamanio, fill=color, outline=color)

# Función para dibujar líneas en el Canvas
def dibujar_linea():

    if numeroPuntos >= 2:
        tamanio = float(canvas.itemcget(lapiz, "width"))
        color = canvas.itemcget(lapiz, "fill")
        
        canvas.create_line(coordenadas[numeroPuntos - 1][0], coordenadas[numeroPuntos - 1][1],
                           coordenadas[numeroPuntos - 0][0], coordenadas[numeroPuntos - 0][1], fill=color, outline=color)

# Variables globales
coordenadas = []
numeroPuntos = 0

# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación de Dibujo")

# Crear el Canvas para dibujar
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack(side=tk.LEFT, padx=10, pady=10)

# Crear el lápiz (inicialmente negro)
lapiz = canvas.create_oval(0, 0, 5, 5, fill="black")

# Configurar eventos de dibujo en el Canvas
canvas.bind("<Button-1>", dibujar)

# Crear un marco para los botones
frame = tk.Frame(root)
frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Crear una entrada para cambiar el tamaño del punto
label_tamanio = tk.Label(frame, text="Tamaño del punto:")
label_tamanio.pack()
entry_tamanio = tk.Entry(frame)
entry_tamanio.pack()
btn_cambiar_tamanio = tk.Button(frame, text="Cambiar Tamaño", command=cambiar_tamanio_punto)
btn_cambiar_tamanio.pack()

# Crear una lista de opciones de colores
colores = ["black", "red", "green", "blue", "orange", "purple", "pink"]
color_var = tk.StringVar(value="black")

# Crear una etiqueta y un menú desplegable para cambiar el color del punto
label_color = tk.Label(frame, text="Color del punto:")
label_color.pack()
menu_color = tk.OptionMenu(frame, color_var, *colores)
menu_color.pack()
btn_cambiar_color = tk.Button(frame, text="Cambiar Color", command=cambiar_color_punto)
btn_cambiar_color.pack()

# Crear un botón para dibujar líneas
btn_dibujar_linea = tk.Button(frame, text="Dibujar Línea", command=dibujar_linea)
btn_dibujar_linea.pack()

# Ejecutar la aplicación
root.mainloop()
