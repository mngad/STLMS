import os
import sys
import stl_tools as su
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import numpy as np
from matplotlib.patches import Polygon

if __name__ == "__main__":
    os.chdir(sys.argv[1])
    PCName = ''
    fig = plt.figure(1)
    filelist = []
    allfilelist = sorted(os.listdir(sys.argv[1]))
    for filename in allfilelist:
        if filename.endswith(".stl"):
            filelist.append(filename)

    #print(len(filelist))
    if sys.argv[2] == 'True':
        if len(filelist)>3:
            myorder = [2, 1, 0, 6, 3, 4, 5]
            filelist = [filelist[i] for i in myorder]
        if len(filelist)==3:
            myorder = [0, 2, 1]
            filelist = [filelist[i] for i in myorder]

    for filename in filelist:
        if filename.endswith(".stl"):
            PCName = filename[:3]
            vbmesh_un = su.get_uniq_pc(filename)
            midarrayz = su.get_mid_array(vbmesh_un, 1, 'z')
            
            plt.plot(
                midarrayz[:, 0],
                midarrayz[:, 1],
                'o',
                label=filename[:-4].replace('_', ' '))
            

    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.legend()
    plt.savefig(PCName + '_AxialSlice.eps', dpi=320, facecolor='w', edgecolor='w',
        orientation='landscape', format=None,
        transparent=False, bbox_inches=None, pad_inches=1,
        frameon=None)
    plt.savefig(PCName + '_AxialSlice.png', dpi=320, facecolor='w', edgecolor='w',
        orientation='landscape', format=None,
        transparent=False, bbox_inches=None, pad_inches=1,
        frameon=None)
    fig = plt.figure(2)

    for filename in filelist:
        if filename.endswith(".stl"):

            vbmesh_un = su.get_uniq_pc(filename)
            midarrayz = su.get_mid_array(vbmesh_un, 1, 'x')

            plt.plot(
                midarrayz[:, 1],
                midarrayz[:, 2],
                'o',
                label=filename[:-4].replace('_', ' '))

    plt.xlabel('Y axis')
    plt.ylabel('Z axis')
    plt.legend()
    plt.savefig(PCName + '_SagitalSlice.eps', dpi=320, facecolor='w', edgecolor='w',
        orientation='landscape', format=None,
        transparent=False, bbox_inches=None, pad_inches=1,
        frameon=None)
    plt.savefig(PCName + '_SagitalSlice.png', dpi=320, facecolor='w', edgecolor='w',
        orientation='landscape', format=None,
        transparent=False, bbox_inches=None, pad_inches=1,
        frameon=None)
    fig = plt.figure(3)

    for filename in filelist:
        if filename.endswith(".stl"):

            vbmesh_un = su.get_uniq_pc(filename)
            midarrayz = su.get_mid_array(vbmesh_un, 1, 'y')

            plt.plot(
                midarrayz[:, 0],
                midarrayz[:, 2],
                'o',
                label=filename[:-4].replace('_', ' '))

    plt.xlabel('X axis')
    plt.ylabel('Z axis')
    plt.legend()
    plt.savefig(PCName + '_CoronalSlice.eps', dpi=320, facecolor='w', edgecolor='w',
        orientation='landscape', format=None,
        transparent=False, bbox_inches=None, pad_inches=1,
        frameon=None)
    plt.savefig(PCName + '_CoronalSlice.png', dpi=320, facecolor='w', edgecolor='w',
        orientation='landscape', format=None,
        transparent=False, bbox_inches=None, pad_inches=1,
        frameon=None)
    #plt.show()
