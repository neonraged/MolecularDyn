# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation


def move_obj(n, x, y, z, point):
    # Функция для обновления положения точки
    point.set_data(np.array([x[n], y[n]]))
    point.set_3d_properties(z, 'z')
    return point


def xyz_count(axe0, axe, v, k, dt, m):
    #  Расчет координат точки по времени
    list_axe = []
    for i in range(100):
        f = -k * (axe - axe0)
        a = f / m
        v = v + a * dt
        axe = axe0 + v * dt
        list_axe.append(axe)
    return list_axe


#  Параметры системы

k = 10
m = 100
x0 = 2
y0 = 3
z0 = 0
dt = 0.1

#  Начальное состояние

y = 1
z = 1
x = 1
v_x = 2
v_y = 3
v_z = 1
t = 0


fig = plt.figure()
ax = p3.Axes3D(fig)

x_1 = [int(x*100000) for x in xyz_count(x0, x, v_x, k, dt, m)]
y_1 = [int(y*100000) for y in xyz_count(y0, y, v_y, k, dt, m)]
z_1 = [int(z*100000) for z in xyz_count(z0, z, v_z, k, dt, m)]
min_x1, min_y1, min_z1 = min(x_1), min(y_1), min(z_1)
x_1 = [x-min_x1 for x in x_1]
y_1 = [y-min_y1 for y in y_1]
z_1 = [z-min_z1 for z in z_1]
particle, = ax.plot([x_1[0]], [y_1[0]], [z_1[0]], label='Test particle')
ax.legend()
ax.set_xlim((min(x_1)-1, max(x_1)+1))
ax.set_ylim((min(y_1)-1, max(y_1)+1))
ax.set_zlim((min(z_1)-1, max(z_1)+1))
ani = animation.FuncAnimation(fig, move_obj, 100, fargs=(x_1, y_1, z_1, particle))

plt.show()