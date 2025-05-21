import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
import matplotlib.animation as animation
def update(frameNum, img, grid):
 # Definimos el kernel: todos los vecinos cuentan igual, la celda central no se cuenta
    kernel = np.array([[1, 1, 1],
                    [1, 0, 1],
                    [1, 1, 1]])
 # Usamos convolve2d para aplicar el kernel a la grilla, considerando condiciones de frontera periódicas
    convolved = convolve2d(grid, kernel, mode='same', boundary='fill')
 # Aplicamos las reglas del Juego de la Vida de Conway
    birth = (convolved == 3) & (grid == 0) # Una célula muerta con exactamente 3 vecinos vivos "nace"
    survive = ((convolved == 2) | (convolved == 3)) & (grid == 1) # Una célula viva con 2 o 3 vecinos vivos sobrevive
    grid[:, :] = 0 # Primero, seteamos todas las células a "muertas"
    grid[birth | survive] = 1 # Luego, actualizamos las células que deben "nacer" o sobrevivir
 # Actualizamos la imagen con el nuevo estado
    img.set_data(grid)
    return img,
# Configuración inicial
N = 100 # Tamaño de la grilla NxN
grid = np.random.choice([0,1], N*N, p=[0.8, 0.2]).reshape(N, N) # Inicialización aleatoria
print(grid)
# Configuración de la visualización
fig, ax = plt.subplots()
img = ax.imshow(grid, interpolation='nearest')
ani = animation.FuncAnimation(fig, update, fargs=(img, grid),
                                frames=10,
                                interval=100,
                                save_count=5)
plt.show()