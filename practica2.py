import tkinter as tk
import math
import random
import numpy as np

# Variables globales
coordenadas = []
coordenadas_traducidas = []
# array que indica donde están las líneas
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
    canvas.create_rectangle(realx , realy , realx + tamanio, realy + tamanio, fill=color, outline=color)
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



def dibujar_linea_bresenham():
    
        if len(coordenadas) >= 2:

            lineas.append(len(coordenadas) - 1)

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

            



def bresenham_algorithm(x1, y1, x2, y2):
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



def traducir_coordenadas(x, y):
    x = x - 300
    y = (- y - 300)

    return [x, y]


def destraduccir_coordenadas(x, y):
    #pasar los ejes a coordenadas positivas de forma que entren en el canvas
    x = x + 300
    y = - y + 300

    return [x, y]


def traslation():
    #este metodo trasladará los puntos que se encuentren en el array de coordenadas en funcion de las entradas de traslacion en x y en y
    #se debe de verificar que el array de coordenadas no este vacio
   
    
    print("traslation algorithm")

    if len(coordenadas) <= 0:
        print("no hay coordenadas")
        return -1
    
    
    #se obtienen los valores de traslacion en x y en y
    trasl_x = int(entry_trasl_x.get())
    trasl_y = int(entry_trasl_y.get())
    

    trasl_matrix=[trasl_x, trasl_y, 1]
    #array bidimensional con las coordenadas y una fila extra de todo ceroy el ultimo valor un 1

    coords_transf=np.array(coordenadas).T
    ceros = np.zeros(len(coordenadas)+1)
    ceros[len(coordenadas)]=1
    coords_transf = np.vstack(coords_transf,ceros)
    #TODO probar que funcione bien

    #se recorre el array de coordenadas y se trasladan los puntos
    
    
    '''
    for i in range(len(coordenadas)):

        x = coordenadas[i][0]
        y = coordenadas[i][1]


        x=x-300
        y=-(y-300)

        x = x + trasl_x
        y = y + trasl_y

        coordenadas[i] = destraduccir_coordenadas(x,y)    
    #se limpia el canvas
    flush_canvas()




    #se dibujan los puntos
    for i in range(len(coordenadas)):

        

        x = coordenadas[i][0]
        y = coordenadas[i][1]

        

        color = canvas.itemcget(lapiz, "fill")

        canvas.create_rectangle(x - tamanhos_coords[i], y - tamanhos_coords[i],
                                 x + tamanhos_coords[i], y + tamanhos_coords[i], fill=color, outline=color)

    #se dibujan las lineas
    for i in range(len(lineas)):
        punto1=coordenadas[lineas[i]]
        punto2=coordenadas[lineas[i]-1]

        x1=punto1[0]
        x2=punto2[0]
        y1=punto1[1]
        y2=punto2[1]


        if canvas.itemcget(lapiz,"width")=="": #si no se ha definido el tamaño del lapiz se le asigna un tamaño de 2.0
            tamanio = 2.0
        else:
            tamanio = float(canvas.itemcget(lapiz, "width"))

        bresenham_algorithm(x1, y1, x2, y2, tamanio)

    '''

        


#metodo vacio para que no marque error
def metodo_vacio():
    print("Hola mundo")

def rotacion():
    #funcion que toma los puntos del array de coordenadas y los rota en funcion de la entrada de rotacion.
    #se rotan los elementos en funcion del centro del canvas
    #se debe de verificar que el array de coordenadas no este vacio
    

    #TODO arreglar bug de que los puntos se acerquen al centro del canvas

    #print("rotation algorithm")


    if len(coordenadas) < 1:
        
        print("no hay coordenadas")
        return -1
    
    #se obtiene el valor de rotacion
    rot_alfa = int(entry_rot_alfa.get())
    
    #se recorre el array de coordenadas y se rota cada punto
    
    array_aux=[]

    for punto in coordenadas:
        array_aux.append(rotar_punto(punto, rot_alfa))

    coordenadas = array_aux
    flush_canvas()

    dibujar_punto(coordenadas)

    for linea in lineas:
        bresenham_algorithm(coordenadas[linea], coordenadas[linea-1])




