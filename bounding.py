import stl_tools as su
from matplotlib import pyplot
import numpy as np
import os
import sys

from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def cuboid_data2(o, size=(1, 1, 1)):
    X = [[[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],
         [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
         [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
         [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
         [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
         [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]]
    X = np.array(X).astype(float)
    for i in range(3):
        X[:, :, i] *= size[i]
    X += np.array(o)
    return X


def plotCubeAt2(positions, sizes=None, colors=None, **kwargs):
    if not isinstance(colors, (list, np.ndarray)):
        colors = ["C0"] * len(positions)
    if not isinstance(sizes, (list, np.ndarray)):
        sizes = [(1, 1, 1)] * len(positions)
    g = []
    for p, s, c in zip(positions, sizes, colors):
        g.append(cuboid_data2(p, size=s))
    return Poly3DCollection(np.concatenate(g),
                            facecolors=np.repeat(colors, 6),
                            alpha=0.2,
                            **kwargs)


def plot(mesh_un, fname, folder):

    fig = pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')
    # = elliptical cylinder about z-axis 1

    # ax.plot_surface(x, y, z, linewidth=1, color='red', alpha=0.7)

    ax.scatter(mesh_un[:, 0], mesh_un[:, 1], mesh_un[:, 2], s=1)
    # ax.scatter(centreX, centreY, mid, s=5, c='g')

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    # rotate the axes and update

    # positions = [(-3,5,-2),(1,7,1)]
    # sizes = [(4,5,3), (3,3,7)]
    # colors = ["crimson","limegreen"]
    mesh_left_half = su.get_half_points(mesh_un, 0, su.get_extent(mesh_un, 0),
                                        0)
    mesh_right_half = su.get_half_points(mesh_un, 1, su.get_extent(mesh_un, 0),
                                         0)

    positions = [
        # su.boundingorigin(mesh_un),
        su.boundingorigin(mesh_left_half),
        su.boundingorigin(mesh_right_half)
    ]
    sizes = [
        # su.boundingsize(mesh_un),
        su.boundingsize(mesh_left_half),
        su.boundingsize(mesh_right_half)
    ]
    print("positions = " + str(positions))
    print("sizes = " + str(sizes))
    colors = ["crimson", "green"]
    pc = plotCubeAt2(positions, sizes, colors=colors, edgecolor="k")
    ax.add_collection3d(pc)

    pyplot.savefig(folder + "/" + fname + '_persp.png')
    ax.view_init(0, 0)
    # pyplot.show()
    pyplot.savefig(folder + "/" + fname + '_0_0.png')

    ax.view_init(0, 90)

    pyplot.savefig(folder + "/" + fname + '_0_90.png')

    ax.view_init(90, 0)

    pyplot.savefig(folder + "/" + fname + '_90_0.png')


if __name__ == "__main__":
    os.chdir(sys.argv[1])
    folder = "boundingcube"
    if folder not in os.listdir(sys.argv[1]):
        os.mkdir(sys.argv[1] + "/" + folder)
    for filename in sorted(os.listdir(sys.argv[1])):
        if filename.endswith(".stl"):
            mesh_un = su.get_uniq_pc(filename)
            plot(mesh_un, filename, folder)
