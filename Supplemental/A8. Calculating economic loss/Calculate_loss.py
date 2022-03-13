# -*- coding: utf-8 -*-
'''
-------------------------------------------------------------------------------------------------
This code accompanies the paper titled "Human injury-based safety decision of automated vehicles"
Author: Qingfan Wang, Qing Zhou, Miao Lin, Bingbing Nie
Corresponding author: Bingbing Nie (nbb@tsinghua.edu.cn)
-------------------------------------------------------------------------------------------------
'''


import numpy as np
import xlwt


np.set_printoptions(suppress=True)


def main():
    ''' Calculate and save the equivalent economic loss. '''

    # Load parameters.
    cost_floor = np.load('para/inj_cost_floor.npy')
    cost_ceiling = np.load('para/inj_cost_ceiling.npy')

    # Load data.
    Inj_list = np.load('data/Inj_list.npz')

    # Define economic loss of different levels and types.
    Cost_EB_med_1 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_EB_mon_1 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_EB_all_1 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_EB_med_2 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_EB_mon_2 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_EB_all_2 = np.ones((11, 4 * 50 * 2)) * (-1)

    Cost_S1_med_1 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_S1_mon_1 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_S1_all_1 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_S1_med_2 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_S1_mon_2 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_S1_all_2 = np.ones((11, 4 * 50 * 2)) * (-1)

    Cost_S2_med_1 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_S2_mon_1 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_S2_all_1 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_S2_med_2 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_S2_mon_2 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_S2_all_2 = np.ones((11, 4 * 50 * 2)) * (-1)

    Cost_S3_med_1 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_S3_mon_1 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_S3_all_1 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_S3_med_2 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_S3_mon_2 = np.ones((11, 4 * 50 * 2)) * (-1)
    Cost_S3_all_2 = np.ones((11, 4 * 50 * 2)) * (-1)

    # Calculate economic loss case by case.
    for Num_file in range(50):
        for Num_ext in range(4):
            for veh in [0, 1]:
                # Load injury data from the IRM algorithm.
                inj_EB = Inj_list['inj_EB'][Num_ext + Num_file * 4 + veh * 200]
                inj_S1 = Inj_list['inj_S1'][Num_ext + Num_file * 4 + veh * 200]
                inj_S2 = Inj_list['inj_S2'][Num_ext + Num_file * 4 + veh * 200]
                inj_S3 = Inj_list['inj_S3'][Num_ext + Num_file * 4 + veh * 200]

                # Calculate economic loss.
                cost_EB_med_1 = cost_floor[0, 0] * inj_EB[1] + cost_floor[0, 1] * inj_EB[2] + cost_floor[0, 2] * inj_EB[3]
                cost_EB_mon_1 = cost_floor[1, 0] * inj_EB[1] + cost_floor[1, 1] * inj_EB[2] + cost_floor[1, 2] * inj_EB[3]
                cost_EB_all_1 = cost_floor[2, 0] * inj_EB[1] + cost_floor[2, 1] * inj_EB[2] + cost_floor[2, 2] * inj_EB[3]
                cost_EB_med_2 = cost_ceiling[0, 0] * inj_EB[1] + cost_ceiling[0, 1] * inj_EB[2] + cost_ceiling[0, 2] * inj_EB[3]
                cost_EB_mon_2 = cost_ceiling[1, 0] * inj_EB[1] + cost_ceiling[1, 1] * inj_EB[2] + cost_ceiling[1, 2] * inj_EB[3]
                cost_EB_all_2 = cost_ceiling[2, 0] * inj_EB[1] + cost_ceiling[2, 1] * inj_EB[2] + cost_ceiling[2, 2] * inj_EB[3]

                cost_S1_med_1 = cost_floor[0, 0] * inj_S1[1] + cost_floor[0, 1] * inj_S1[2] + cost_floor[0, 2] * inj_S1[3]
                cost_S1_mon_1 = cost_floor[1, 0] * inj_S1[1] + cost_floor[1, 1] * inj_S1[2] + cost_floor[1, 2] * inj_S1[3]
                cost_S1_all_1 = cost_floor[2, 0] * inj_S1[1] + cost_floor[2, 1] * inj_S1[2] + cost_floor[2, 2] * inj_S1[3]
                cost_S1_med_2 = cost_ceiling[0, 0] * inj_S1[1] + cost_ceiling[0, 1] * inj_S1[2] + cost_ceiling[0, 2] * inj_S1[3]
                cost_S1_mon_2 = cost_ceiling[1, 0] * inj_S1[1] + cost_ceiling[1, 1] * inj_S1[2] + cost_ceiling[1, 2] * inj_S1[3]
                cost_S1_all_2 = cost_ceiling[2, 0] * inj_S1[1] + cost_ceiling[2, 1] * inj_S1[2] + cost_ceiling[2, 2] * inj_S1[3]

                cost_S2_med_1 = cost_floor[0, 0] * inj_S2[1] + cost_floor[0, 1] * inj_S2[2] + cost_floor[0, 2] * inj_S2[3]
                cost_S2_mon_1 = cost_floor[1, 0] * inj_S2[1] + cost_floor[1, 1] * inj_S2[2] + cost_floor[1, 2] * inj_S2[3]
                cost_S2_all_1 = cost_floor[2, 0] * inj_S2[1] + cost_floor[2, 1] * inj_S2[2] + cost_floor[2, 2] * inj_S2[3]
                cost_S2_med_2 = cost_ceiling[0, 0] * inj_S2[1] + cost_ceiling[0, 1] * inj_S2[2] + cost_ceiling[0, 2] * inj_S2[3]
                cost_S2_mon_2 = cost_ceiling[1, 0] * inj_S2[1] + cost_ceiling[1, 1] * inj_S2[2] + cost_ceiling[1, 2] * inj_S2[3]
                cost_S2_all_2 = cost_ceiling[2, 0] * inj_S2[1] + cost_ceiling[2, 1] * inj_S2[2] + cost_ceiling[2, 2] * inj_S2[3]

                cost_S3_med_1 = cost_floor[0, 0] * inj_S3[1] + cost_floor[0, 1] * inj_S3[2] + cost_floor[0, 2] * inj_S3[3]
                cost_S3_mon_1 = cost_floor[1, 0] * inj_S3[1] + cost_floor[1, 1] * inj_S3[2] + cost_floor[1, 2] * inj_S3[3]
                cost_S3_all_1 = cost_floor[2, 0] * inj_S3[1] + cost_floor[2, 1] * inj_S3[2] + cost_floor[2, 2] * inj_S3[3]
                cost_S3_med_2 = cost_ceiling[0, 0] * inj_S3[1] + cost_ceiling[0, 1] * inj_S3[2] + cost_ceiling[0, 2] * inj_S3[3]
                cost_S3_mon_2 = cost_ceiling[1, 0] * inj_S3[1] + cost_ceiling[1, 1] * inj_S3[2] + cost_ceiling[1, 2] * inj_S3[3]
                cost_S3_all_2 = cost_ceiling[2, 0] * inj_S3[1] + cost_ceiling[2, 1] * inj_S3[2] + cost_ceiling[2, 2] * inj_S3[3]

                # Save economic loss.
                for j in range(11):
                    Cost_EB_med_1[j, Num_ext + Num_file * 4 + veh * 200] = cost_EB_med_1[j]
                    Cost_EB_mon_1[j, Num_ext + Num_file * 4 + veh * 200] = cost_EB_mon_1[j]
                    Cost_EB_all_1[j, Num_ext + Num_file * 4 + veh * 200] = cost_EB_all_1[j]
                    Cost_EB_med_2[j, Num_ext + Num_file * 4 + veh * 200] = cost_EB_med_2[j]
                    Cost_EB_mon_2[j, Num_ext + Num_file * 4 + veh * 200] = cost_EB_mon_2[j]
                    Cost_EB_all_2[j, Num_ext + Num_file * 4 + veh * 200] = cost_EB_all_2[j]

                    Cost_S1_med_1[j, Num_ext + Num_file * 4 + veh * 200] = cost_S1_med_1[j]
                    Cost_S1_mon_1[j, Num_ext + Num_file * 4 + veh * 200] = cost_S1_mon_1[j]
                    Cost_S1_all_1[j, Num_ext + Num_file * 4 + veh * 200] = cost_S1_all_1[j]
                    Cost_S1_med_2[j, Num_ext + Num_file * 4 + veh * 200] = cost_S1_med_2[j]
                    Cost_S1_mon_2[j, Num_ext + Num_file * 4 + veh * 200] = cost_S1_mon_2[j]
                    Cost_S1_all_2[j, Num_ext + Num_file * 4 + veh * 200] = cost_S1_all_2[j]

                    Cost_S2_med_1[j, Num_ext + Num_file * 4 + veh * 200] = cost_S2_med_1[j]
                    Cost_S2_mon_1[j, Num_ext + Num_file * 4 + veh * 200] = cost_S2_mon_1[j]
                    Cost_S2_all_1[j, Num_ext + Num_file * 4 + veh * 200] = cost_S2_all_1[j]
                    Cost_S2_med_2[j, Num_ext + Num_file * 4 + veh * 200] = cost_S2_med_2[j]
                    Cost_S2_mon_2[j, Num_ext + Num_file * 4 + veh * 200] = cost_S2_mon_2[j]
                    Cost_S2_all_2[j, Num_ext + Num_file * 4 + veh * 200] = cost_S2_all_2[j]

                    Cost_S3_med_1[j, Num_ext + Num_file * 4 + veh * 200] = cost_S3_med_1[j]
                    Cost_S3_mon_1[j, Num_ext + Num_file * 4 + veh * 200] = cost_S3_mon_1[j]
                    Cost_S3_all_1[j, Num_ext + Num_file * 4 + veh * 200] = cost_S3_all_1[j]
                    Cost_S3_med_2[j, Num_ext + Num_file * 4 + veh * 200] = cost_S3_med_2[j]
                    Cost_S3_mon_2[j, Num_ext + Num_file * 4 + veh * 200] = cost_S3_mon_2[j]
                    Cost_S3_all_2[j, Num_ext + Num_file * 4 + veh * 200] = cost_S3_all_2[j]


    # Create a table.
    Deci_result = xlwt.Workbook()
    deci_result = Deci_result.add_sheet('economic loss')

    # Table header.
    deci_result.write(0, 0, 'Optimization level')
    deci_result.write(0, 1, 'Activation time [ms]')
    deci_result.write(0, 2, 'Medical cost [$]')
    deci_result.write(0, 6, 'Monetary cost [$]')
    deci_result.write(0, 10, 'Comprehensive cost [$]')
    deci_result.write(1, 2, 'Lower limit')
    deci_result.write(1, 4, 'Upper limit')
    deci_result.write(1, 6, 'Lower limit')
    deci_result.write(1, 8, 'Upper limit')
    deci_result.write(1, 10, 'Lower limit')
    deci_result.write(1, 12, 'Upper limit')
    for j in range(6):
        deci_result.write(2, 2 * (j + 1), 'Mean')
        deci_result.write(2, 2 * (j + 1) + 1, '[%]')
    deci_result.write(3, 0, 'EB')
    deci_result.write(3 + 11, 0, 'S1')
    deci_result.write(3 + 22, 0, 'S2')
    deci_result.write(3 + 33, 0, 'S3')

    for i in range(11):
        # Table header.
        deci_result.write(i + 3, 1, str(-(10 - i) * 100))
        deci_result.write(i + 3 + 11, 1, str(-(10 - i) * 100))
        deci_result.write(i + 3 + 22, 1, str(-(10 - i) * 100))
        deci_result.write(i + 3 + 33, 1, str(-(10 - i) * 100))

        # Economic loss.
        deci_result.write(i + 3, 2 + 0, np.average(Cost_EB_med_1[i]))
        deci_result.write(i + 3, 2 + 4, np.average(Cost_EB_mon_1[i]))
        deci_result.write(i + 3, 2 + 8, np.average(Cost_EB_all_1[i]))
        deci_result.write(i + 3, 2 + 2, np.average(Cost_EB_med_2[i]))
        deci_result.write(i + 3, 2 + 6, np.average(Cost_EB_mon_2[i]))
        deci_result.write(i + 3, 2 + 10, np.average(Cost_EB_all_2[i]))
        deci_result.write(i + 3, 2 + 0 + 1, np.average(Cost_EB_med_1[i]) / np.average(Cost_EB_med_1[10]))
        deci_result.write(i + 3, 2 + 4 + 1, np.average(Cost_EB_mon_1[i]) / np.average(Cost_EB_mon_1[10]))
        deci_result.write(i + 3, 2 + 8 + 1, np.average(Cost_EB_all_1[i]) / np.average(Cost_EB_all_1[10]))
        deci_result.write(i + 3, 2 + 2 + 1, np.average(Cost_EB_med_2[i]) / np.average(Cost_EB_med_2[10]))
        deci_result.write(i + 3, 2 + 6 + 1, np.average(Cost_EB_mon_2[i]) / np.average(Cost_EB_mon_2[10]))
        deci_result.write(i + 3, 2 + 10 + 1, np.average(Cost_EB_all_2[i]) / np.average(Cost_EB_all_2[10]))

        deci_result.write(i + 3 + 11, 2 + 0, np.average(Cost_S1_med_1[i]))
        deci_result.write(i + 3 + 11, 2 + 4, np.average(Cost_S1_mon_1[i]))
        deci_result.write(i + 3 + 11, 2 + 8, np.average(Cost_S1_all_1[i]))
        deci_result.write(i + 3 + 11, 2 + 2, np.average(Cost_S1_med_2[i]))
        deci_result.write(i + 3 + 11, 2 + 6, np.average(Cost_S1_mon_2[i]))
        deci_result.write(i + 3 + 11, 2 + 10, np.average(Cost_S1_all_2[i]))
        deci_result.write(i + 3 + 11, 2 + 0 + 1, np.average(Cost_S1_med_1[i]) / np.average(Cost_S1_med_1[10]))
        deci_result.write(i + 3 + 11, 2 + 4 + 1, np.average(Cost_S1_mon_1[i]) / np.average(Cost_S1_mon_1[10]))
        deci_result.write(i + 3 + 11, 2 + 8 + 1, np.average(Cost_S1_all_1[i]) / np.average(Cost_S1_all_1[10]))
        deci_result.write(i + 3 + 11, 2 + 2 + 1, np.average(Cost_S1_med_2[i]) / np.average(Cost_S1_med_2[10]))
        deci_result.write(i + 3 + 11, 2 + 6 + 1, np.average(Cost_S1_mon_2[i]) / np.average(Cost_S1_mon_2[10]))
        deci_result.write(i + 3 + 11, 2 + 10 + 1, np.average(Cost_S1_all_2[i]) / np.average(Cost_S1_all_2[10]))

        deci_result.write(i + 3 + 22, 2 + 0, np.average(Cost_S2_med_1[i]))
        deci_result.write(i + 3 + 22, 2 + 4, np.average(Cost_S2_mon_1[i]))
        deci_result.write(i + 3 + 22, 2 + 8, np.average(Cost_S2_all_1[i]))
        deci_result.write(i + 3 + 22, 2 + 2, np.average(Cost_S2_med_2[i]))
        deci_result.write(i + 3 + 22, 2 + 6, np.average(Cost_S2_mon_2[i]))
        deci_result.write(i + 3 + 22, 2 + 10, np.average(Cost_S2_all_2[i]))
        deci_result.write(i + 3 + 22, 2 + 0 + 1, np.average(Cost_S2_med_1[i]) / np.average(Cost_S2_med_1[10]))
        deci_result.write(i + 3 + 22, 2 + 4 + 1, np.average(Cost_S2_mon_1[i]) / np.average(Cost_S2_mon_1[10]))
        deci_result.write(i + 3 + 22, 2 + 8 + 1, np.average(Cost_S2_all_1[i]) / np.average(Cost_S2_all_1[10]))
        deci_result.write(i + 3 + 22, 2 + 2 + 1, np.average(Cost_S2_med_2[i]) / np.average(Cost_S2_med_2[10]))
        deci_result.write(i + 3 + 22, 2 + 6 + 1, np.average(Cost_S2_mon_2[i]) / np.average(Cost_S2_mon_2[10]))
        deci_result.write(i + 3 + 22, 2 + 10 + 1, np.average(Cost_S2_all_2[i]) / np.average(Cost_S2_all_2[10]))

        deci_result.write(i + 3 + 33, 2 + 0, np.average(Cost_S3_med_1[i]))
        deci_result.write(i + 3 + 33, 2 + 4, np.average(Cost_S3_mon_1[i]))
        deci_result.write(i + 3 + 33, 2 + 8, np.average(Cost_S3_all_1[i]))
        deci_result.write(i + 3 + 33, 2 + 2, np.average(Cost_S3_med_2[i]))
        deci_result.write(i + 3 + 33, 2 + 6, np.average(Cost_S3_mon_2[i]))
        deci_result.write(i + 3 + 33, 2 + 10, np.average(Cost_S3_all_2[i]))
        deci_result.write(i + 3 + 33, 2 + 0 + 1, np.average(Cost_S3_med_1[i]) / np.average(Cost_S3_med_1[10]))
        deci_result.write(i + 3 + 33, 2 + 4 + 1, np.average(Cost_S3_mon_1[i]) / np.average(Cost_S3_mon_1[10]))
        deci_result.write(i + 3 + 33, 2 + 8 + 1, np.average(Cost_S3_all_1[i]) / np.average(Cost_S3_all_1[10]))
        deci_result.write(i + 3 + 33, 2 + 2 + 1, np.average(Cost_S3_med_2[i]) / np.average(Cost_S3_med_2[10]))
        deci_result.write(i + 3 + 33, 2 + 6 + 1, np.average(Cost_S3_mon_2[i]) / np.average(Cost_S3_mon_2[10]))
        deci_result.write(i + 3 + 33, 2 + 10 + 1, np.average(Cost_S3_all_2[i]) / np.average(Cost_S3_all_2[10]))

    # Save the table.
    Deci_result.save('economic_loss.xls')


if __name__ == "__main__":
    main()