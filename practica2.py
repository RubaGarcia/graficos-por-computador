import tkinter as tk
import math
import random
import numpy as np
from PIL import Image
from PIL import ImageDraw


# Variables globales
coordenadas = []
coordenadas_traducidas = []
# array que indica donde están las líneas
puntos = None
lineas = []

TAM_PIXEL=6
CANVAS_WIDTH=600

'''
# Función para cambiar el tamaño de los puntos en el Canvas
def cambiar_tamanio_punto():
    nuevo_tamanio = float(entry_tamanio.get())
    canvas.itemconfig(lapiz, width=nuevo_tamanio)
'''
# Función para cambiar el color de los puntos en el Canvas
def cambiar_color_punto():
    nuevo_color = color_var.get()
    canvas.itemconfig(lapiz, fill=nuevo_color)

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

def dibujar(event):
    x, y = event.x, event.y
    # Para dibujar las líneas

    x, y = pseudopuntos(x,y)


    coordenadas.append([x,y])
    global puntos
    if puntos is None:
        unos = np.ones(3)
        puntos = np.c_[unos,[x,y,1]]
        puntos = np.delete(puntos, 0, 1)  
    elif puntos is not None:
        puntos = np.c_[puntos,[x,y,1]]
        
    #print(puntos)
    #print(len(puntos))
    #print (len(puntos[0]))


        
    color = canvas.itemcget(lapiz, "fill")
    realx,realy=undo_pseudopuntos(x,y)
    canvas.create_rectangle(realx , realy , realx + TAM_PIXEL, realy + TAM_PIXEL, fill=color, outline=color)

def dibujar_linea_bresenham():
    
        if len(coordenadas) >= 2:

            lineas.append(len(coordenadas) - 1)

            punto1=coordenadas[len(coordenadas) - 1]
            punto2=coordenadas[len(coordenadas) - 2]

            x1=punto1[0]
            x2=punto2[0]
            y1=punto1[1]
            y2=punto2[1]

            
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)           

            if dx>=dy:
                dibujar_punto(bresenham_algorithm(x1, y1, x2, y2))
            else:
                List = bresenham_algorithm(y1, x1, y2, x2)
                ListaDibujo = []
                for punto in List:
                    ListaDibujo.append([punto[1],punto[0]])

                dibujar_punto(ListaDibujo)

def dibujar_linea_bresenham_input(index):
    punto1 = coordenadas[index]
    punto2 = coordenadas[index-1]

    x1 = punto1[0]
    x2 = punto2[0]
    y1 = punto1[1]
    y2 = punto2[1]

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    if dx >= dy:
        dibujar_punto(bresenham_algorithm(x1, y1, x2, y2))
    else:
        List = bresenham_algorithm(y1, x1, y2, x2)
        ListaDibujo = []
        for punto in List:
            ListaDibujo.append([punto[1], punto[0]])

        dibujar_punto(ListaDibujo)

