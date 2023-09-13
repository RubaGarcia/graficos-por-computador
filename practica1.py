import tkinter as tk
import time

# Variables globales
coordenadas = []

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
    x, y = event.x, event.y
    # Para dibujar las líneas
    coordenadas.append([x, y])

    print(coordenadas)
    print (len(coordenadas))

    tamanio = float(canvas.itemcget(lapiz, "width"))
    color = canvas.itemcget(lapiz, "fill")
    canvas.create_oval(x - tamanio, y - tamanio, x + tamanio, y + tamanio, fill=color, outline=color)
    # Crear una etiqueta para mostrar las coordenadas
    coordenadas_text = tk.StringVar()

    #en caso de que sea la primera vez que se impriman las coordenadastendra el inidcador de las coordenadas
    if len(coordenadas) < 2:
        coords_str= "coordenadas:" +str(x-300)+","+str(-(y-300))
    else:
        coords_str=str(x-300)+","+str(-(y-300))

    coordenadas_text.set(coords_str)
    coordenadas_label = tk.Label(frame, textvariable=coordenadas_text)
    coordenadas_label.pack()

# Función para dibujar líneas en el Canvas
def dibujar_linea():

    if len(coordenadas) >= 2:
        tamanio = float(canvas.itemcget(lapiz, "width"))
        color = canvas.itemcget(lapiz, "fill")
        
        punto1=coordenadas[len(coordenadas) - 1]
        punto2=coordenadas[len(coordenadas) - 2]
        canvas.create_line(punto1[0], punto1[1], punto2[0], punto2[1], fill=color, width=tamanio)


def dibujar_linea_DDA():
    print("llamado a dibujar linea DDA")

    if len(coordenadas) >= 2:
        
        punto1=coordenadas[len(coordenadas) - 1]
        punto2=coordenadas[len(coordenadas) - 2]

        DDA_algorithm(punto1[0], punto1[1],punto2[0], punto2[1])


def DDA_algorithm(x1, y1, x2, y2):


    dx=x1-x2
    dy=y1-y2


    steps=max(dx, dy)

    xinc=dx/steps
    yinc=dy/steps

    x=float(x1)
    y=float(y1)

    

    for i in range(steps):
        tamanio = float(canvas.itemcget(lapiz, "width"))
        color = canvas.itemcget(lapiz, "fill")

        canvas.create_oval(x - tamanio, y - tamanio, x + tamanio, y + tamanio, fill=color, outline=color)

        x -= xinc
        y -= yinc
        




def metodo_vacio():
    print("Hola mundo")


# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación de Dibujo")

# Crear el Canvas para dibujar
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack(side=tk.LEFT, padx=10, pady=10)
canvas.create_line(300,0,300,600,fill="black", width=2)
canvas.create_line(0,300,600,300,fill="black", width=2)


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
btn_dibujar_linea = tk.Button(frame, text="Dibujar Línea normal", command=dibujar_linea)
btn_dibujar_linea.pack()

#TODO placeholders
# Crear un botón para dibujar líneas
btn_dibujar_linea_1 = tk.Button(frame, text="DDA algorithm", command=dibujar_linea_DDA)
btn_dibujar_linea_1.pack()
# Crear un botón para dibujar líneas
btn_dibujar_linea_2 = tk.Button(frame, text="slope intercept", command=metodo_vacio)
btn_dibujar_linea_2.pack()
# Crear un botón para dibujar líneas
btn_dibujar_linea_3 = tk.Button(frame, text="Bresenham", command=metodo_vacio)
btn_dibujar_linea_3.pack()
# Ejecutar la aplicación



root.mainloop()
