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

    def __init__(self, r):

        self.x = int(input("X axis start point for particle:"))
        self.y = int(input("Y axis start point for particle:"))
        self.z = int(input("Z axis start point for particle:"))
        self.v = Vec(int(input()), int(input()), int(input()))
        self.a = Vec(int(input()), int(input()), int(input()))
        self.dt = 0.1
        self.r = r
        self.xmass = []
        self.ymass = []
        self.zmass = []


class Vec:

    def __init__(self, x, y, z):

        self.coords = [x, y, z]

    def __sub__(self, other):

        if isinstance(other, Vec):

            self.coords = [a - b for a, b in zip(self.coords, other.coords)]

        else:

            self.coords = [x - other for x in self.coords]

    def __mul__(self, other):

        if isinstance(other, Vec):

            self.coords = [a * b for a, b in zip(self.coords, other.coords)]

        else:

            self.coords = [x*other for x in self.coords]

    def __add__(self, other):

        if isinstance(other, Vec):

            self.coords = [a + b for a, b in zip(self.coords, other.coords)]

        else:

            self.coords = [x + other for x in self.coords]


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

        if p.x + p.v.coords[1] * p.dt + ((p.a.coords[1] * (p.dt ** 2))/2) > self.max_x:
            p.x = self.max_x
            p.v.coords[1] = -p.v.coords[1]

        elif p.x + p.v.coords[1] * p.dt + ((p.a.coords[1] * (p.dt ** 2))/2) < self.min_x:
            p.x = self.min_x
            p.v.coords[1] = -p.v.coords[1]

        if p.y + p.v.coords[2] * p.dt + ((p.a.coords[2] * (p.dt ** 2))/2) > self.max_y:
            p.y = self.max_y
            p.v.coords[2] = -p.v.coords[2]

        elif p.y + p.v.coords[2] * p.dt + ((p.a.coords[2] * (p.dt ** 2))/2) < self.min_y:
            p.y = self.min_y
            p.v.coords[2] = -p.v.coords[2]

        if p.z + p.v.coords[3] * p.dt + ((p.a.coords[3] * (p.dt ** 2))/2) > self.max_z:
            p.z = self.max_z
            p.v.coords[3] = -p.v.coords[3]

        elif p.z + p.v.coords[3] * p.dt + ((p.a.coords[3] * (p.dt ** 2))/2) < self.min_z:
            p.z = self.min_z
            p.v.coords[3] = -p.v.coords[3]

    def move(self, p):

        p.x += p.v.coords[1] * p.dt + (p.a.coords[1] * (p.dt ** 2)) / 2
        p.y += p.v.coords[2] * p.dt + (p.a.coords[1] * (p.dt ** 2)) / 2
        p.z += p.v.coords[3] * p.dt + (p.a.coords[1] * (p.dt ** 2)) / 2
        p.v.coords[1] += p.a.coords[1] * p.dt
        p.v.coords[2] += p.a.coords[2] * p.dt
        p.v.coords[3] += p.a.coords[3] * p.dt
        p.xmass.append(p.x)
        p.ymass.append(p.y)
        p.zmass.append(p.z)
