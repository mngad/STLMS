import os
import sys
import stl_tools as su
import matplotlib.pyplot as plt

if __name__ == "__main__":
    os.chdir(sys.argv[1])
    PCName = ''
    fig = plt.figure(1)
    filelist = []
    allfilelist = sorted(os.listdir(sys.argv[1]))
    for filename in allfilelist:
        if filename.endswith(".stl"):
            filelist.append(filename)

    print(len(filelist))
    if sys.argv[2] == 'True':
        myorder = [2, 1, 0, 6, 3, 4, 5]
        filelist = [filelist[i] for i in myorder]

    for filename in filelist:
        if filename.endswith(".stl"):
            PCName = filename[:3]
            vbmesh_un = su.get_uniq_pc(filename)
            midarrayz = su.get_mid_array(vbmesh_un, 1, 'z')

            plt.scatter(
                midarrayz[:, 0],
                midarrayz[:, 1],
                s=1,
                label=filename[:-4].replace('_', ' '))

    plt.xlabel('X axis')
    plt.ylabel('Y')
    plt.legend()
    plt.savefig(PCName + '_Axial')
    plt.show()
    fig = plt.figure(2)

    for filename in filelist:
        if filename.endswith(".stl"):

            vbmesh_un = su.get_uniq_pc(filename)
            midarrayz = su.get_mid_array(vbmesh_un, 1, 'x')

            plt.scatter(
                midarrayz[:, 1],
                midarrayz[:, 2],
                s=1,
                label=filename[:-4].replace('_', ' '))

    plt.xlabel('Y')
    plt.ylabel('Z axis')
    plt.legend()
    plt.show()
    plt.savefig(PCName + '_Sagital')
    fig = plt.figure(3)

    for filename in filelist:
        if filename.endswith(".stl"):

            vbmesh_un = su.get_uniq_pc(filename)
            midarrayz = su.get_mid_array(vbmesh_un, 1, 'y')

            plt.scatter(
                midarrayz[:, 0],
                midarrayz[:, 2],
                s=1,
                label=filename[:-4].replace('_', ' '))

    plt.xlabel('X axis')
    plt.ylabel('Z axis')
    plt.legend()
    plt.savefig(PCName + '_Coronal')
    plt.show()
