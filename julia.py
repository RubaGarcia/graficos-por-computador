import numpy as np
import matplotlib.pyplot as plt

def julia_set(width, height, x_min, x_max, y_min, y_max, c, max_iter):
    julia_matrix = np.zeros((width, height))

    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)

    for i in range(width):
        for j in range(height):
            z = complex(x[i], y[j])
            julia_matrix[i, j] = calculate_julia(z, c, max_iter)

    return julia_matrix

def calculate_julia(z, c, max_iter):
    for i in range(max_iter):
        z = z * z + c
        if abs(z) > 2:
            return i
    return max_iter

def plot_julia_set(julia_matrix):
    plt.imshow(julia_matrix, cmap='hot', extent=(-2, 2, -2, 2))
    #plt.colorbar()
    plt.axis('off')  # Desactivar ejes
    plt.tight_layout(pad=0)  # Eliminar márgenes
    plt.show()

def mandelbrot_set(width, height, x_min, x_max, y_min, y_max, max_iter):
    mandelbrot_matrix = np.zeros((width, height))

    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)

    for i in range(width):
        for j in range(height):
            c = complex(x[i], y[j])
            mandelbrot_matrix[i, j] = calculate_mandelbrot(c, max_iter)

    return mandelbrot_matrix

def calculate_mandelbrot(c, max_iter):
    z = 0
    for i in range(max_iter):
        z = z*z + c
        if abs(z) > 2:
            return i
    return max_iter

def plot_mandelbrot_set(mandelbrot_matrix):
    plt.imshow(mandelbrot_matrix, cmap='hot', extent=(-2, 2, -2, 2))
    plt.colorbar()
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.title("Conjunto de Mandelbrot")
    plt.show()

# Parámetros para el conjunto de Julia
width, height = 1920, 1080
x_min, x_max = -2, 2
y_min, y_max = -2, 2
c = complex(-0.7, 0.27015)
max_iter = 750

julia_matrix = julia_set(width, height, x_min, x_max, y_min, y_max, c, max_iter)
plot_julia_set(julia_matrix)

max_iter = 75
mandelbrot_matrix = mandelbrot_set(width, height, x_min, x_max, y_min, y_max, max_iter)
plot_mandelbrot_set(mandelbrot_matrix)

def transform(p, matrix, translation):
    x, y = p
    a, b, c, d = matrix[0, 0], matrix[0, 1], matrix[1, 0], matrix[1, 1]
    e, f = translation

    return a*x + b*y + e, c*x + d*y + f

def ifs_deterministic(iterations, initial_point, transforms):
    points = [initial_point]

    for _ in range(iterations):
        current_point = points[-1]
        rand_index = np.random.randint(len(transforms))
        matrix, translation = transforms[rand_index][0], transforms[rand_index][1]
        new_point = transform(current_point, matrix, translation)
        points.append(new_point)

    return np.array(points)

def plot_fractal(points):
    plt.scatter(points[:, 0], points[:, 1], s=1, c='black', marker='.')
    plt.axis('equal')
    plt.axis('off')
    plt.show()

# Definición de transformaciones para el conjunto IFS de Koch
koch_transforms = [
    (np.array([[0.333, 0.0], [0.0, 0.333]]), np.array([0.0, 0.0])),
    (np.array([[0.167, -0.288], [0.288, 0.167]]), np.array([0.333, 0.0])),
    (np.array([[0.167, 0.288], [-0.288, 0.167]]), np.array([0.5, 0.288])),
    (np.array([[0.333, 0.0], [0.0, 0.333]]), np.array([0.667, 0.0]))
]

# Parámetros para el conjunto IFS de Koch
iterations = 50000
initial_point = (0, 0)

# Generar el conjunto IFS de Koch determinista
fractal_points_koch = ifs_deterministic(iterations, initial_point, koch_transforms)

# Plotear el conjunto IFS de Koch
plot_fractal(fractal_points_koch)