def rotar_punto(punto, angulo_grados):
    # Convierte el ángulo de grados a radianes
    angulo_radianes = np.radians(angulo_grados)

    # Crea la matriz de rotación
    matriz_rotacion = np.array([[np.cos(angulo_radianes), -np.sin(angulo_radianes)],
                                [np.sin(angulo_radianes), np.cos(angulo_radianes)]])

    # Multiplica la matriz de rotación por el punto
    punto_rotado = np.dot(matriz_rotacion, np.array(punto))

    return punto_rotado


def escalado():
    #funcion que toma los puntos del array de coordenadas y los escala en funcion de las entradas de escalado en x y en y.
    #se debe de verificar que el array de coordenadas no este vacio
    if len(coordenadas) <= 0:
        return -1
    
    #se obtienen los valores de escalado en x y en y
    esc_x = float(entry_esc_x.get())
    esc_y = float(entry_esc_y.get())
    
    #se recorre el array de coordenadas y se escala cada punto
    for i in range(len(coordenadas)):
        x = coordenadas[i][0]
        y = coordenadas[i][1]

        coordenadas_traducidas[i][0] = x * esc_x
        coordenadas_traducidas[i][1] = y * esc_y

    for i in range(len(coordenadas)):
        coordenadas[i] = destraduccir_coordenadas(coordenadas_traducidas[i][0], coordenadas_traducidas[i][1])

    #se limpia el canvas
    flush_canvas()

    

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

        if canvas.itemcget(lapiz,"width")=="": #si no se ha definido el tamaño del lapiz se le asigna un tamaño de 2.0
            tamanio = 2.0
        else:
            tamanio = float(canvas.itemcget(lapiz, "width"))

        bresenham_algorithm(x1, y1, x2, y2, tamanio)
    

def flush_canvas():
    canvas.create_rectangle(0, 0, 600, 600, fill="white", outline="white")
    canvas.create_line(300,0,300,600,fill="black", width=1)
    canvas.create_line(0,300,600,300,fill="black", width=1)

def rotate(grados):
    
    #funcion que toma los puntos del array de coordenadas y los rota en funcion de la entrada de rotacion.
    #se rotan los elementos en funcion del centro del canvas
    #se debe de verificar que el array de coordenadas no este vacio
    

    #TODO arreglar bug de que los puntos se acerquen al centro del canvas
    #TODO se supone que igual con calculo matricial se puede arreglar pero no tengo mucha fe

    #print("rotation algorithm")


    if len(coordenadas) <= 0:
        
        print("no hay coordenadas")
        return -1
    
    #se obtiene el valor de rotacion
    rot_alfa = grados
    
    alfa_radianes = math.radians(rot_alfa)
    #se recorre el array de coordenadas y se rota cada punto
    
    for i in range(len(coordenadas)):

        x = coordenadas[i][0]
        y = coordenadas[i][1]


        x=x-300
        y=-(y-300)

        x = round( (x * math.cos(alfa_radianes)) - (y * math.sin(alfa_radianes)), 0)
        y = round( (x * math.sin(alfa_radianes)) + (y * math.cos(alfa_radianes)), 0)

        coordenadas[i] = destraduccir_coordenadas(x,y)

    

    #se limpia el canvas
    flush_canvas()

    

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


        dist=math.sqrt((x2-x1)**2+(y2-y1)**2)

        print ("rot = ",rot_alfa,"dist = " ,dist)

        if canvas.itemcget(lapiz,"width")=="": #si no se ha definido el tamaño del lapiz se le asigna un tamaño de 2.0
            tamanio = 2.0
        else:
            tamanio = float(canvas.itemcget(lapiz, "width"))
            
        bresenham_algorithm(x1, y1, x2, y2, tamanio)



def rot_animation():
        rot_alfa = int(entry_rot_alfa.get())
        for i in range(rot_alfa):
            rotate(1)

def movidas():

    for i in range (300):
        coordenadas.append([random.randint(0,600),random.randint(0,600)])
        tamanhos_coords.append(random.randint(1,5))
    print ("buenas tardes")
    '''
    for i in range (20):
        print("hola")
        rotate(30)'''
    
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
btn_rot_animation = tk.Button(frame, text="Rotación animada", command=rot_animation)
btn_rot_animation.pack()


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

btn_random = tk.Button(frame, text="Random", command=movidas)
btn_random.pack()


# Ejecutar la aplicación
root.mainloop()

