import numpy as np
from pyaxidraw import axidraw
import random

# Lims = 430 x 297 mm


def mark(axi, dist):
    axi.move(-dist, -dist)
    axi.line(2 * dist, 2 * dist)
    axi.line(-dist, -1.5 * dist)
    axi.line(dist, dist)
    axi.line(-2 * dist, 0.5 * dist)


def offset(mode):
    return random.triangular(mode=mode)


def scribble(axi):
    num_x = 7
    num_y = 8
    scale = 5
    for x in range(num_x):
        for y in range(num_y):
            jitter = (x * y) / (num_x + num_y)
            axi.moveto((x + offset(jitter)) * scale, (y + offset(jitter)) * scale)
            mark(axi, 3)


def burst(axi, num_x, num_y, length, scale):
    for x in range(num_x):
        for y in range(num_y):
            jitter = (x + y) / (num_x + num_y)

            axi.moveto((x + offset(jitter)) * scale, (y + offset(jitter)) * scale)
            axi.line(scale * x, scale * y)


def hump(axi, resolution, height):
    drawn_paths = 0
    for x in range(resolution):
        axi.lineto(x, height * (resolution / 2))


if __name__ == "__main__":
    ad = axidraw.AxiDraw()
    ad.interactive()
    ad.options.model = 2
    ad.options.units = 2
    ad.update()
    ad.connect()

    # scribble(ad)
    # burst(ad, 10, 10, 10, 2)
    hump(ad, 30, 20)
    ad.moveto(0, 0)
    ad.disconnect()
