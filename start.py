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
        p1.v_x, p2.v_x = p2.v_x, p1.v_x
        p1.v_y, p2.v_y = p2.v_y, p1.v_y
        p1.v_z, p2.v_z = p2.v_z, p1.v_z


class Particle:

    #  Создание класса частиц -- единичных обьектов, за которые мы принимаем молекулы идеального газа

    def __init__(self):
        self.x = int(input("X axis start point for particle:"))
        self.y = int(input("Y axis start point for particle:"))
        self.z = int(input("Z axis start point for particle:"))
        self.v_x = int(input("X axis start velocity for particle:"))
        self.v_y = int(input("Y axis start velocity for particle:"))
        self.v_z = int(input("Z axis start velocity for particle:"))
        self.dt = 1
        self.xmass = []
        self.ymass = []
        self.zmass = []

    def move(self):
        self.x += self.v_x*self.dt
        self.y += self.v_y*self.dt
        self.z += self.v_z*self.dt
        self.xmass.append(self.x)
        self.ymass.append(self.y)
        self.zmass.append(self.z)


class Simulation:

    # Создание класса сосуда симуляции и происшествий внутри модели

    def __init__(self):
        self.min_x = int(input("X axis min border:"))
        self.min_y = int(input("Y axis min border:"))
        self.min_z = int(input("Z axis min border:"))
        self.max_x = int(input("X axis max border:"))
        self.max_y = int(input("Y axis max border:"))
        self.max_z = int(input("Z axis max border:"))
        self.particles = []

    def bounce(self, particle):

        if particle.x > self.max_x + 1:
            particle.x = self.max_x - 1
            particle.v_x = -particle.v_x

        elif particle.x < self.min_x - 1:
            particle.x = self.min_x + 1
            particle.v_x = -particle.v_x

        if particle.y > self.max_y + 1:
            particle.y = self.max_y - 1
            particle.v_y = -particle.v_y

        elif particle.y < self.min_y - 1:
            particle.y = self.min_y + 1
            particle.v_y = -particle.v_y

        if particle.z > self.max_z - 1:
            particle.z = self.max_z - 1
            particle.v_z = -particle.v_z

        elif particle.z < self.min_z - 1:
            particle.z = self.min_z + 1
            particle.v_z = -particle.v_z

    def addparticle(self, numb):
        for i in range(numb):
            self.particles.append(Particle())

    def process(self, time):

        self.addparticle(int(input("Enter number of particles in system:")))

        for t in range(0, time):

            for i in range(0, len(self.particles)):
                a = self.particles[i]
                a.move()

            for bou in range(0, len(self.particles)):
                self.bounce(self.particles[bou])

            for con in range(1, len(self.particles)):
                colliding(self.particles[con-1], self.particles[con])


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



time = 50
env = Simulation()
env.process(time)
fig = plt.figure()
ax = p3.Axes3D(fig)
plotting = AnimatedPlot(env)
plotting.addaniobj(ax)
ax.legend()
ax.set_xlim((env.min_x, env.max_x))
ax.set_ylim((env.min_y, env.max_y))
ax.set_zlim((env.min_z, env.max_z))
ani_list = [0 for x in range(len(env.particles))]
for i in range(len(env.particles)):
    obj = env.particles[i]
    aniobjf = plotting.aniobj[i]
    ani_list[i] = animation.FuncAnimation(fig, move_obj, 50, fargs=(obj.xmass, obj.ymass, obj.zmass, aniobjf))
plt.show()
