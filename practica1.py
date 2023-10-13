import tkinter as tk
import math

# Variables globales
coordenadas = []

TAM_PIXEL=3

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

    x, y = pseudopuntos(x,y)

    coordenadas.append([x, y])

    print(coordenadas)
    print (len(coordenadas))

    if canvas.itemcget(lapiz,"width")=="":
        tamanio = TAM_PIXEL
    else:
        tamanio = float(canvas.itemcget(lapiz, "width")) * TAM_PIXEL
        
    color = canvas.itemcget(lapiz, "fill")
    realx,realy=undo_pseudopuntos(x,y)
    canvas.create_rectangle(realx - tamanio, realy - tamanio, realx + tamanio, realy + tamanio, fill=color, outline=color)
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


def pseudopuntos(x,y):
    x = (x - (CANVAS_WIDTH // 2)) // TAM_PIXEL
    y = (y - (CANVAS_WIDTH // 2)) // TAM_PIXEL
    return x,y

def undo_pseudopuntos(x,y):
    x = (x * TAM_PIXEL) + (CANVAS_WIDTH // 2)
    y = (y * TAM_PIXEL) + (CANVAS_WIDTH // 2)
    return x,y

def dibujar_punto_linea(x1,y1, x2, y2):
    tamanio = float(canvas.itemcget(lapiz, "width"))
    color = canvas.itemcget(lapiz, "fill")
    
    canvas.create_rectangle(x1 - tamanio, y1 - tamanio, x1 + tamanio, y1 + tamanio, fill=color, outline=color)
    canvas.create_rectangle(x2 - tamanio, y2 - tamanio, x2 + tamanio, y2 + tamanio, fill=color, outline=color)
    canvas.create_line(x1, y1, x2, y2, fill=color, width=tamanio)
    

# Función para dibujar líneas en el Canvas
def dibujar_linea():

    if len(coordenadas) >= 2:
        tamanio = float(canvas.itemcget(lapiz, "width"))
        color = canvas.itemcget(lapiz, "fill")
        
        punto1=coordenadas[len(coordenadas) - 1]
        punto2=coordenadas[len(coordenadas) - 2]
        canvas.create_line(punto1[0], punto1[1], punto2[0], punto2[1], fill=color, width=tamanio)


def dibujar_linea_DDA():

    if len(coordenadas) >= 2:
        
        punto1=coordenadas[len(coordenadas) - 1]
        punto2=coordenadas[len(coordenadas) - 2]

        #punto1,punto2=undo_pseudopuntos(punto1[0], punto1[1]),undo_pseudopuntos(punto2[0], punto2[1])

        DDA_algorithm(punto1[0], punto1[1],punto2[0], punto2[1])


def DDA_algorithm(x1, y1, x2, y2):

    dx=x1-x2
    dy=y1-y2


    steps=max(abs(dx), abs(dy))

    xinc=dx/steps
    yinc=dy/steps

    x=x1+0.5
    y=y1+0.5

    if canvas.itemcget(lapiz,"width")=="":
        tamanio = TAM_PIXEL
    else:
        tamanio = float(canvas.itemcget(lapiz, "width")) * TAM_PIXEL

    color = canvas.itemcget(lapiz, "fill")

    for i in range(steps+1):

        xReal,yReal = undo_pseudopuntos(math.floor(x),math.floor(y))

        canvas.create_rectangle(xReal - tamanio, yReal - tamanio, xReal + tamanio, yReal + tamanio, fill=color, outline=color)

        x -= xinc
        y -= yinc
        


def dibujar_linea_bresenham():
    
        if len(coordenadas) >= 2:
            punto1=coordenadas[len(coordenadas) - 1]
            punto2=coordenadas[len(coordenadas) - 2]

            x1=punto1[0]
            x2=punto2[0]
            y1=punto1[1]
            y2=punto2[1]

            if canvas.itemcget(lapiz,"width")=="":
                tamanio = TAM_PIXEL
            else:
                tamanio = float(canvas.itemcget(lapiz, "width")) * TAM_PIXEL

                       

            bresenham_algorithm(x1, y1, x2, y2, tamanio)
            


def bresenham_algorithm(x1, y1, x2, y2, size):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    
    def signo(x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        else:
            return 0

    sx = signo(x2-x1)
    sy = signo(y2-y1)

    color = canvas.itemcget(lapiz, "fill")

    ne = 2 * dy -dx

    for num in range(dx + 1):
        x1Real,y1Real=undo_pseudopuntos(x1,y1)
            
        canvas.create_rectangle(x1Real , y1Real , x1Real + size, y1Real + size, fill=color, outline=color)

        while ne >= 0:
            y1 = y1 + 1 * sy
            ne = ne - 2 * dx
        x1 = x1 + 1 * sx
        ne = ne + 2 * dy

    '''
    if dx > dy:
        m = dy / dx
        e = m - size / dx
        while x1 != x2:
            #draw_point(x1, y1, size)
            x1Real,y1Real=undo_pseudopuntos(x1,y1)
            
            canvas.create_rectangle(x1Real - size, y1Real - size, x1Real + size, y1Real + size, fill=color, outline=color)
            if e >= 0:
                y1 += sy
                e -= 1
            x1 += sx
            e += m
    else:
        m = dx / dy
        e = m - size / dy
        while y1 != y2:
            x1Real,y1Real=undo_pseudopuntos(x1,y1)
            
            canvas.create_rectangle(x1Real - size, y1Real - size, x1Real + size, y1Real + size, fill=color, outline=color)
            if e >= 0:
                x1 += sx
                e -= 1
            y1 += sy
            e += m
    x1Real,y1Real=undo_pseudopuntos(x1,y1)
            
    canvas.create_rectangle(x1Real - size, y1Real - size, x1Real + size, y1Real + size, fill=color, outline=color)
    '''

def flush_canvas():

    coordenadas = []
    canvas.create_rectangle(0, 0, 600, 600, fill="white", outline="white")
    canvas.create_line(300,0,300,600,fill="black", width=1)
    canvas.create_line(0,300,600,300,fill="black", width=1)
    



def dibujar_linea_slope_intercept():
    if len(coordenadas) >= 2:
        punto1=coordenadas[len(coordenadas) - 1]
        punto2=coordenadas[len(coordenadas) - 2]

        x1=punto1[0]
        x2=punto2[0]
        y1=punto1[1]
        y2=punto2[1]

        dx = x2 - x1
        dy = y2 - y1

        m = dy/dx

        b = y1 - m*x1

        if abs(y2-y1) < abs(x2-x1):
            if(x1>x2):
                slope_intercept_algorithm_low(x2, x1,  m, b)
            else:
                slope_intercept_algorithm_low(x1, x2,  m, b)
        else:
            if(y1>y2):
                slope_intercept_algorithm_high(y2, y1, m, b)
            else:
                slope_intercept_algorithm_high(y1, y2, m, b)

    

def slope_intercept_algorithm_low(x1, x2, m, b):
    x = x1
    while x < x2:
        y = m * x + b
        tamanio = float(canvas.itemcget(lapiz, "width")) * TAM_PIXEL
        color = canvas.itemcget(lapiz, "fill")

        canvas.create_rectangle(x - tamanio, y - tamanio, x + tamanio, y + tamanio, fill=color, outline=color)

        x += tamanio  # Incrementar x en cada iteración del bucle while

def slope_intercept_algorithm_high( y1, y2, m, b):
    y = y1
    while y < y2:
        x = (y - b) / m
        tamanio = float(canvas.itemcget(lapiz, "width")) * TAM_PIXEL
        color = canvas.itemcget(lapiz, "fill")

        canvas.create_rectangle(x - tamanio, y - tamanio, x + tamanio, y + tamanio, fill=color, outline=color)

        y += tamanio  # Incrementar y en cada iteración del bucle while
    
def metodo_vacio():
    print("Hola mundo")


# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación de Dibujo")



# Crear el Canvas para dibujar
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600

canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
canvas.pack(side=tk.LEFT, padx=10, pady=10)

#ejes del canvas
canvas.create_line(300,0,300,600,fill="black", width=1)
canvas.create_line(0,300,600,300,fill="black", width=1)


# Crear el lápiz (inicialmente negro)
lapiz = canvas.create_rectangle(0, 0, 0, 0, fill="black")

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


# Crear un botón para dibujar líneas
slope_intercept = tk.Button(frame, text="Slope Intercept", command=dibujar_linea_slope_intercept)
slope_intercept.pack()
# Crear un botón para dibujar líneas
btn_dda = tk.Button(frame, text="DDA", command=dibujar_linea_DDA)
btn_dda.pack()
# Crear un botón para dibujar líneas
btn_bresenham = tk.Button(frame, text="Bresenham", command=dibujar_linea_bresenham)
btn_bresenham.pack()
# Ejecutar la aplicación


btn_flush = tk.Button(frame, text="Flush", command=flush_canvas)
btn_flush.pack()


root.mainloop()
