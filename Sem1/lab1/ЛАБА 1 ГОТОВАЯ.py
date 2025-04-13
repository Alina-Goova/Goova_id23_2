import numpy as np
from tkinter import *
import math

def F(num_points=400): #ПЛОТНОСТЬ
    global x0, y0, r
    a = []    
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = x0 + r * math.cos(2 * math.pi * i / num_points)
        y = y0 + r * math.sin(2 * math.pi * i / num_points)
        a.append((x, y))
    return a

def move():
    global n, a, point, speed, dir
    n+=dir_
    if dir_*n==len(a):
        n=0
    i, j = a[n]
    canvas.delete(point)
    point = canvas.create_oval(i-5, j-5, i+5, j+5, fill='red')
    canvas.after(speed, move)
    
size = 600
root = Tk() #создаем окно
canvas = Canvas(root, width=size, height=size) #создаем холст
canvas.pack() #указание расположить холст внутри окна
w = 100
x0 = 300
y0 = 300
r = 250
canvas.create_oval(w, w, size - w, size - w, fill='blue')
a = F()
i, j = a[0]
point = canvas.create_oval(i-5, j-5, i+5, j+5, fill='red')
n = 0
speed = 10 # СКОРОСТЬ
dir_ = -1 # НАПРАВЛЕНИЕ
move()
root.mainloop()
