# -*- coding: utf-8 -*-

from toolsSimul import *

time = 500

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
    ani_list[i] = animation.FuncAnimation(fig, move_obj, 500, fargs=(obj.xmass, obj.ymass, obj.zmass, aniobjf))

plt.show()
