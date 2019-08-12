import numpy as np

def Snow(w, h, isBool = False):
    stim = np.random.rand(w, h)
    stim = stim * 255
    if isBool:
        stim[stim <=  0.5]  = 0
        stim[stim >   0.5]  = 255

    return stim


def makeGabor_bcl(cyclesPerPix, Contrast, phase, orientation, bkColor, width, height,
                  SDx, SDy):
    phase       = (phase % 360) * (np.pi / 180)

    orientation = (orientation % 360) * (np.pi / 180)

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

    return stim
