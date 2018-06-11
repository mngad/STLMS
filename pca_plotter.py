import os
import sys
import stl_tools as su
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

pointsize = 2
alphaval = 0.5


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
            midarrayz = su.get_mid_array(vbmesh_un, 'all', 'z')

            plt.scatter(
                midarrayz[:, 0],
                midarrayz[:, 1],
                s=pointsize,
                alpha=alphaval,
                lw=0,
                label=filename[:-4].replace('_', ' '))

    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.legend(markerscale=6)
    plt.savefig(PCName + '_Axial.eps', dpi=320, facecolor='w', edgecolor='w',
        orientation='landscape', format=None,
        transparent=False, bbox_inches=None, pad_inches=1,
        frameon=None)
    plt.savefig(PCName + '_Axial.png', dpi=320, facecolor='w', edgecolor='w',
        orientation='landscape', format=None,
        transparent=False, bbox_inches=None, pad_inches=1,
        frameon=None)
    #plt.show()
    fig = plt.figure(2)

    for filename in filelist:
        if filename.endswith(".stl"):

            vbmesh_un = su.get_uniq_pc(filename)
            midarrayz = su.get_mid_array(vbmesh_un, 'all', 'x')

            plt.scatter(
                midarrayz[:, 1],
                midarrayz[:, 2],
                s=pointsize,
                alpha=alphaval,
                lw=0,
                label=filename[:-4].replace('_', ' '))

    plt.xlabel('Y axis')
    plt.ylabel('Z axis')
    plt.legend(markerscale=6)
    #plt.show()
    plt.savefig(PCName + '_Sagital.eps', dpi=320, facecolor='w', edgecolor='w',
        orientation='landscape', format=None,
        transparent=False, bbox_inches=None, pad_inches=1,
        frameon=None)
    plt.savefig(PCName + '_Sagital.png', dpi=320, facecolor='w', edgecolor='w',
        orientation='landscape', format=None,
        transparent=False, bbox_inches=None, pad_inches=1,
        frameon=None)
    fig = plt.figure(3)

    for filename in filelist:
        if filename.endswith(".stl"):

            vbmesh_un = su.get_uniq_pc(filename)
            midarrayz = su.get_mid_array(vbmesh_un, 'all', 'y')

            plt.scatter(
                midarrayz[:, 0],
                midarrayz[:, 2],
                s=pointsize,
                alpha=alphaval,
                lw=0,
                label=filename[:-4].replace('_', ' '))

    plt.xlabel('X axis')
    plt.ylabel('Z axis')
    plt.legend(markerscale=6)
    plt.savefig(PCName + '_Coronal.eps', dpi=320, facecolor='w', edgecolor='w',
        orientation='landscape', format=None,
        transparent=False, bbox_inches=None, pad_inches=1,
        frameon=None)
    plt.savefig(PCName + '_Coronal.png', dpi=320, facecolor='w', edgecolor='w',
        orientation='landscape', format=None,
        transparent=False, bbox_inches=None, pad_inches=1,
        frameon=None)
    #plt.show()


    fig = plt.figure(4)
    ax = fig.add_subplot(111, projection='3d')
    for filename in filelist:
        if filename.endswith(".stl"):

            vbmesh_un = su.get_uniq_pc(filename)
            midarrayz = su.get_mid_array(vbmesh_un, 'all', 'y')

            ax.scatter(
                vbmesh_un[:, 0],
                vbmesh_un[:, 1],
                vbmesh_un[:, 2],
                zdir='z',
                s=2,
                alpha=0.5,
                lw=0,
                depthshade=True,
                label=filename[:-4].replace('_', ' ')
                )

    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.ylabel('Z axis')
    ax.legend(markerscale=6)
    #plt.legend()
    plt.savefig(PCName + '_3d.eps', dpi=320, facecolor='w', edgecolor='w',
        orientation='landscape', format=None,
        transparent=False, bbox_inches=None, pad_inches=1,
        frameon=None)
    plt.savefig(PCName + '_3d.png', dpi=320, facecolor='w', edgecolor='w',
        orientation='landscape', format=None,
        transparent=False, bbox_inches=None, pad_inches=1,
        frameon=None)
    #plt.show()