def bresenham_algorithm(x1, y1, x2, y2):
    dx = int(abs(x2 - x1))
    dy = int(abs(y2 - y1))
    

    
    def signo(x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        else:
            return 0

    sx = signo(x2-x1)
    sy = signo(y2-y1)


    ne = 2 * dy -dx

    L = []

    for num in range(dx + 1):
        
            
        L.append([x1,y1])

        while ne >= 0:
            y1 = y1 + 1 * sy
            ne = ne - 2 * dx
        x1 = x1 + 1 * sx
        ne = ne + 2 * dy
    
    return L

def dibujar_punto(Lista):
    
    color = canvas.itemcget(lapiz, "fill")
    for punto in Lista:
        x,y = undo_pseudopuntos(punto[0],punto[1])
        canvas.create_rectangle(x, y, x + TAM_PIXEL, y + TAM_PIXEL, fill=color, outline=color)

def traslation():
    #este metodo trasladará los puntos que se encuentren en el array de coordenadas en funcion de las entradas de traslacion en x y en y
    #se debe de verificar que el array de coordenadas no este vacio
    global puntos
    
    print("traslation algorithm")

    if len(coordenadas) <= 0:
        print("no hay coordenadas")
        return -1
    
    
    #se obtienen los valores de traslacion en x y en y
    trasl_x = int(entry_trasl_x.get())
    trasl_y = int(entry_trasl_y.get())
    
    #array bidimensional con las coordenadas y una fila extra de todo ceroy el ultimo valor un 1

    id = np.identity(3)
    id[0][2] = trasl_x
    id[1][2] = trasl_y


    result_matrix = id@puntos
    
    result_matrix.astype(int)
    

    puntos = result_matrix
    for i in range(len(puntos[0])):
        coordenadas[i] = [result_matrix[0][i],result_matrix[1][i]]
        print(coordenadas[i])
    
    flush_canvas()

    dibujar_punto(coordenadas)
   
    for i in range(len(lineas)):
        print(lineas[i])
        dibujar_linea_bresenham_input(lineas[i])

def metodo_vacio():
    print("Hola mundo")

def rot_function():
    print("rot_function")
    coordenadas = rotacion()

def rotacion():
    #funcion que toma los puntos del array de coordenadas y los rota en funcion de la entrada de rotacion.
    #se rotan los elementos en funcion del centro del canvas
    #se debe de verificar que el array de coordenadas no este vacio
    

    print("rotation algorithm")


    if len(coordenadas) < 1:
        
        print("no hay coordenadas")
        return -1
    
    #se obtiene el valor de rotacion
    rot_alfa = int(entry_rot_alfa.get())
    rot_alfa = math.radians(rot_alfa)
    print(rot_alfa)
    #se recorre el array de coordenadas y se rota cada punto


    id=np.identity(3)
    id[0][0]=math.cos(rot_alfa)
    id[0][1]=-(math.sin(rot_alfa))
    id[1][0]=math.sin(rot_alfa)
    id[1][1]=math.cos(rot_alfa)

    global puntos
    result_matrix = id@puntos

    result_matrix.astype(int)

    puntos = result_matrix

    for i in range(len(puntos[0])):
        coordenadas[i] = [result_matrix[0][i],result_matrix[1][i]]
        print(coordenadas[i])
    
    flush_canvas()

    dibujar_punto(coordenadas)
   
    for i in range(len(lineas)):
        print(lineas[i])
        dibujar_linea_bresenham_input(lineas[i])

def rotacion_g(grados):
    #funcion que toma los puntos del array de coordenadas y los rota en funcion de la entrada de rotacion.
    #se rotan los elementos en funcion del centro del canvas
    #se debe de verificar que el array de coordenadas no este vacio


    print("rotation algorithm")


    if len(coordenadas) < 1:
        
        print("no hay coordenadas")
        return -1
    
    #se obtiene el valor de rotacion
    rot_alfa = grados
    rot_alfa = math.radians(rot_alfa)
    print(rot_alfa)
    #se recorre el array de coordenadas y se rota cada punto


    id=np.identity(3)
    id[0][0]=math.cos(rot_alfa)
    id[0][1]=-(math.sin(rot_alfa))
    id[1][0]=math.sin(rot_alfa)
    id[1][1]=math.cos(rot_alfa)

    global puntos
    result_matrix = id@puntos

    result_matrix.astype(int)

    puntos = result_matrix

    for i in range(len(puntos[0])):
        coordenadas[i] = [result_matrix[0][i],result_matrix[1][i]]
        print(coordenadas[i])
    
    flush_canvas()

    dibujar_punto(coordenadas)
   
    for i in range(len(lineas)):
        print(lineas[i])
        dibujar_linea_bresenham_input(lineas[i])

def escalado():
    #funcion que toma los puntos del array de coordenadas y los escala en funcion de las entradas de escalado en x y en y.
    #se debe de verificar que el array de coordenadas no este vacio
    if len(coordenadas) <= 0:
        return -1
    
    #se obtienen los valores de escalado en x y en y
    esc_x = float(entry_esc_x.get())
    esc_y = float(entry_esc_y.get())
    
    id = np.identity(3)
    id[0][0] = esc_x
    id[1][1] = esc_y

    global puntos
    result_matrix = id@puntos

    result_matrix.astype(int)

    puntos = result_matrix

    for i in range(len(puntos[0])):
        coordenadas[i] = [result_matrix[0][i],result_matrix[1][i]]
        print(coordenadas[i])
    
    flush_canvas()

    dibujar_punto(coordenadas)
   
    for i in range(len(lineas)):
        print(lineas[i])
        dibujar_linea_bresenham_input(lineas[i])
  
def flush_canvas():
    canvas.create_rectangle(0, 0, 600, 600, fill="white", outline="white")
    canvas.create_line(300,0,300,600,fill="black", width=1)
    canvas.create_line(0,300,600,300,fill="black", width=1)

def shearing():
    #funcion que toma los puntos del array de coordenadas y los cizalla en funcion de las entradas de cizalla en x y en y.
    #se debe de verificar que el array de coordenadas no este vacio
    if len(coordenadas) <= 0:
        return -1
    
    #se obtienen los valores de escalado en x y en y
    ciz_x = float(entry_ciz_x.get())
    ciz_y = float(entry_ciz_y.get())
    
    id = np.identity(3)
    id[0][1] = ciz_x
    id[1][0] = ciz_y

    global puntos
    result_matrix = id@puntos

    result_matrix.astype(int)

    puntos = result_matrix

    for i in range(len(puntos[0])):
        coordenadas[i] = [result_matrix[0][i],result_matrix[1][i]]
        print(coordenadas[i])
    
    flush_canvas()

    dibujar_punto(coordenadas)
   
    for i in range(len(lineas)):
        print(lineas[i])
        dibujar_linea_bresenham_input(lineas[i])
       
def reflexion_x():
    #funcion que toma los puntos del array de coordenadas y los refleja en funcion de la entrada de reflexion en x.
    #se debe de verificar que el array de coordenadas no este vacio
    if len(coordenadas) <= 0:
        return -1
    
    
    id = np.identity(3)
    id[1][1] = -1


    global puntos
    result_matrix = id@puntos

    result_matrix.astype(int)

    puntos = result_matrix

    for i in range(len(puntos[0])):
        coordenadas[i] = [result_matrix[0][i],result_matrix[1][i]]
        print(coordenadas[i])
    
    flush_canvas()

    dibujar_punto(coordenadas)
   
    for i in range(len(lineas)):
        print(lineas[i])
        dibujar_linea_bresenham_input(lineas[i])

def reflexion_y():
    #funcion que toma los puntos del array de coordenadas y los refleja en funcion de la entrada de reflexion en y.
    #se debe de verificar que el array de coordenadas no este vacio
    if len(coordenadas) <= 0:
        return -1
    
    
    id = np.identity(3)
    id[0][0] = -1
    global puntos
    result_matrix = id@puntos

    result_matrix.astype(int)
    
    puntos = result_matrix

    for i in range(len(puntos[0])):
        coordenadas[i] = [result_matrix[0][i],result_matrix[1][i]]
        print(coordenadas[i])
    
    flush_canvas()

    dibujar_punto(coordenadas)
   
    for i in range(len(lineas)):
        print(lineas[i])
        dibujar_linea_bresenham_input(lineas[i])

def reflexion_45():
    rotacion_g(45)
    reflexion_x()
    rotacion_g(-45)


def save_image():
    image = Image.new("RGB", (CANVAS_WIDTH, CANVAS_WIDTH), "white")
    draw = ImageDraw.Draw(image)

    writing_list = puntos.astype(int)

    print(writing_list)
    for i in range(len(coordenadas)):
        x = writing_list[0][i] * TAM_PIXEL + (CANVAS_WIDTH // 2)
        y = writing_list[1][i] * TAM_PIXEL + (CANVAS_WIDTH // 2)
        color = canvas.itemcget(lapiz, "fill")
        draw.rectangle((x, y, x + TAM_PIXEL, y + TAM_PIXEL), fill=color, outline=color)

    for i in range(len(lineas)-1):
        lista_dibujar = []
        
        color_linea = color
        print(writing_list)
        print(writing_list[0])
        elem1 = (writing_list[0][lineas[i]], writing_list[1][lineas[i]])
        elem2 = (writing_list[0][lineas[i + 1]], writing_list[1][lineas[i + 1]])

        dx = abs(elem2[0] - elem1[0])
        dy = abs(elem2[1] - elem1[1])
        x1 = elem1[0]
        y1 = elem1[1]
        x2 = elem2[0]
        y2 = elem2[1]


        if (dx >= dy):
            lista_dibujar = bresenham_algorithm(x1, y1, x2, y2) 
        else:
            lista_aux = bresenham_algorithm(y1, x1, y2, x2)
            for pixel in lista_aux:
                lista_dibujar.append((pixel[1], pixel[0]))

        for pixel in lista_dibujar:
            drawingX = pixel[0] * TAM_PIXEL + (CANVAS_WIDTH // 2)
            drawingY = pixel[1] * TAM_PIXEL + (CANVAS_WIDTH // 2)
            draw.rectangle((drawingX, drawingY, drawingX + TAM_PIXEL, drawingY + TAM_PIXEL), fill=color_linea)


    nombre = nombre_archivo.get()
    
    # Verificar si la cadena de nombre tiene una extensión
    if not nombre.endswith(('.png', '.jpg', '.jpeg', '.gif')):
        # Si no tiene una extensión, agregar ".png" por defecto
        nombre += ".png"

    try:
        image.save(nombre)
        print(f"Imagen guardada como {nombre}")
    except Exception as e:
        print(f"Error al guardar la imagen: {e}")

    image.save(nombre)
    
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
#label_tamanio = tk.Label(frame, text="Tamaño del punto:")
#label_tamanio.pack()
#entry_tamanio = tk.Entry(frame)
#entry_tamanio.pack()
#btn_cambiar_tamanio = tk.Button(frame, text="Cambiar Tamaño", command=cambiar_tamanio_punto)
#btn_cambiar_tamanio.pack()

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


label_trasl_x = tk.Label(frame, text="Traslación en x")
label_trasl_x.pack()
entry_trasl_x = tk.Entry(frame)
entry_trasl_x.pack()

label_trasl_y = tk.Label(frame, text="Traslación en y")
label_trasl_y.pack()
entry_trasl_y = tk.Entry(frame)
entry_trasl_y.pack()

btn_trasl = tk.Button(frame, text="Traslación", command=traslation)
btn_trasl.pack()

#Rotacion

label_rot_alfa= tk.Label(frame, text="alfa:")
label_rot_alfa.pack()
entry_rot_alfa = tk.Entry(frame)
entry_rot_alfa.pack()


btn_rot = tk.Button(frame, text="Rotación", command=rotacion)
btn_rot.pack()
#btn_rot_animation = tk.Button(frame, text="Rotación animada", command=rot_animation)
#btn_rot_animation.pack()


#Escalado
label_esc_x = tk.Label(frame, text="Escalado en x")
label_esc_x.pack()
entry_esc_x = tk.Entry(frame)
entry_esc_x.pack()

label_esc_y = tk.Label(frame, text="Escalado en y")
label_esc_y.pack()
entry_esc_y = tk.Entry(frame)
entry_esc_y.pack()


btn_esc = tk.Button(frame, text="Escalado", command=escalado)
btn_esc.pack()



#cizalla
label_ciz_x = tk.Label(frame, text="Cizalla en x")
label_ciz_x.pack()
entry_ciz_x = tk.Entry(frame)   
entry_ciz_x.pack()

label_ciz_y = tk.Label(frame, text="Cizalla en y")
label_ciz_y.pack()
entry_ciz_y = tk.Entry(frame)
entry_ciz_y.pack()

btn_ciz = tk.Button(frame, text="Cizalla", command=shearing)
btn_ciz.pack()

#reflexion
btn_reflexion_x = tk.Button(frame, text="Reflexion en x", command=reflexion_x)

btn_reflexion_x.pack()

btn_reflexion_y = tk.Button(frame, text="Reflexion en y", command=reflexion_y)
btn_reflexion_y.pack()

btn_reflexion_recta = tk.Button(frame, text="Reflexion en recta", command=reflexion_45)
btn_reflexion_recta.pack()

btn_save_image = tk.Button(frame, text="Guardar imagen", command=save_image)
label_nombre_archivo = tk.Label(frame, text="Nombre del archivo")
label_nombre_archivo.pack()
nombre_archivo = tk.Entry(frame)
nombre_archivo.pack()
btn_save_image.pack()

# Ejecutar la aplicación
root.mainloop()

