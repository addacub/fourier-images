# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 12:16:40 2020

@author: Acubelic
"""
from svg.path import parse_path
import matplotlib.pyplot as plt
import scipy.integrate
import numpy as np
import math


musicNote = ("""m 408.04 658 c 5.88 14.34 12.3 22.76 16.39 27.42 c 3.23 3.68
              20.94 20.04 0.53 45.61 c 12.12 -25.04 7.76 -39.88 -13.92 -49.03
              v 53 c 0.68 21.83 -21.75 23.16 -27.21 17.35 c -5.65 -5.99 7.67
              -25.89 24.21 -19.35 v -75 Z""")

PPCLogo = ("""M3455 747 c-39 -52 -61 -61 -51 -21 7 28 7 28 -16 -6 -23 -34 -27
-35 -103 -43 -116 -11 -212 -33 -270 -61 -39 -19 -60 -24 -92 -19 -27 3 -48 1
-57 -6 -11 -10 -24 -9 -60 3 -56 19 -144 33 -261 41 -134 9 -152 13 -190 47
-19 16 -35 25 -35 19 0 -7 -20 2 -45 19 -34 23 -43 26 -38 13 6 -16 5 -16 -10
-4 -10 8 -20 11 -24 7 -3 -3 -1 -6 5 -6 7 0 12 -6 12 -14 0 -8 16 -20 35 -26
29 -10 34 -14 24 -26 -9 -12 -5 -14 26 -14 39 0 143 -29 307 -86 53 -18 132
-40 175 -49 103 -21 148 -44 226 -115 70 -64 77 -68 77 -45 0 11 7 14 25 9 40
-10 29 10 -35 61 -33 26 -60 53 -60 60 0 7 33 24 73 40 39 15 138 61 218 102
81 41 162 76 182 80 25 4 34 10 30 19 -3 8 0 14 5 14 6 0 10 9 9 19 -1 15 -5
17 -19 10 -9 -5 -20 -14 -23 -19 -12 -20 -26 -10 -15 11 19 35 7 28 -25 -14z""")

LMALogo = ("""m312.7 78.5-8 17h-7.3l-.8-17h-.3l-3.5 17h-7.6l5.3-25.5h12.5
           l.2 14.7h.3l6.2-14.7h12.9l-5.3 25.5h-8.1l3.7-17z
           m27.8-8.4h11.6l1.8 25.5h-8.3l-.1-4.5h-7.5l-2 4.5h-7.8z
           m5 15.6-.5-9.7h-.3l-4.7 9.7z
           m59.1-9.6h-5.6l1.3-6h19.5l-1.2 6h-5.6l-4.1 19.5h-8.3z
           m48.4-6h11.3l2.5 15.2h.2l3.2-15.2h7.9l-5.3 25.5h-11.3l-2.1-15.6
           h-.3l-3.2 15.6h-8.2z
           m-82.5 0h12.3c6 0 8.1 3.3 8.1 6.5 0 4.8-4.1 6.2-6.1 6.6v.4
           c2.4.3 3.5 2 3.5 4.2 0 1.7-.4 3.4-.4 5.6 0 .9.2 1.9.2 2.3
           h-8.9c0-.1-.1-1-.1-1.5 0-2.1.6-3.6.6-6 0-1.1-.4-2.1-2.1-2.1
           h-2.2l-2 9.6h-8.4z
           m8.3 10.6c2.4 0 3.4-1.2 3.4-2.7 0-1.3-.7-1.9-2.4-1.9h-2.1l-1 4.6z
           m51.5-10.6h8.3l-5.3 25.5h-8.3z
           m-422 0h8.3l-4 19.5h8.2l-1.2 6h-16.6z
           m96.4 0h8.3l-2.3 11h.2l7.4-11h8.9l-9.2 12 4.6 13.5h-8.9l-3.5-11.3
           h-.2l-2.4 11.3h-8.3z
           m43.3 15.9h-5l-2 9.6h-8.3l5.3-25.5h8.3l-2 9.6h5l2-9.6h8.3
           l-5.3 25.5h-8.3z
           m58.6-15.9h17.5l-1.3 6h-9.2l-.8 3.8h8.3l-1.3 6h-8.3l-.8 3.7h9.6
           l-1.3 6h-17.9z
           m-32 0h17.5l-1.3 6h-9.2l-.8 3.8h8.3l-1.3 6h-8.3l-.8 3.7h9.6
           l-1.3 6h-17.9z
           m-128.5-.4c6.2 0 9.5 3.5 9.5 9 0 6.7-3.5 17.2-14.4 17.2-6 0-9.6
           -3.3-9.6-9 .2-7.4 4-17.2 14.5-17.2
           m-3.9 19.8c3.7 0 5.2-9.1 5.2-11.2 0-1.1-.5-2.2-2.2-2.2-3.8 0
           -5.2 9.3-5.2 11.2 0 1.8 1.2 2.2 2.2 2.2
           m197.8-19.4h9.4c8.1 0 11.4 4.5 11.4 9.5 0 9.5-6 16-16 16h-10.2z
           m4.3 19.4h2.4c3.4 0 5.7-4.5 5.7-10 0-2-.9-3.5-3.9-3.5h-1.5z
           m-156.8-3.5c-1.4 6.9-6.4 9.9-12.3 9.9-6.2 0-9.5-3.5-9.5-9 0
           -6.4 3.3-17.2 14.4-17.2 5.1 0 9.2 1.9 9 7.3 0 .8-.2 2.1-.3 2.6
           h-7.8c0-.2.2-.9.2-1.6 0-1.4-1.1-1.9-2-1.9-3.8 0-5.3 9.2-5.3
           11.2 0 1.5.9 2.2 2.1 2.2 1.3 0 2.5-1 3.5-3.5z
           m417.1 1.9c-.7.7-.7.7 0 0
           m63.6-27.5 25.8.6-30.6 17.3c1.6-6.1 3.1-11.7 4.8-17.9
           m-.1-30.3-4.5 23.4h-21.2z
           m58.7 23.4h-56.6c7.4-28 14.2-51.7 14.2-51.7s-25.6 27.2-48.2 51.7
           l-224.5.5h.2-.2l218.9 5.5c-16.8 17.9-25.7 28.1-26.1 28.5l.1-.1
           c.7-.6 31-28.3 31-28.3l26.6.7-4 21-124.8 70.6c-.3.2-.5.3-.5.3
           s99.1-52.1 124.1-64.7c0 0-8.8 45.8-8.8 46v-.1.1l.1-.5
           c.8-3 6.1-21 13.2-47.7 32.7-16.6 65.3-31.8 65.3-31.8""")

LMALogo = ("""m63.6-27.5 25.8.6-30.6 17.3c1.6-6.1 3.1-11.7 4.8-17.9
           m-.1-30.3-4.5 23.4h-21.2z
           m58.7 23.4h-56.6c7.4 -28 14.2 -51.7 14.2 -51.7s-25.6 27.2 -48.2
           51.7l-224.5.5h.2 -.2l218.9 5.5c-16.8 17.9 -25.7 28.1 -26.1 28.5
           l.1 -.1c.7 -.6 31 -28.3 31 -28.3l26.6 .7 -4 21 -124.8 70.6
           c-.3.2 -.5.3 -.5.3s99.1 -52.1 124.1 -64.7c0 0 -8.8 45.8 -8.8 46
           v-.1.1l.1 -.5c.8 -3 6.1 -21 13.2 -47.7 32.7 -16.6 65.3 -31.8 65.3
           -31.8""")


def get_image_outline(svgPath, resolution, invertY=False):
    """Return points of SVG path."""

    # Initialise empty list
    outline = []

    # Parse the SVG path to get a path object
    pathObject = parse_path(svgPath)

    # Set initial value of t and determine time increment
    dt = 1 / resolution

    for pathObject in pathObject[1:]:
        t = 0
        for i in range(resolution):
            outline.append(pathObject.point(t))
            t += dt

    # Flip or not flip y-axis
    outline = np.array(outline)
    if invertY:
        outline = np.conj(outline)

    return outline


def get_centroid(outline):
    """Return centroid / geometric centre of shape to translate origin."""
    nPoints = len(outline)
    centroid = sum(outline) / nPoints

    return centroid


def draw_image(outline):
    """Draws outline of image."""

    # Initialise x and y lists
    xPoints = []
    yPoints = []

    # Extract real and imaginary points
    for point in outline:
        xPoints.append(point.real)
        yPoints.append(point.imag)

    plt.plot(xPoints, yPoints, 'b-')
    # plt.plot(centroid.real, centroid.imag, 'ro')
    plt.xlabel('real axis')
    plt.ylabel('imaginary axis')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


def integrate(outline, nValue):
    """Return the integral of the function between 0 --> 1."""

    # Create array of constants n
    terms = np.arange(-nValue, nValue + 1)

    # Vectorise output points
    outline = np.array(outline)

    # Create t values
    nPoints = len(outline)
    dt = 1 / (nPoints - 1)
    t = np.arange(0, 1 + dt, dt)

    # Initialise empty list for constants
    CnList = []

    for n in terms:
        exp = math.e**(-n * 2 * math.pi * 1j * t)
        eValues = np.array(exp)
        CnList.append(scipy.integrate.simps(outline * eValues, t))

    return CnList


def get_Cn_List(constants):
    """Cycles through the selected number of constants."""

    CnListOrdered = []
    n = len(constants)

    mid_point = (n - 1) // 2
    positive = False
    k = 0  # nth value of constant
    for i in range(n):
        if positive:
            CnListOrdered.append(constants[mid_point + k])
            positive = False
        else:
            CnListOrdered.append(constants[mid_point - k])
            k += 1
            positive = True

    return CnListOrdered


def get_constants(svgPath, pathResolution=150, invertY=True, nValue=200):
    """Returns constants required to draw image using Fourier Transform."""
    outline = get_image_outline(svgPath, pathResolution, invertY=invertY)
    centroid = get_centroid(outline)
    outlineTranslated = outline - centroid
    # Uncomment when plot required to preview image
    draw_image(outlineTranslated)
    constants = integrate(outlineTranslated, nValue)
    CnList = get_Cn_List(constants)

    return CnList

# %%
# Code to test that calculating image point works.


def get_n_value(i):
    """Return n value of ith element in Cn List."""
    sign = (-1)**(i + 1)
    value = i // 2 + abs(math.sin(i * math.pi / 2))
    n = int(sign * value)

    return n


def get_edge_point(t, n, Cn):
    complexPoint = Cn * math.e**(n * 2 * math.pi * 1j * t)

    return complexPoint


def get_image_point(t, CnList):
    point = 0
    for i, Cn in enumerate(CnList):
        n = get_n_value(i)
        point += get_edge_point(t, n, Cn)

    return point


if __name__ == "__main__":
    CnList = get_constants(LHMLogo)
    outline = []
    for t in np.arange(0, 1, 1 / 50):
        outline.append(get_image_point(t, CnList))

    # draw_image(outline)
