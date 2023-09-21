import tkinter as tk

from practica1 import *

# Variables globales
coordenadas = []
# array que indica donde están las líneas
lineas = []




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

    if canvas.itemcget(lapiz,"width")=="":
        tamanio = 2.0
    else:
        tamanio = float(canvas.itemcget(lapiz, "width"))

    color = canvas.itemcget(lapiz, "fill")
    canvas.create_rectangle(x - tamanio, y - tamanio, x + tamanio, y + tamanio, fill=color, outline=color)
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




def traslation():
    #este metodo trasladará los puntos que se encuentren en el array de coordenadas en funcion de las entradas de traslacion en x y en y
    #se debe de verificar que el array de coordenadas no este vacio
    
    if True:
        print("hola")

    if len(coordenadas) <= 0:
        return -1
    
    #se obtienen los valores de traslacion en x y en y
    trasl_x = int(entry_trasl_x.get())
    trasl_y = int(entry_trasl_y.get())

    #se recorre el array de coordenadas y se trasladan los puntos
    for i in range(len(coordenadas)):
        coordenadas[i][0] = coordenadas[i][0] + trasl_x
        coordenadas[i][1] = coordenadas[i][1] + trasl_y

    #se limpia el canvas
    canvas.delete("all")

    #se dibujan los ejes
    canvas.create_line(300,0,300,600,fill="black", width=1)
    canvas.create_line(0,300,600,300,fill="black", width=1)

    #se dibujan los puntos
    for i in range(len(coordenadas)):
        x = coordenadas[i][0]
        y = coordenadas[i][1]

        if canvas.itemcget(lapiz,"width")=="":

            tamanio = 2.0 
        else:
            tamanio = float(canvas.itemcget(lapiz, "width"))
        color = canvas.itemcget(lapiz, "fill")

        canvas.create_rectangle(x - tamanio, y - tamanio, x + tamanio, y + tamanio, fill=color, outline=color)

    #se dibujan las lineas
    for i in range(len(lineas)):
        punto1=coordenadas[lineas[i]]
        punto2=coordenadas[lineas[i]-1]

        x1=punto1[0]
        x2=punto2[0]
        y1=punto1[1]
        y2=punto2[1]

        if abs(y2-y1) < abs(x2-x1):
            if(x1>x2):
                bresenham_algotithm_low(x2, y2, x1, y1)
            else:
                bresenham_algotithm_low(x1, y1, x2, y2)
        else:
            if(y1>y2):
                bresenham_algotithm_high(x2, y2, x1, y1)
            else:
                bresenham_algotithm_high(x1, y1, x2, y2)

#metodo vacio para que no marque error

def metodo_vacio():
    print("Hola mundo")


# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación de Dibujo")

# Crear el Canvas para dibujar
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack(side=tk.LEFT, padx=10, pady=10)

#ejes del canvas
canvas.create_line(300,0,300,600,fill="black", width=1)
canvas.create_line(0,300,600,300,fill="black", width=1)

# Crear el lápiz (inicialmente negro)
lapiz = canvas.create_rectangle(0, 0, 0, 0, fill="black", width=1.0)

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

#Boton de dibujo de linea
btn_bresenham = tk.Button(frame, text="Bresenham", command=dibujar_linea_bresenham)
btn_bresenham.pack()


#botones con funciones de traslaciones

#Traslacion
btn_trasl = tk.Button(frame, text="Traslación", command=traslation)
btn_trasl.pack()

label_trasl_x = tk.Label(frame, text="Traslación en x")
label_trasl_x.pack()
entry_trasl_x = tk.Entry(frame)
entry_trasl_x.pack()

label_trasl_y = tk.Label(frame, text="Traslación en y")
label_trasl_y.pack()
entry_trasl_y = tk.Entry(frame)
entry_trasl_y.pack()

#Rotacion
btn_rot = tk.Button(frame, text="Rotación", command=metodo_vacio)
btn_rot.pack()

label_rot_alfa= tk.Label(frame, text="alfa:")
label_rot_alfa.pack()
entry_rot_alfa = tk.Entry(frame)
entry_rot_alfa.pack()


#Escalado
btn_esc = tk.Button(frame, text="Escalado", command=metodo_vacio)
btn_esc.pack()

label_esc_x = tk.Label(frame, text="Traslación en x")
label_esc_x.pack()
entry_esc_x = tk.Entry(frame)
entry_esc_x.pack()

label_esc_y = tk.Label(frame, text="Traslación en y")
label_esc_y.pack()
entry_esc_y = tk.Entry(frame)
entry_esc_y.pack()


# Ejecutar la aplicación
root.mainloop()
