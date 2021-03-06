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


def get_mesh_parts(mesh_un, fname, folder):

    mesh_left_half = su.get_half_points(mesh_un, 0, su.get_extent(mesh_un, 0),
                                        0)
    mesh_right_half = su.get_half_points(mesh_un, 1, su.get_extent(mesh_un, 0),
                                         0)
    mesh_right_cond = su.get_condyle(mesh_right_half,
                                     su.get_extent(mesh_right_half, 1),
                                     0)

    mesh_left_cond = su.get_condyle(mesh_left_half,
                                    su.get_extent(mesh_left_half, 1),
                                    1)

    mesh_left_cond_thirds = su.split_into_thirds(
        mesh_left_cond, 1)
    mesh_right_cond_thirds = su.split_into_thirds(
        mesh_right_cond, 1)
    mesh_left_cond_thirds_x = su.split_into_thirds(
        mesh_left_cond, 0)
    mesh_right_cond_thirds_x = su.split_into_thirds(
        mesh_right_cond, 0)
    mesh_un_thirds = su.split_into_thirds(mesh_un, 1)

    mesh_un_middline = su.get_mid_array(mesh_un, 2, "y")
    mesh_un_thirds_middline = []
    for i in mesh_un_thirds:
        mesh_un_thirds_middline.append(su.get_mid_array(i, 2, "y"))

    mesh_left_cond_thirds_x_middline = []
    for i in mesh_left_cond_thirds_x:
        mesh_left_cond_thirds_x_middline.append(su.get_mid_array(i, 2, "x"))

    mesh_left_cond_thirds_middline = []
    for i in mesh_left_cond_thirds:
        mesh_left_cond_thirds_middline.append(su.get_mid_array(i, 2, "y"))

    mesh_right_cond_thirds_x_middline = []
    for i in mesh_right_cond_thirds_x:
        mesh_right_cond_thirds_x_middline.append(su.get_mid_array(i, 2, "x"))

    mesh_right_cond_thirds_middline = []
    for i in mesh_right_cond_thirds:
        mesh_right_cond_thirds_middline.append(su.get_mid_array(i, 2, "y"))

    all_measurments = []

    all_measurments.append(get_measurements(mesh_un_middline, "FCW", 0))
    all_measurments.append(get_measurements(mesh_un_thirds_middline[2], "FCWA",
                                            0))
    all_measurments.append(get_measurements(mesh_un_thirds_middline[0], "FCWP",
                                            0))
    all_measurments.append(get_measurements(mesh_left_cond_thirds_middline[1],
                                            "Left FW", 0))
    all_measurments.append(get_measurements(mesh_left_cond_thirds_middline[2],
                                            "Left FWA", 0))
    all_measurments.append(get_measurements(mesh_left_cond_thirds_middline[0],
                                            "Left FWP", 0))
    all_measurments.append(get_measurements(mesh_left_cond_thirds_x_middline[1],
                                            "Left FL", 1))
    all_measurments.append(get_measurements(mesh_left_cond_thirds_x_middline[2],
                                            "Left FLM", 1))
    all_measurments.append(get_measurements(mesh_left_cond_thirds_x_middline[0],
                                            "Left FLL", 1))
    all_measurments.append(get_measurements(mesh_right_cond_thirds_middline[1],
                                            "Right FW", 0))
    all_measurments.append(get_measurements(mesh_right_cond_thirds_middline[2],
                                            "Right FWA", 0))
    all_measurments.append(get_measurements(mesh_right_cond_thirds_middline[0],
                                            "Right FWP", 0))
    all_measurments.append(get_measurements(mesh_right_cond_thirds_x_middline[1],
                                            "Right FL", 1))
    all_measurments.append(get_measurements(mesh_right_cond_thirds_x_middline[2],
                                            "Right FLM", 1))
    all_measurments.append(get_measurements(mesh_right_cond_thirds_x_middline[0],
                                            "Right FLL", 1))

    export_to_csv(fname, folder, all_measurments)


def plot(mesh_un, fname, folder):

    fig = pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(mesh_un[:, 0], mesh_un[:, 1], mesh_un[:, 2], s=1)

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
    mesh_right_cond = su.get_condyle(mesh_right_half,
                                     su.get_extent(mesh_right_half, 1),
                                     0)

    mesh_left_cond = su.get_condyle(mesh_left_half,
                                    su.get_extent(mesh_left_half, 1),
                                    1)

    mesh_left_cond_thirds = su.split_into_thirds(
        mesh_left_cond, 1)
    mesh_right_cond_thirds = su.split_into_thirds(
        mesh_right_cond, 1)
    mesh_left_cond_thirds_x = su.split_into_thirds(
        mesh_left_cond, 0)
    mesh_right_cond_thirds_x = su.split_into_thirds(
        mesh_right_cond, 0)
    mesh_un_thirds = su.split_into_thirds(mesh_un, 1)

    # mesh_un_middline = su.get_mid_array(mesh_un, 2, "y")
    mesh_un_thirds_middline = []
    for i in mesh_un_thirds:
        mesh_un_thirds_middline.append(su.get_mid_array(i, 2, "y"))

    mesh_left_cond_thirds_x_middline = []
    for i in mesh_left_cond_thirds_x:
        mesh_left_cond_thirds_x_middline.append(su.get_mid_array(i, 2, "x"))

    mesh_left_cond_thirds_middline = []
    for i in mesh_left_cond_thirds:
        mesh_left_cond_thirds_middline.append(su.get_mid_array(i, 2, "y"))

    mesh_right_cond_thirds_x_middline = []
    for i in mesh_right_cond_thirds_x:
        mesh_right_cond_thirds_x_middline.append(su.get_mid_array(i, 2, "x"))

    mesh_right_cond_thirds_middline = []
    for i in mesh_right_cond_thirds:
        mesh_right_cond_thirds_middline.append(su.get_mid_array(i, 2, "y"))

    positions = [
        su.boundingorigin(mesh_right_cond_thirds_middline[0]),
        su.boundingorigin(mesh_right_cond_thirds_middline[1]),
        su.boundingorigin(mesh_right_cond_thirds_middline[2])
    ]
    sizes = [
        su.boundingsize(mesh_right_cond_thirds_middline[0]),
        su.boundingsize(mesh_right_cond_thirds_middline[1]),
        su.boundingsize(mesh_right_cond_thirds_middline[2])
    ]

    # print("positions = " + str(positions))
    # print("sizes = " + str(sizes))
    colors = ["crimson", "green", "red", "blue", "yellow", "purple", "orange"]
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


def get_measurements(mesh, name, axis):
    # get (and print) the measurements according to Elsner et al 2010

    measure = abs(su.get_extent(mesh, axis)[1] - su.get_extent(mesh, axis)[0])
    string = name + ", " + str(measure) + "\n"
    print(string)
    return string


def export_to_csv(stl_name, folder, string):
    f = open(folder + "/" + stl_name[:-4] + ".csv", "w")
    print(folder + "/" + stl_name[:-4] + ".csv")
    full_string = ""
    for i in string:
        full_string = full_string + str(i)
    f.write(full_string)
    f.close()


if __name__ == "__main__":
    os.chdir(sys.argv[1])
    for filename in sorted(os.listdir(sys.argv[1])):
        if filename.endswith(".stl"):
            print(filename)
            mesh_un = su.get_uniq_pc(filename)
            mesh_zeroed = su.reposition(mesh_un)
            # plot(mesh_zeroed, filename, folder)
            get_mesh_parts(mesh_zeroed, filename, sys.argv[1])
