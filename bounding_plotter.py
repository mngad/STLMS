import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd

pointsize = 2
alphaval = 0.5


if __name__ == "__main__":
    os.chdir(sys.argv[1])
    fig = plt.figure(1)
    filelist = []
    allfilelist = sorted(os.listdir(sys.argv[1]))
    for filename in allfilelist:
        if filename.endswith(".csv"):
            filelist.append(filename)

    print(filelist)
    # data to plot
    n_groups = 8
    mpl.rcParams.update({'font.size': 16})

    frames = []

    for f in filelist:
        df = pd.read_csv(
            sys.argv[1] + "/" + f,
            header=None,
            sep=',')

        print(df)
        df_transposed = df.T

        new_header = df_transposed.iloc[0]  # grab the first row for the header
        df_transposed = df_transposed[1:]  # take the data less the header row
        df_transposed.columns = new_header  # set the header row as the df
        # header

        frames.append(df_transposed)

    df_concated = pd.concat(frames)
    print(df_concated)

    x_pos = np.arange(len(df_concated.columns))

    print(df_concated.mean(axis=0))
    fig, ax = plt.subplots()
    ax.bar(x_pos, df_concated.mean(axis=0), yerr=df_concated.std(
        axis=0), align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_ylabel('Length (mm)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(df_concated.columns)
    ax.yaxis.grid(True)

    # Save the figure and show
    plt.tight_layout()
    plt.savefig('bar_plot_with_error_bars.png')
    plt.show()

    # plt.show()
    # plt.savefig('foss_05_1.png', dpi=None, facecolor='w', edgecolor='w',
    #         orientation='landscape', papertype=None, format=None,
    #         transparent=False, bbox_inches=None, pad_inches=1,
    #         frameon=None)
