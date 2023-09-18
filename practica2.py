import tkinter as tk

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
    print(len(coordenadas))

    # Obtener el tamaño del punto como cadena
    tamanio_str = entry_tamanio.get()

    # Verificar si la cadena tiene un valor válido
    if tamanio_str:
        tamanio = float(tamanio_str)
    else:
        tamanio = 1.0  # Valor predeterminado en caso de que no haya un tamaño válido

    color = color_var.get()
    canvas.create_oval(x - tamanio, y - tamanio, x + tamanio, y + tamanio, fill=color, outline=color)
    
    # Crear una etiqueta para mostrar las coordenadas
    coordenadas_text = tk.StringVar()

    # en caso de que sea la primera vez que se impriman las coordenadas tendrá el indicador de las coordenadas
    if len(coordenadas) < 2:
        coords_str = "coordenadas:" + str(x - 300) + "," + str(-(y - 300))
    else:
        coords_str = str(x - 300) + "," + str(-(y - 300))

    coordenadas_text.set(coords_str)
    coordenadas_label = tk.Label(frame, textvariable=coordenadas_text)
    coordenadas_label.pack()


        
def dibujar_linea_bresenham():
    
        if len(coordenadas) >= 2:

            lineas.append(len(coordenadas) - 1)

            punto1=coordenadas[len(coordenadas) - 1]
            punto2=coordenadas[len(coordenadas) - 2]

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
        
            
    

def bresenham_algotithm_low(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    yi = 1

    if dy < 0:
        yi = -1
        dy = -dy

    D = (2*dy) - dx
    y = y1

    for x in range(x1, x2):
        tamanio = float(canvas.itemcget(lapiz, "width"))
        color = canvas.itemcget(lapiz, "fill")

        canvas.create_oval(x - tamanio, y - tamanio, x + tamanio, y + tamanio, fill=color, outline=color)

        if D > 0:
            y = y + yi
            D = D + (2*dy) - (2*dx)
        else:
            D = D + 2*dy

def bresenham_algotithm_high(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    xi = 1

    if dx < 0:
        xi = -1
        dx = -dx

    D = (2*dx) - dy
    x = x1

    for y in range(y1, y2):
        tamanio = float(canvas.itemcget(lapiz, "width"))
        color = canvas.itemcget(lapiz, "fill")

        canvas.create_oval(x - tamanio, y - tamanio, x + tamanio, y + tamanio, fill=color, outline=color)

        if D > 0:
            x = x + xi
            D = D + (2*dx) - (2*dy)
        else:
            D = D + 2*dx



def traslation():
    canvas.delete("all")

    # Ejes del canvas
    canvas.create_line(300, 0, 300, 600, fill="black", width=2)
    canvas.create_line(0, 300, 600, 300, fill="black", width=2)

    # Importar las coordenadas de la traslación
    desp_x = int(entry_trasl_x.get())
    desp_y = int(entry_trasl_y.get())

    # Obtener el tamaño del punto como cadena
    tamanio_str = canvas.itemcget(lapiz, "width")

    # Verificar si la cadena tiene un valor válido
    if tamanio_str:
        tamanio = float(tamanio_str)
    else:
        tamanio = 1.0  # Valor predeterminado en caso de que no haya un tamaño válido

    color = canvas.itemcget(lapiz, "fill")

    for i in range(len(coordenadas)):
        punto = coordenadas[i]
        x = punto[0]
        y = punto[1]
        x += desp_x
        y += desp_y
        canvas.create_oval(x - tamanio, y - tamanio, x + tamanio, y + tamanio, fill=color, outline=color)

    for j in range(len(lineas)):
        punto1 = coordenadas[lineas[j]]
        punto2 = coordenadas[lineas[j] - 1]
        x1 = punto1[0]
        x2 = punto2[0]
        y1 = punto1[1]
        y2 = punto2[1]

        if abs(y2 - y1) < abs(x2 - x1):
            if x1 > x2:
                bresenham_algotithm_low(x2, y2, x1, y1)
            else:
                bresenham_algotithm_low(x1, y1, x2, y2)
        else:
            if y1 > y2:
                bresenham_algotithm_high(x2, y2, x1, y1)
            else:
                bresenham_algotithm_high(x1, y1, x2, y2)



def metodo_vacio():
    print("Hola mundo")


# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación de Dibujo")

# Crear el Canvas para dibujar
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack(side=tk.LEFT, padx=10, pady=10)

#ejes del canvas
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
