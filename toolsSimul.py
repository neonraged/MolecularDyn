# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation


def move_obj(n, xp, yp, zp, part):

    #  Функция для обновления положения точки

    part.set_data(np.array([xp[n], yp[n]]))
    part.set_3d_properties(zp[n], 'z')
    return part


def colliding(p1, p2):

    #  Функция проверки точек на столкновение

    if p1.x == p2.x and p1.y == p2.y and p1.z == p2.z:
        p1.v_x, p2.v_x, p1.ax, p2.ax = p2.v_x, p1.v_x, p2.ax, p1.ax
        p1.v_y, p2.v_y, p1.ay, p2.ay = p2.v_y, p1.v_y, p2.ay, p1.ay
        p1.v_z, p2.v_z, p1.az, p2.az = p2.v_z, p1.v_z, p2.az, p1.az


class Particle:

    #  Создание класса частиц -- единичных обьектов, за которые мы принимаем молекулы идеального газа

    def __init__(self, types):
        self.x = int(input("X axis start point for particle:"))
        self.y = int(input("Y axis start point for particle:"))
        self.z = int(input("Z axis start point for particle:"))
        self.v_x = int(input("X axis start velocity for particle:"))
        self.v_y = int(input("Y axis start velocity for particle:"))
        self.v_z = int(input("Z axis start velocity for particle:"))
        self.ax = int(input("X axis start acceleration for particle:"))
        self.ay = int(input("Y axis start acceleration for particle:"))
        self.az = int(input("Z axis start acceleration for particle:"))
        self.dt = 0.1
        self.xmass = []
        self.ymass = []
        self.zmass = []


class AnimatedPlot:

    def __init__(self, envs):
            self.itercount = len(envs.particles)
            self.aniobj = []
            self.env = envs

    def addaniobj(self, axs):
        for i in range(self.itercount):
            obj = self.env.particles[i]
            aniobject, = axs.plot([obj.xmass[0]], [obj.ymass[0]], [obj.ymass[0]], marker='o', markersize=10)
            self.aniobj.append(aniobject)


class Gas:

    def __init__(self, partnum=1, types=0):
        self.partnum = partnum
        self.types = types
        self.particles = []
        self.min_x = int(input("X axis min border:"))
        self.min_y = int(input("Y axis min border:"))
        self.min_z = int(input("Z axis min border:"))
        self.max_x = int(input("X axis max border:"))
        self.max_y = int(input("Y axis max border:"))
        self.max_z = int(input("Z axis max border:"))

    def addparticle(self):
        for i in range(self.partnum):
            self.particles.append(Particle(self.types))

    def process(self, time):

        self.addparticle()

        for t in range(0, time):

            for i in range(0, len(self.particles)):
                a = self.particles[i]
                self.move(a)

            for bou in range(0, len(self.particles)):
                self.bounce(self.particles[bou])

            for con in range(1, len(self.particles)):
                colliding(self.particles[con-1], self.particles[con])

    def bounce(self, p):

        if p.x + p.v_x * p.dt + ((p.ax * (p.dt ** 2))/2) > self.max_x:
            p.x = self.max_x
            p.v_x = -p.v_x

        elif p.x + p.v_x * p.dt + ((p.ax * (p.dt ** 2))/2) < self.min_x:
            p.x = self.min_x
            p.v_x = -p.v_x

        if p.y + p.v_y * p.dt + ((p.ay * (p.dt ** 2))/2) > self.max_y:
            p.y = self.max_y
            p.v_y = -p.v_y

        elif p.y + p.v_y * p.dt + ((p.ay * (p.dt ** 2))/2) < self.min_y:
            p.y = self.min_y
            p.v_y = -p.v_y

        if p.z + p.v_z * p.dt + ((p.az * (p.dt ** 2))/2) > self.max_z:
            p.z = self.max_z
            p.v_z = -p.v_z

        elif p.z + p.v_z * p.dt + ((p.az * (p.dt ** 2))/2) < self.min_z:
            p.z = self.min_z
            p.v_z = -p.v_z

    def move(self, p):
        p.x += p.v_x * p.dt + (p.ax * (p.dt ** 2)) / 2
        p.y += p.v_y * p.dt + (p.ay * (p.dt ** 2)) / 2
        p.z += p.v_z * p.dt + (p.az * (p.dt ** 2)) / 2
        p.v_x += p.ax * p.dt
        p.v_y += p.ay * p.dt
        p.v_z += p.az * p.dt
        p.particle.append(p.x)
        p.ymass.append(p.y)
        p.zmass.append(p.z)
