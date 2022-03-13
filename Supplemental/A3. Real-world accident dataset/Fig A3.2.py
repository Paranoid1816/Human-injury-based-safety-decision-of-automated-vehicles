# -*- coding: utf-8 -*-
'''
-------------------------------------------------------------------------------------------------
This code accompanies the paper titled "Human injury-based safety decision of automated vehicles"
Author: Qingfan Wang, Qing Zhou, Miao Lin, Bingbing Nie
Corresponding author: Bingbing Nie (nbb@tsinghua.edu.cn)
-------------------------------------------------------------------------------------------------
'''


import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.neighbors import KernelDensity


def main():
    ''' Plot Fig A3.2. '''

    # Load general data.
    data = np.load('data/data.npy')


    ''' Show Table A3.1. '''
    print(np.around(np.average(data[:, 0]), decimals=2), np.around(np.std(data[:, 0]), decimals=2))  # collision delta-v
    print(np.around(np.average(data[:, 1]), decimals=2), np.around(np.std(data[:, 1]), decimals=2))  # collision angle
    print(Counter(data[:, 2]))  # PoI of the ego vehicle
    print(Counter(data[:, 3]))  # PoI of the opposing vehicle
    print(Counter(data[:, 4]))  # occupant age
    print(np.around(np.average(data[:, 11]), decimals=2), np.around(np.std(data[:, 11]), decimals=2))  # occupant age
    print(Counter(data[:, 5]))  # occupant gender
    print(Counter(data[:, 6]))  # belt usage
    print(Counter(data[:, 7]))  # airbag usage
    print(Counter(data[:, 8]))  # vehicle mass ratio
    print(np.around(np.average(data[:, 12]), decimals=2), np.around(np.std(data[:, 12]), decimals=2))  # vehicle mass ratio

    print(np.around(np.average(data[:, 10]), decimals=2), np.around(np.std(data[:, 10]), decimals=2))  # occupant ISS (as a continuous variable)
    print(Counter(data[:, 9]))  # occupant ISS (as a discrete variable)
    print(np.around(np.average(data[:, 10][data[:, 9] == 0]), decimals=2), np.around(np.std(data[:, 10][data[:, 9] == 0]), decimals=2))
    print(np.around(np.average(data[:, 10][data[:, 9] == 1]), decimals=2), np.around(np.std(data[:, 10][data[:, 9] == 1]), decimals=2))
    print(np.around(np.average(data[:, 10][data[:, 9] == 2]), decimals=2), np.around(np.std(data[:, 10][data[:, 9] == 2]), decimals=2))
    print(np.around(np.average(data[:, 10][data[:, 9] == 3]), decimals=2), np.around(np.std(data[:, 10][data[:, 9] == 3]), decimals=2))


    ''' Plot Fig A3.2. '''

    # Basic setup.
    fig1 = plt.figure(figsize=(12, 5))
    font1 = {'family': 'Arial', 'size': 16}
    plt.subplots_adjust(left=0.08, wspace=0.24, hspace=0.4, bottom=0.12, top=0.96, right=0.97)


    ''' Plot Fig A3.2.1. '''

    # Basic setup.
    ax1 = fig1.add_subplot(221)
    plt.xlabel('Delta-v [m/s]', font1)
    plt.ylabel('Frequency', font1)
    plt.xticks(range(0, 139, 20), range(0, 31, 5), family='Arial', fontsize=14)
    plt.yticks(family='Arial', fontsize=14)
    plt.xlim([0, 120])

    # Plot histogram.
    plt.hist(data[:, 0], np.arange(0, 139, 3), histtype='bar', rwidth=0.8, color='#48CAE4')

    # Plot kde curve.
    X_plot = np.arange(0, 139, 0.1)[:, np.newaxis]
    kde = KernelDensity(kernel='gaussian', bandwidth=2).fit(data[:, 0][:, np.newaxis])
    log_dens = kde.score_samples(X_plot)
    plt.plot(X_plot[:, 0], np.exp(log_dens) * len(data) * 3, color='tomato')


    ''' Plot Fig A3.2.2. '''

    # Basic setup.
    ax2 = fig1.add_subplot(222)
    plt.xlabel('Collision Angle [°]', font1)
    plt.ylabel('Frequency', font1)
    plt.xticks(range(-180, 181, 45), family='Arial', fontsize=14)
    plt.yticks(family='Arial', fontsize=14)
    plt.ylim([0, 1500])

    # Plot histogram.
    angle = data[:, 1]
    plt.hist(angle, range(-185, 186, 10), histtype='bar', rwidth=0.8, color='#0096C3')

    # Plot kde curve.
    X_plot = np.arange(-180, 180, 1)[:, np.newaxis]
    kde = KernelDensity(kernel='gaussian', bandwidth=8).fit(angle[:, np.newaxis])
    log_dens = kde.score_samples(X_plot)
    plt.plot(X_plot[:, 0], np.exp(log_dens) * len(data) * 11, color='tomato')


    ''' Plot Fig A3.2.3. '''

    # Basic setup.
    ax3 = fig1.add_subplot(223)
    plt.xlabel('Occupant Age', font1)
    plt.ylabel('Frequency', font1)
    plt.xticks(family='Arial', fontsize=14)
    plt.yticks(family='Arial', fontsize=14)
    plt.ylim([0, 600])

    # Plot histogram.
    plt.hist(data[:, 11], range(16, 100, 2), histtype='bar', rwidth=0.8, color='#0078B7')

    # Plot kde curve.
    X_plot = np.arange(16, 100, 0.2)[:, np.newaxis]
    kde = KernelDensity(kernel='gaussian', bandwidth=2).fit(data[:, 11][:, np.newaxis])
    log_dens = kde.score_samples(X_plot)
    plt.plot(X_plot[:, 0], np.exp(log_dens) * len(data) * 2, color='tomato')


    ''' Plot Fig A3.2.4. '''

    # Basic setup.
    ax4 = fig1.add_subplot(224)
    plt.xlabel('Occupant ISS', font1)
    plt.ylabel('Frequency', font1)
    plt.xticks(family='Arial', fontsize=14)
    plt.yticks(family='Arial', fontsize=14)
    plt.ylim([0, 4000])

    # Plot histogram.
    plt.hist(data[:, 10], np.arange(-0.5, 75.6, 1), histtype='bar', rwidth=0.8, color='#00609E')

    # Plot kde curve.
    X_plot = np.arange(0, 75, 0.1)[:, np.newaxis]
    kde = KernelDensity(kernel='gaussian', bandwidth=0.5).fit(data[:, 10][:, np.newaxis])
    log_dens = kde.score_samples(X_plot)
    plt.plot(X_plot[:, 0], np.exp(log_dens) * len(data) * 1, color='tomato')


    # Show.
    # plt.show()
    plt.savefig('Fig A3_2_1.png', dpi=600)
    plt.close()


    ''' Plot Fig A3.2.5. '''

    # Basic setup.
    fig2 = plt.figure(figsize=(5, 2.3))
    font1 = {'family': 'Arial', 'size': 16}
    plt.subplots_adjust(left=0.12, wspace=0.24, hspace=0.4, bottom=0.12, top=0.96, right=0.97)

    plt.xlabel('Delta-v [m/s]', font1)
    plt.ylabel('Frequency', font1)
    plt.xticks(range(0, 139, 20), range(0, 31, 5), family='Arial', fontsize=14)
    plt.yticks(family='Arial', fontsize=14)
    plt.xlim([12*4-0.3, 30*4])
    plt.ylim([0, 50])

    # Plot histogram.
    plt.hist(data[:, 0], np.arange(0, 139, 3), histtype='bar', rwidth=0.8, color='#48CAE4')

    # Plot kde curve.
    X_plot = np.arange(0, 139, 0.1)[:, np.newaxis]
    kde = KernelDensity(kernel='gaussian', bandwidth=2).fit(data[:, 0][:, np.newaxis])
    log_dens = kde.score_samples(X_plot)
    plt.plot(X_plot[:, 0], np.exp(log_dens) * len(data) * 3, color='tomato')

    # Show.
    # plt.show()
    plt.savefig('Fig A3_2_2.png', dpi=600)
    plt.close()


    ''' Plot Fig A3.2.6. '''

    # Basic setup.
    fig3 = plt.figure(figsize=(6, 2))
    font1 = {'family': 'Arial', 'size': 16}
    plt.subplots_adjust(left=0.12, wspace=0.24, hspace=0.4, bottom=0.12, top=0.96, right=0.97)

    plt.xlabel('Occupant ISS', font1)
    plt.ylabel('Frequency', font1)
    plt.xticks([0, 25, 50, 75], family='Arial', fontsize=14)
    plt.yticks(family='Arial', fontsize=14)
    plt.ylim([0, 150])

    # Plot histogram.
    plt.hist(data[:, 10], np.arange(-0.5, 75.6, 5), histtype='bar', rwidth=0.8, color='#00609E')

    # Plot kde curve.
    X_plot = np.arange(0, 75, 4)[:, np.newaxis]
    kde = KernelDensity(kernel='gaussian', bandwidth=3).fit(data[:, 10][:, np.newaxis])
    log_dens = kde.score_samples(X_plot)
    plt.plot(X_plot[:, 0], np.exp(log_dens) * len(data) * 5, color='tomato')

    # Show.
    # plt.show()
    plt.savefig('Fig A3_2_3.png', dpi=600)
    plt.close()


if __name__ == "__main__":
    main()
