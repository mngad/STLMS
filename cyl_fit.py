import stl_uniq as su
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import os
import sys



def measure_vb(vbmesh_un, filename):

    zmin = min(vbmesh_un[:, 2])
    zmax = max(vbmesh_un[:, 2])
    mid = (zmax - zmin) / 2 + zmin
    count = 0
    for i in range(len(vbmesh_un)):
        if (vbmesh_un[i, 2] <= mid + 0.5 and vbmesh_un[i, 2] >= mid - 0.5):
            #print(vbmesh_un[i])
            count += 1

    midarray = np.zeros((count, 3))
    a = 0
    for i in range(len(vbmesh_un)):
        if (vbmesh_un[i, 2] <= mid + 0.5 and vbmesh_un[i, 2] >= mid - 0.5):
            #print(vbmesh_un[i])
            midarray[a] = vbmesh_un[i]
            a += 1

    midxmin = min(midarray[:, 0])
    midxmax = max(midarray[:, 0])
    midymin = min(midarray[:, 1])
    midymax = max(midarray[:, 1])
    centreX = (midxmax - midxmin) / 2 + midxmin

    for i in range(len(midarray)):
        if (midarray[i, 0] >= centreX - 1 and midarray[i, 0] <= centreX + 1 and
                midarray[i, 1] <= ((midymax - midymin) / 2 + midymin)):
            midymintrue = midarray[i, 1]
    for i in range(len(midarray)):
        if (midarray[i, 0] >= centreX - 1 and midarray[i, 0] <= centreX + 1 and
                midarray[i, 1] >= ((midymax - midymin) / 2 + midymin)):
            midymaxtrue = midarray[i, 1]

    centreY = (midymaxtrue - midymintrue) / 2 + midymintrue

    for i in range(len(midarray)):
        if (midarray[i, 1] >= centreY - 1 and midarray[i, 1] <= centreY + 1 and
                midarray[i, 0] <= ((midxmax - midxmin) / 2 + midxmin)):
            midxmintrue = midarray[i, 0]
    for i in range(len(midarray)):
        if (midarray[i, 1] >= centreY - 1 and midarray[i, 1] <= centreY + 1 and
                midarray[i, 0] >= ((midxmax - midxmin) / 2 + midxmin)):
            midxmaxtrue = midarray[i, 0]
    centreX = (midxmaxtrue - midxmintrue) / 2 + midxmintrue

    currsmallest = zmax
    currsmallestind = 0
    for i in range(len(vbmesh_un)):
        if (vbmesh_un[i, 2] > mid and vbmesh_un[i, 1] <= centreY + 8 and
                vbmesh_un[i, 1] >= centreY - 8 and
                vbmesh_un[i, 0] <= centreX + 8 and
                vbmesh_un[i, 0] >= centreX - 8):
            if (vbmesh_un[i, 2] <= currsmallest):
                currsmallest = vbmesh_un[i, 2]
                currsmallestin = i

    topInternal = vbmesh_un[currsmallestin, 2]

    currsmallest = zmin
    currsmallestind = 0
    for i in range(len(vbmesh_un)):
        if (vbmesh_un[i, 2] < mid and vbmesh_un[i, 1] <= centreY + 8 and
                vbmesh_un[i, 1] >= centreY - 8 and
                vbmesh_un[i, 0] <= centreX + 8 and
                vbmesh_un[i, 0] >= centreX - 8):
            if (vbmesh_un[i, 2] >= currsmallest):
                currsmallest = vbmesh_un[i, 2]
                currsmallestin = i

    bottomInternal = vbmesh_un[currsmallestin, 2]
    a = midxmintrue - centreX
    b = midymintrue - centreY
    x = a * np.cos(np.linspace(0, -np.pi * 2.0, 50)) + centreX
    z = np.linspace(bottomInternal, topInternal, 50)
    x, z = np.meshgrid(x, z)
    y = b * np.sin(np.linspace(0, -np.pi * 2.0, 50)) + centreY
    get_volume(a, b, topInternal - bottomInternal, filename)
    return midarray, centreX, centreY, mid, x, y, z


def plot(midarray, centreX, centreY, mid, x, y, z, fname):

    fig = pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')
    #= elliptical cylinder about z-axis 1

    ax.plot_surface(x, y, z, linewidth=1, color='red', alpha=0.7)

    ax.scatter(midarray[:, 0], midarray[:, 1], midarray[:, 2], s=2, c='r')
    ax.scatter(vbmesh_un[:, 0], vbmesh_un[:, 1], vbmesh_un[:, 2], s=1)
    ax.scatter(centreX, centreY, mid, s=5, c='g')

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    # rotate the axes and update
    ax.view_init(0, 0)
    pyplot.savefig(fname + '_0_0.eps')
    pyplot.savefig(fname + '_0_0.png')

    ax.view_init(0, 90)
    pyplot.savefig(fname + '_0_90.eps')
    pyplot.savefig(fname + '_0_90.png')

    ax.view_init(90, 0)
    pyplot.savefig(fname + '_90_0.eps')
    pyplot.savefig(fname + '_90_0.png')


def get_volume(a, b, h, fname):
    print(fname + ", " + str(np.pi * a * b * h))

    with open("cyl_fit.txt", "a") as myfile:
        myfile.write(fname + ", " + str(np.pi * a * b * h) + "\n")

    return np.pi * a * b * h


if __name__ == "__main__":
    os.chdir(sys.argv[1])
    for filename in sorted(os.listdir(sys.argv[1])):
        if filename.endswith(".stl"):

            vbmesh_un = su.get_uniq_pc(filename)
            midarray, centreX, centreY, mid, x, y, z = measure_vb(
                vbmesh_un, filename[:-4])
            plot(midarray, centreX, centreY, mid, x, y, z, filename[:-4])
