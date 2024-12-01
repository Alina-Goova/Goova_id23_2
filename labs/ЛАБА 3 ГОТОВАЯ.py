from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QSpinBox, QLabel, QDialog, QMainWindow
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt, QTimer, QRect
import json
import random

spinbox_chr_list = [['Размер (width):', 1, 800],
                    ['Размер (height):', 1, 690],
                    ['Плотность капель', 100, 500, 300],
                    ['Скорость капель', 4, 8, 5]]

class ChangeTuchkaWindow(QDialog): # спавнит окно для изменения тучки
    def __init__(self, current_size, drops_data, form_number):
        global spinbox_chr_list
        super().__init__()
        self.resize(300, 200)
        
        self.layout = QVBoxLayout()
        
        #1
        self.spinbox1 = QSpinBox(self)
        self.spinbox1.setRange(spinbox_chr_list[0][1], spinbox_chr_list[0][2])
        self.spinbox1.setValue(current_size[0])        
        self.label1 = QLabel(spinbox_chr_list[0][0], self)
        
        #2
        self.spinbox2 = QSpinBox(self)
        self.spinbox2.setRange(spinbox_chr_list[1][1], spinbox_chr_list[1][2])
        self.spinbox2.setValue(current_size[1])        
        self.label2 = QLabel(spinbox_chr_list[1][0], self)
        
        #3
        self.spinbox3 = QSpinBox(self)
        self.spinbox3.setRange(spinbox_chr_list[2][1], spinbox_chr_list[2][2])
        self.spinbox3.setValue(drops_data[0])        
        self.label3 = QLabel(spinbox_chr_list[2][0], self)

        #4
        self.spinbox4 = QSpinBox(self)
        self.spinbox4.setRange(spinbox_chr_list[3][1], spinbox_chr_list[3][2])
        self.spinbox4.setValue(drops_data[1])        
        self.label4 = QLabel(spinbox_chr_list[3][0], self)

        #5
        self.spinbox5 = QSpinBox(self)
        self.spinbox5.setRange(1, 3)
        self.spinbox5.setValue(form_number)        
        self.label5 = QLabel(f'Выберите форму тучки:\n1 - Прямоугольник\n2 - Овал\n3 - Винни-Пух', self)

        apply_button = QPushButton("Apply", self)
        apply_button.clicked.connect(self.accept)  # Закрытие окна при нажатии
        
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.spinbox1)
        
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.spinbox2)
        
        self.layout.addWidget(self.label3)
        self.layout.addWidget(self.spinbox3)
        
        self.layout.addWidget(self.label4)
        self.layout.addWidget(self.spinbox4)
        
        self.layout.addWidget(self.label5)
        self.layout.addWidget(self.spinbox5)
        
        self.layout.addWidget(apply_button)
        self.setLayout(self.layout)
        self.setWindowTitle('Изменить тучку')
        self.show()

    def changed_values(self):
        return self.spinbox1.value(), self.spinbox2.value(), self.spinbox3.value(), self.spinbox4.value(), self.spinbox5.value()

class Tuchka():
    def __init__(self, x, y, pause_pressed, upd):
        self.x = x
        self.y = y
        self.width = 120
        self.height = 80
        self.drops_amount = 150
        self.drops_speed = 5

        self.drops = []
        self.form_number = 1
        self.upd = upd
        
        self.dragging = False
        self.pause_pressed = pause_pressed
        self.drops_list()

        self.timer = QTimer()
        self.timer.timeout.connect(self.drops_change)
        if self.pause_pressed == False:
            self.timer.start(20)
        else:
            self.timer.stop()
        
    def paint(self, painter):
        painter.setPen(QPen(Qt.white, 2))
        if self.form_number == 1:
            painter.drawRect(self.x, self.y, self.width-1, self.height-1)
        elif self.form_number == 2:
            painter.drawEllipse(self.x, self.y, self.width-1, self.height-1)
        elif self.form_number == 3:
            pixmap = QPixmap("винни-пух-тучка2.png")
            painter.drawPixmap(QRect(self.x, self.y, self.width-1, self.height-1), pixmap)
            
        for drop in self.drops:
            painter.drawLine(drop[0], drop[1], drop[0], drop[1]+drop[2])                

    def drops_list(self):
        self.drops = []
        for _ in range(self.drops_amount):
            x = random.randint(self.x + 10, self.x+self.width - 10)
            y = random.randint(self.y+self.height, self.y+self.height+50)
            self.drops.append([x, y, random.randint(20, 30), random.randint(0,3), random.randint(1*self.drops_speed, 3*self.drops_speed)])

    def change_tuchka(self):
        current_size = (self.width, self.height)
        drops_data = (self.drops_amount, self.drops_speed)
        change_tuchka_window = ChangeTuchkaWindow(current_size, drops_data, self.form_number)
        if change_tuchka_window.exec_() == ChangeTuchkaWindow.Accepted:
            new_values_list = change_tuchka_window.changed_values()
            new_width, new_height = new_values_list[:2]
            self.width = new_width
            self.height = new_height
            self.drops_amount = new_values_list[2]
            self.drops_speed = new_values_list[3]
            self.drops_list()
            if new_values_list[4] != self.form_number:
                self.form_number = new_values_list[4]
                self.upd()

    def drops_change(self):
        for drop in self.drops:
            drop[1]+=drop[4]
            if drop[1]+drop[2]>690:
                drop[1] = random.randint(self.y + self.height, self.y + self.height + 50)
                drop[0] = random.randint(self.x + 10, self.x+self.width -10)
        self.upd()

