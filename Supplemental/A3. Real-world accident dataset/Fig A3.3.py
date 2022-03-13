# -*- coding: utf-8 -*-
'''
-------------------------------------------------------------------------------------------------
This code accompanies the paper titled "Human injury-based safety decision of automated vehicles"
Author: Qingfan Wang, Qing Zhou, Miao Lin, Bingbing Nie
Corresponding author: Bingbing Nie (nbb@tsinghua.edu.cn)
-------------------------------------------------------------------------------------------------
'''


import numpy as np
import seaborn as sns
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt


def main():
    ''' Plot Fig A3.3. '''

    # Load data.
    data = np.load('data/data.npy')

    # Process data.
    ISS = []
    for i in range(len(data)):
        if data[i, 9] < 0.5:
            ISS.append('0')
        elif 0.5 < data[i, 9] < 1.5:
            ISS.append('1-3')
        elif 1.5 < data[i, 9] < 2.5:
            ISS.append('4-14')
        elif 2.5 < data[i, 9]:
            ISS.append('15-75')

    # transfer to dataFrame.
    dic1 = {'deltaV': data[:, 0], 'angle': data[:, 1], 'ISS': ISS}
    df = pd.DataFrame(dic1)

    # Plot.
    h = sns.jointplot(data=df, x='deltaV', y='angle', hue="ISS", kind="scatter", xlim=[0, 120], ylim=[-185, 185], s=15,
                      palette=['#48CAE4', '#0096C3', '#0078B7', '#00609E'], legend=False)

    # Basic figure setting.
    matplotlib.rcParams['font.family'] = 'Arial'
    matplotlib.rcParams['font.size'] = 16
    h.ax_joint.set_xlabel('Delta-v [m/s]', family='Arial', fontsize=16)
    h.ax_joint.set_ylabel('Collision Angle [°]', family='Arial', fontsize=16)
    h.ax_joint.set_xticks(range(0, 121, 20))
    h.ax_joint.set_xticklabels(np.arange(0, 31, 5), family='Arial', fontsize=14)
    h.ax_joint.set_yticks(np.arange(-180, 181, 45))
    h.ax_joint.set_yticklabels(np.arange(-180, 181, 45), family='Arial', fontsize=14)

    # Show.
    # plt.show()
    plt.savefig('Fig A3_3.png', dpi=600)
    plt.close()


if __name__ == "__main__":
    main()
