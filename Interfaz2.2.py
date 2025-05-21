# Python interface: Zombie Invasion Game (PyQt6 + matplotlib + serial)
import sys
import numpy as np
import random
import re
import serial
import time
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QSpinBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from playsound import playsound  # or QSound if preferred

# Pulsar pattern from annex
PULSAR_PATTERN = np.array([
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,0]
])
INVERSE_PULSAR = 1 - PULSAR_PATTERN

class ZombieGame(QWidget):
    def __init__(self, N=100, interval=100):
        super().__init__()
        self.N = N
        self.interval = interval
        # state grid: 0=zombie,1=alive,2=dead
        self.state = np.random.choice([0,1], N*N, p=[0.2,0.8]).reshape(N,N)
        self.life = np.full((N,N), 200, dtype=int)
        self.init_ui()
        self.setup_serial()
        self.setup_timers()

    def init_ui(self):
        layout = QVBoxLayout()
        self.title = QLabel("Zombie Invasion Simulator")
        self.title.setFont(QFont("Arial",18,QFont.Weight.Bold))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)
        # buttons for special events
        btn_layout = QHBoxLayout()
        events = ["Infección masiva","Pulsar mutado","Ritual purificación","I am atomic!","Reiniciar"]
        for i, name in enumerate(events,1):
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, x=i: self.handle_event(x))
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)
        # canvas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def setup_serial(self):
        self.ser = serial.Serial('COM8',9600,timeout=1)
        time.sleep(2)

    def setup_timers(self):
        # game iterations
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.iteration)
        self.timer.start(self.interval)
        # serial read
        self.serial_timer = QTimer(self)
        self.serial_timer.timeout.connect(self.check_serial)
        self.serial_timer.start(100)

    def iteration(self):
        new_state = self.state.copy()
        new_life = self.life.copy()
        kernel = np.ones((3,3),int)
        kernel[1,1]=0
        # count neighbors for alive and zombies
        alive_nb = convolve2d((self.state==1).astype(int),kernel,'same','wrap')
        zombie_nb= convolve2d((self.state==0).astype(int),kernel,'same','wrap')
        for i in range(self.N):
            for j in range(self.N):
                s = self.state[i,j]
                if s==1: # person
                    loss = 5*zombie_nb[i,j]
                    new_life[i,j] -= loss
                    if new_life[i,j]<=0:
                        new_state[i,j]=0; new_life[i,j]=100
                elif s==0: # zombie
                    if alive_nb[i,j]<2: new_life[i,j]-=10
                    elif alive_nb[i,j]>3: new_life[i,j]-=30
                    if new_life[i,j]<=0:
                        if random.random()<0.1:
                            new_state[i,j]=1; new_life[i,j]=100
                        else:
                            new_state[i,j]=2; new_life[i,j]=0
                else: # dead
                    if alive_nb[i,j]>=2 and zombie_nb[i,j]<2:
                        new_state[i,j]=1; new_life[i,j]=100
                    elif zombie_nb[i,j]>=2 and alive_nb[i,j]<2:
                        new_state[i,j]=0; new_life[i,j]=100
                    elif zombie_nb[i,j]>=2 and alive_nb[i,j]>=2:
                        new_state[i,j]=0; new_life[i,j]=100
        self.state=new_state; self.life=new_life
        self.draw()
        self.check_endgame()

    def draw(self):
        cmap = {0:(0.5,0,0),1:(1,1,1),2:(0.2,0.2,0.2)}
        img = np.zeros((self.N,self.N,3))
        for k,v in cmap.items(): img[self.state==k]=v
        self.ax.clear(); self.ax.imshow(img,interpolation='nearest')
        self.canvas.draw()

    def handle_event(self,x):
        if x==1: # 5x5 random alive block -> zombies 200
            i,j = random.randint(0,self.N-5),random.randint(0,self.N-5)
            self.state[i:i+5,j:j+5]=0; self.life[i:i+5,j:j+5]=200
        elif x==2: # pulsar mutado
            off = 6
            center = self.N//2
            mask = PULSAR_PATTERN
            self.state[center-off:center-off+13,center-off:center-off+13] = np.where(mask,0,self.state[center-off:center-off+13,center-off:center-off+13])
            self.life[center-off:center-off+13,center-off:center-off+13]=200
        elif x==3: # ritual purificación
            i,j = random.randint(0,self.N-15),random.randint(0,self.N-15)
            sub = self.state[i:i+15,j:j+15]
            zpos = np.where(sub==0)
            for a,b in zip(*zpos):
                if random.random()<0.8: sub[a,b]=1; self.life[i+a,j+b]=200
            self.state[i:i+15,j:j+15]=sub
        elif x==4: # atomic
            i,j = random.randint(0,self.N-25),random.randint(0,self.N-25)
            self.state[i:i+25,j:j+25]=2; self.life[i:i+25,j:j+25]=0
        else: # reiniciar
            self.reset_game()
        self.draw()

    def reset_game(self):
        self.state = np.random.choice([0,1],self.N*self.N,p=[0.2,0.8]).reshape(self.N,self.N)
        self.life = np.full((self.N,self.N),200)
        self.draw()

    def check_serial(self):
        if self.ser.in_waiting>0:
            msg = self.ser.readline().decode().strip()
            if re.match(r'^a-[1-4]$',msg):
                eid=int(msg.split('-')[1]); self.handle_event(eid)
            elif msg=='r': self.reset_game()

    def check_endgame(self):
        if np.all(self.state==0) or np.all(self.state==1):
            #playsound('victory.mp3' if np.all(self.state==1) else 'defeat.mp3')
            self.reset_game()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zombie Invasion Simulator")
        self.setGeometry(50,50,800,800)
        self.game = ZombieGame()
        self.setCentralWidget(self.game)

if __name__=='__main__':
    app=QApplication(sys.argv)
    w=MainWindow(); w.show(); sys.exit(app.exec())