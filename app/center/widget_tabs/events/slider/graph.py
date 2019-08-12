import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt

from app.func import Func


def Snow(w, h):
    stim = np.random.rand(w, h)
    stim[stim <=  0.5]  = 0
    stim[stim >   0.5] = 255
    # vmax = stim[0][0]
    # vmin = stim[0][0]
    # for i in stim.shape():
    #     for j in i:
            # if j > vmax:
            #     vmax = j
            # if j < vmin:
            #     vmin = j
    return stim


def makeGabor_bcl(cyclesPerPix, Contrast, phase, orientation, bkColor, width, height,
                  SDx, SDy):
    phase = (phase % 360) * (np.pi / 180)
    orientation = (orientation % 360) * (np.pi / 180)

    # pixelsPerPeriod = (1 / cyclesPerPix)

    # gaussianSpaceConstant = periodsCoveredByOneStandardDeviation * pixelsPerPeriod

    radius = (int(width / 2.0), int(height / 2.0))

    [x, y] = np.meshgrid(range(-radius[0], radius[0] + 1), range(-radius[1], radius[1] + 1))

    cicleMask = (x / radius[0]) ** 2 + (y / radius[1]) ** 2

    cicleMask = cicleMask >= 1

    xm = (x) * np.cos(orientation) - (y) * np.sin(orientation)
    ym = (x) * np.sin(orientation) + (y) * np.cos(orientation)

    circularGaussianMaskMatrix = np.exp(-((xm / SDx) ** 2 + (ym / SDy) ** 2) / 2)
    circularGaussianMaskMatrix[cicleMask] = 0

    f = 2 * np.pi * cyclesPerPix
    a = np.cos(orientation) * f
    b = np.sin(orientation) * f

    layer = 255 * circularGaussianMaskMatrix * (np.cos(a * x + b * y + phase) * Contrast + 1.0) / 2.0

    stim = np.zeros((height + 1, width + 1, 3))

    for i in range(height + 1):
        for j in range(width + 1):
            for k in range(3):
                stim[i, j, k] = layer[i, j]

    for iDim in range(0, np.size(bkColor)):
        stim[:, :, iDim] = stim[:, :, iDim] + (1 - circularGaussianMaskMatrix) * bkColor[iDim]


    #
    # figure = plt.figure(figsize=(width /100, height/100))
    # ax = figure.add_subplot(1, 1, 1, position=[0, 0, 1, 1])
    # plt.xticks(())
    # plt.yticks(())
    # ax.imshow(stim / 255)
    # plt.savefig(Func.getImage("gabor1.png"))
    # plt.close()

    return stim
