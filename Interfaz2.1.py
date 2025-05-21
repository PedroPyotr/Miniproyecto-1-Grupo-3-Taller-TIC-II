import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSpinBox, QPushButton
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import serial
import time

class ConwayGame(QWidget):
    def __init__(self, N=100, interval=100):
        super().__init__()
        self.N = N
        self.interval = interval
        self.grid = np.random.choice([0, 1], N*N, p=[0.8, 0.2]).reshape(N, N)
        self.layout = QVBoxLayout()
        self.celulas_vivas=0
        # Título del juego
        self.title_label = QLabel("Conway's Game of Life")
        self.title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)
        
        # Controles para ajustar las reglas
        self.controls_layout = QHBoxLayout()
        
        # SpinBox para nacimiento
        self.birth_label = QLabel("Nacimiento (vecinos):")
        self.birth_spinbox = QSpinBox()
        self.birth_spinbox.setRange(0, 5)
        self.birth_spinbox.setValue(3)
        self.birth_spinbox.valueChanged.connect(self.update_rules)
        self.controls_layout.addWidget(self.birth_label)
        self.controls_layout.addWidget(self.birth_spinbox)
        
        # SpinBox para supervivencia mínima
        self.survive_min_label = QLabel("Supervivencia mínima (vecinos):")
        self.survive_min_spinbox = QSpinBox()
        self.survive_min_spinbox.setRange(0, 5)
        self.survive_min_spinbox.setValue(2)
        self.survive_min_spinbox.valueChanged.connect(self.update_rules)
        self.controls_layout.addWidget(self.survive_min_label)
        self.controls_layout.addWidget(self.survive_min_spinbox)
        
        # SpinBox para supervivencia máxima
        self.survive_max_label = QLabel("Supervivencia máxima (vecinos):")
        self.survive_max_spinbox = QSpinBox()
        self.survive_max_spinbox.setRange(0, 5)
        self.survive_max_spinbox.setValue(3)
        self.survive_max_spinbox.valueChanged.connect(self.update_rules)
        self.controls_layout.addWidget(self.survive_max_label)
        self.controls_layout.addWidget(self.survive_max_spinbox)
        
        self.layout.addLayout(self.controls_layout)
        
        # Gráfica del juego
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.img = self.ax.imshow(self.grid, interpolation='nearest', cmap='gray')
        self.layout.addWidget(self.canvas)
        
        self.setLayout(self.layout)
        
        # Inicializar reglas
        self.birth_rule = self.birth_spinbox.value()
        self.survive_min_rule = self.survive_min_spinbox.value()
        self.survive_max_rule = self.survive_max_spinbox.value()
        
        # Temporizador para actualizar la cuadrícula
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_grid)
        self.timer.start(self.interval)

         # Botón de reinicio
        self.reset_button = QPushButton("Reiniciar Juego")
        self.reset_button.clicked.connect(self.reset_game)
        self.layout.addWidget(self.reset_button)

        # Contador de células vivas
        self.live_cells_label = QLabel("Células vivas: 0")
        self.layout.addWidget(self.live_cells_label)

        # Temporizador para actualizar el contador cada 10 segundos
        self.counter_timer = QTimer()
        self.counter_timer.timeout.connect(self.update_live_cells_count)
        self.counter_timer.start(10000)  # 10000 ms = 10 segundos

        #Comunicaciones con arduino
        self.ser = serial.Serial('COM8', 9600, timeout=1)
        self.serial_timer = QTimer(self)
        self.serial_timer.timeout.connect(self.check_serial_input)
        self.serial_timer.start(100) 
        self.setup_timers()


    def update_rules(self):
        # Actualizar reglas de nacimiento y supervivencia
        self.birth_rule = self.birth_spinbox.value()
        self.survive_min_rule = self.survive_min_spinbox.value()
        self.survive_max_rule = self.survive_max_spinbox.value()
        
        # Asegurar que survive_min_rule <= survive_max_rule
        if self.survive_min_rule > self.survive_max_rule:
            self.survive_max_spinbox.setValue(self.survive_min_rule)
    
    def update_grid(self):
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])
        convolved = convolve2d(self.grid, kernel, mode='same', boundary='fill')
        birth = (convolved == self.birth_rule) & (self.grid == 0)
        survive = ((convolved >= self.survive_min_rule) & (convolved <= self.survive_max_rule)) & (self.grid == 1)
        self.grid[:, :] = 0
        self.grid[birth | survive] = 1
        self.img.set_data(self.grid)
        self.canvas.draw()

    def reset_game(self):
        # Reiniciar la cuadrícula con una nueva configuración aleatoria
        self.grid = np.random.choice([0, 1], self.N * self.N, p=[0.8, 0.2]).reshape(self.N, self.N)
        self.img.set_data(self.grid)
        self.canvas.draw()

#seccion comunicacion arduino
    def setup_serial(self):
        self.ser = serial.Serial('COM8', 9600, timeout=1)
        time.sleep(2)

    def update_live_cells_count(self):
        # Contar las células vivas y actualizar la etiqueta
        live_cells = np.sum(self.grid)
        self.live_cells_label.setText(f"Células vivas: {live_cells}")
        self.celulas_vivas = live_cells

    def send_live_cells_count(self):
        message = f"{self.celulas_vivas}\n"
        self.ser.write(message.encode('utf-8'))
        print(f"Enviado a Arduino: {message.strip()}")

    def check_serial_input(self):
        if self.ser.in_waiting > 0:
            line = self.ser.readline().decode('utf-8').strip()
            print(f"Recibido de Arduino: {line}")
            if line == "REINICIAR":
                self.reset_game()

    def setup_timers(self):
        # Temporizador para enviar el conteo de células vivas cada 10 segundos
        self.send_timer = QTimer(self)
        self.send_timer.timeout.connect(self.send_live_cells_count)
        self.send_timer.start(10000)  # 10,000 ms = 10 segundos

        # Temporizador para verificar la entrada serial cada 100 ms
        self.serial_timer = QTimer(self)
        self.serial_timer.timeout.connect(self.check_serial_input)
        self.serial_timer.start(100) 

        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conway's Game of Life")
        self.setGeometry(100, 100, 800, 600)
        self.game = ConwayGame()
        self.setCentralWidget(self.game)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

