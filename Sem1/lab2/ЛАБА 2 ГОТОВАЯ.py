from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QTimer
import json
import random

class Rain_Window(QWidget):
    def __init__(self):
        super().__init__()
        # наследуем от класса QWidget
        self.setWindowTitle("Дождь")
        self.setGeometry(550, 150, 800, 800)
        self.setStyleSheet("background-color: ;")
        # создание окна
        self.drops=[]
        # список капель
        self.load_config()
        # сохраняем начальное состояние
        self.timer = QTimer()
        self.timer.timeout.connect(self.drops_change)
        self.timer.start(10)
        # таймер для перерисовки окна
        self.show()
        # показать окно

    def load_config(self):
            try:
                with open('config1.json', 'r') as f:
                    config = json.load(f)
            except FileNotFoundError:
                self.save_config()

    def save_config(self):
        config = 'начальное состояние'
        with open('config1.json', 'w') as f:
            json.dump(config, f)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        for drop in self.drops:
            painter.setPen(QPen(Qt.blue, drop[3])) # Qt.SolidLine по умолчанию
            # painter.setBrush(QBrush(Qt.red, Qt.SolidPattern)) прикольчик для заливки (не нужен)
            painter.drawLine(drop[0], drop[1], drop[0], drop[1]+drop[2])

    def drops_list(self):
        for _ in range(random.randint(200, 400)):
            x = random.randint(0, self.width())
            y = random.randint(-20, self.height())
            self.drops.append([x, y, random.randint(20, 30), random.randint(0,3), random.randint(3, 8)])
            #массив содержит х и у координаты, длину, толщину и скорость капли

    def drops_change(self):
        for drop in self.drops:
            drop[1]+=drop[4]
            if drop[1]>self.height():
                drop[1]=-1*drop[2]
                drop[0] = random.randint(0, self.width()) # CHANGE!!!
        self.repaint()
    
App = QApplication([])
window = Rain_Window()
window.drops_list()
App.exec_()