class Rain_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Дождь")
        self.setGeometry(550, 150, 800, 800)
        self.setStyleSheet("background-color: blue;")
        
        self.tuchka_button_list=[]
        self.pause_pressed = False
        self.deliting_tuchka = False
        self.dragging_tuchka = None

        self.initUI()

        self.InitialSystemState() # функция, отвечающая за начальное состояние ситемы, можно отключить чтобы начать без нее!!

    def initUI(self):
        make_tuchka_button=QPushButton("Создать тучку", self)
        make_tuchka_button.setStyleSheet("background-color: green;")
        make_tuchka_button.resize(180, 60)
        make_tuchka_button.move(50, 690)
        make_tuchka_button.clicked.connect(self.make_tuchka)
        
        make_tuchka_button=QPushButton("Пауза", self)
        make_tuchka_button.setStyleSheet("background-color: yellow;")
        make_tuchka_button.resize(180, 60)
        make_tuchka_button.move(250, 690)
        make_tuchka_button.clicked.connect(self.pause)
        
        make_tuchka_button=QPushButton("Удалить тучку", self)
        make_tuchka_button.setStyleSheet("background-color: red;")
        make_tuchka_button.resize(180, 60)
        make_tuchka_button.move(450, 690)
        make_tuchka_button.clicked.connect(self.delete_tuchka)
        
        self.show()

    def InitialSystemState(self):
        with open('iss.json', 'r') as iss:
            iss_data = json.load(iss)

        for i in range(3):
            tuchka_button = Tuchka(iss_data['x'][i], iss_data['y'][i], self.pause_pressed, self.update)

            tuchka_button.width = iss_data['width'][i]
            tuchka_button.height = iss_data['height'][i]
            tuchka_button.drops_amount = iss_data['drops_amount'][i]
            tuchka_button.drops_speed = iss_data['drops_speed'][i]
            tuchka_button.form_number = iss_data['form_number'][i]

            self.tuchka_button_list.append(tuchka_button)
        self.update()
        

    def make_tuchka(self):
        tuchka_button = Tuchka(random.randint(1, 600), 20, self.pause_pressed, self.update)
        self.tuchka_button_list.append(tuchka_button)
        self.update()

    def mousePressEvent(self, event):
        for tuchka in self.tuchka_button_list[-1::-1]:
            if event.button() == Qt.LeftButton:
                mouse_press_area = QRect(tuchka.x, tuchka.y, tuchka.x+tuchka.width, tuchka.y+tuchka.height)
                if mouse_press_area.contains(event.pos()):
                    if self.deliting_tuchka:
                        self.tuchka_button_list.remove(tuchka)
                        self.deliting_tuchka = False
                        self.update()
                    else:
                        tuchka.change_tuchka()
                    break
            elif event.button() == Qt.RightButton:
                mouse_press_area = QRect(tuchka.x, tuchka.y, tuchka.x+tuchka.width, tuchka.y+tuchka.height)
                if mouse_press_area.contains(event.pos()):
                    tuchka.dragging = True
                    self.dragging_tuchka = tuchka
                    break

    def mouseMoveEvent(self, event):
        if self.dragging_tuchka.dragging:
            self.dragging_tuchka.x, self.dragging_tuchka.y = event.pos().x(), event.pos().y()
            self.update()

    def mouseReleaseEvent(self, event):
        for tuchka in self.tuchka_button_list[-1::-1]:
            if event.button() == Qt.RightButton and tuchka.dragging == True:
                tuchka.dragging = False
                break

    def pause(self):
        for tuchka in self.tuchka_button_list:
            if tuchka.pause_pressed:
                tuchka.timer.start(20)
                tuchka.pause_pressed = False
                self.pause_pressed = False
            else:
                tuchka.timer.stop()
                tuchka.pause_pressed = True
                self.pause_pressed = True

    def delete_tuchka(self):
        self.deliting_tuchka = True

    def paintEvent(self, event):
        painter = QPainter(self)
        for tuchka in self.tuchka_button_list:
            tuchka.paint(painter)

App = QApplication([])
window = Rain_Window()
App.exec_()
