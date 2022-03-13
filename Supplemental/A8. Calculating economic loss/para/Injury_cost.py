# -*- coding: utf-8 -*-
'''
-------------------------------------------------------------------------------------------------
This code accompanies the paper titled "Human injury-based safety decision of automated vehicles"
Author: Qingfan Wang, Qing Zhou, Miao Lin, Bingbing Nie
Corresponding author: Bingbing Nie (nbb@tsinghua.edu.cn)
-------------------------------------------------------------------------------------------------
'''


import numpy as np
import xlrd


np.set_printoptions(suppress=True)


def main():
    ''' Calculate the evaluation criterion of equivalent economic loss. '''

    # Load equivalent economic loss from literatures.
    data_cost = xlrd.open_workbook('Cost.xlsx').sheet_by_name('data')
    data_cost = np.array([data_cost.col_values(2)[1:], data_cost.col_values(3)[1:], data_cost.col_values(4)[1:],
                          data_cost.col_values(5)[1:]])

    # Load AIS injury data from the real-world crash dataset.
    data_AIS = xlrd.open_workbook('AIS_injury.xlsx').sheet_by_name('Data_clear')
    data_AIS_num = data_AIS.col_values(4)[1:]
    data_AIS = data_AIS.col_values(5)[1:]

    AIS_num_list = []
    for i in range(len(data_AIS)):
        AIS_num = data_AIS_num[i]
        if AIS_num == '1':
            AIS_num_list.append(i)


    # Measure the injury numbers per traffic accident victim by AIS given a specific MAIS.
    inj_num = [[[]], [[], []], [[], [], []], [[], [], [], []], [[], [], [], [], []], [[], [], [], [], [], []]]
    for num in range(len(AIS_num_list)):
        temp = np.zeros(6)
        end = AIS_num_list[num + 1] if num + 1 < len(AIS_num_list) else len(data_AIS)
        for i in range(AIS_num_list[num], end):
            AIS = data_AIS[i]
            temp[int(min(int(AIS[6]), 6))-1] += 1
        if temp[5] > 0:
            inj_num[5][0].append(int(temp[0]))
            inj_num[5][1].append(int(temp[1]))
            inj_num[5][2].append(int(temp[2]))
            inj_num[5][3].append(int(temp[3]))
            inj_num[5][4].append(int(temp[4]))
            inj_num[5][5].append(int(temp[5]))
        elif temp[4] > 0:
            inj_num[4][0].append(int(temp[0]))
            inj_num[4][1].append(int(temp[1]))
            inj_num[4][2].append(int(temp[2]))
            inj_num[4][3].append(int(temp[3]))
            inj_num[4][4].append(int(temp[4]))
        elif temp[3] > 0:
            inj_num[3][0].append(int(temp[0]))
            inj_num[3][1].append(int(temp[1]))
            inj_num[3][2].append(int(temp[2]))
            inj_num[3][3].append(int(temp[3]))
        elif temp[2] > 0:
            inj_num[2][0].append(int(temp[0]))
            inj_num[2][1].append(int(temp[1]))
            inj_num[2][2].append(int(temp[2]))
        elif temp[1] > 0:
            inj_num[1][0].append(int(temp[0]))
            inj_num[1][1].append(int(temp[1]))
        elif temp[0] > 0:
            inj_num[0][0].append(int(temp[0]))

    num_11 = np.average(inj_num[0])
    num_21, num_22 = np.average(inj_num[1][0]), np.average(inj_num[1][1])
    num_31, num_32, num_33 = np.average(inj_num[2][0]), np.average(inj_num[2][1]), np.average(inj_num[2][2])
    num_41, num_42, num_43, num_44 = np.average(inj_num[3][0]), np.average(inj_num[3][1]), np.average(inj_num[3][2]), np.average(inj_num[3][3])
    num_51, num_52, num_53, num_54, num_55 = np.average(inj_num[4][0]), np.average(inj_num[4][1]), np.average(inj_num[4][2]), np.average(inj_num[4][3]), np.average(inj_num[4][4])
    num_61, num_62, num_63, num_64, num_65, num_66 = np.average(inj_num[5][0]), np.average(inj_num[5][1]), np.average(inj_num[5][2]), np.average(inj_num[5][3]), np.average(inj_num[5][4]), np.average(inj_num[5][5])
    # print(num_11)
    # print(num_21, num_22)
    # print(num_31, num_32, num_33)
    # print(num_41, num_42, num_43, num_44)
    # print(num_51, num_52, num_53, num_54, num_55)
    # print(num_61, num_62, num_63, num_64, num_65, num_66)


    # Calculate the distributions of injuries collected from NASS/CDS (2004-2015) by body region and injury severity.
    data_sta = np.zeros((6, 7))
    for i in range(len(data_AIS)):
        AIS = data_AIS[i]
        if AIS[0] == '6':
            data_sta[0, 0] += 1
            data_sta[0, min(int(AIS[6]), 6)] += 1
        elif AIS[:4] in ['1202', '1214', '1216', '1218', '1220', '1402', '1404', '1406', '1407', '1610']:
            data_sta[1, 0] += 1
            data_sta[1, min(int(AIS[6]), 6)] += 1
        elif AIS[0] == '8':
            data_sta[2, 0] += 1
            data_sta[2, min(int(AIS[6]), 6)] += 1
        elif AIS[0] == '7':
            data_sta[3, 0] += 1
            data_sta[3, min(int(AIS[6]), 6)] += 1
        elif AIS[0] in ['4', '5']:
            data_sta[4, 0] += 1
            data_sta[4, min(int(AIS[6]), 6)] += 1
        elif AIS[0] in ['1', '2', '3']:
            data_sta[5, 0] += 1
            data_sta[5, min(int(AIS[6]), 6)] += 1

    num_1 = np.sum(data_sta[:, 1])
    num_2 = np.sum(data_sta[:, 2:4])
    num_3 = np.sum(data_sta[:, 4:7])


    # Calculate the floor of evaluation criterion.
    cost_med_1 = data_sta[0, 1] * data_cost[0, 0] + data_sta[1, 1] * data_cost[0, 5] + data_sta[2, 1] * data_cost[0, 10] + \
             data_sta[3, 1] * data_cost[0, 15] + data_sta[4, 1] * data_cost[0, 20] + data_sta[5, 1] * data_cost[0, 25]
    cost_med_1 = cost_med_1 / num_1
    cost_med_2 = data_sta[0, 2] * data_cost[0, 1] + data_sta[1, 2] * data_cost[0, 6] + data_sta[2, 2] * data_cost[0, 11] + \
             data_sta[3, 2] * data_cost[0, 16] + data_sta[4, 2] * data_cost[0, 21] + data_sta[5, 2] * data_cost[0, 26] + \
             data_sta[0, 3] * data_cost[0, 2] + data_sta[1, 3] * data_cost[0, 7] + data_sta[2, 3] * data_cost[0, 12] + \
             data_sta[3, 3] * data_cost[0, 17] + data_sta[4, 3] * data_cost[0, 22] + data_sta[5, 3] * data_cost[0, 27]
    cost_med_2 = cost_med_2 / num_2
    cost_med_3 = data_sta[0, 4] * data_cost[0, 3] + data_sta[1, 4] * data_cost[0, 8] + data_sta[2, 4] * data_cost[0, 13] + \
             data_sta[3, 4] * data_cost[0, 18] + data_sta[4, 4] * data_cost[0, 23] + data_sta[5, 4] * data_cost[0, 28] + \
             data_sta[0, 5] * data_cost[0, 4] + data_sta[1, 5] * data_cost[0, 9] + data_sta[2, 5] * data_cost[0, 14] + \
             data_sta[3, 5] * data_cost[0, 19] + data_sta[4, 5] * data_cost[0, 24] + data_sta[5, 5] * data_cost[0, 29] + \
             data_sta[0, 6] * data_cost[0, 4] + data_sta[1, 6] * data_cost[0, 9] + data_sta[2, 6] * data_cost[0, 14] + \
             data_sta[3, 6] * data_cost[0, 19] + data_sta[4, 6] * data_cost[0, 24] + data_sta[5, 6] * data_cost[0, 29]
    cost_med_3 = cost_med_3 / num_3

    cost_mon_1 = data_sta[0, 1] * data_cost[1, 0] + data_sta[1, 1] * data_cost[1, 5] + data_sta[2, 1] * data_cost[1, 10] + \
             data_sta[3, 1] * data_cost[1, 15] + data_sta[4, 1] * data_cost[1, 20] + data_sta[5, 1] * data_cost[1, 25]
    cost_mon_1 = cost_mon_1 / num_1
    cost_mon_2 = data_sta[0, 2] * data_cost[1, 1] + data_sta[1, 2] * data_cost[1, 6] + data_sta[2, 2] * data_cost[1, 11] + \
             data_sta[3, 2] * data_cost[1, 16] + data_sta[4, 2] * data_cost[1, 21] + data_sta[5, 2] * data_cost[1, 26] + \
             data_sta[0, 3] * data_cost[1, 2] + data_sta[1, 3] * data_cost[1, 7] + data_sta[2, 3] * data_cost[1, 12] + \
             data_sta[3, 3] * data_cost[1, 17] + data_sta[4, 3] * data_cost[1, 22] + data_sta[5, 3] * data_cost[1, 27]
    cost_mon_2 = cost_mon_2 / num_2
    cost_mon_3 = data_sta[0, 4] * data_cost[1, 3] + data_sta[1, 4] * data_cost[1, 8] + data_sta[2, 4] * data_cost[1, 13] + \
             data_sta[3, 4] * data_cost[1, 18] + data_sta[4, 4] * data_cost[1, 23] + data_sta[5, 4] * data_cost[1, 28] + \
             data_sta[0, 5] * data_cost[1, 4] + data_sta[1, 5] * data_cost[1, 9] + data_sta[2, 5] * data_cost[1, 14] + \
             data_sta[3, 5] * data_cost[1, 19] + data_sta[4, 5] * data_cost[1, 24] + data_sta[5, 5] * data_cost[1, 29] + \
             data_sta[0, 6] * data_cost[1, 4] + data_sta[1, 6] * data_cost[1, 9] + data_sta[2, 6] * data_cost[1, 14] + \
             data_sta[3, 6] * data_cost[1, 19] + data_sta[4, 6] * data_cost[1, 24] + data_sta[5, 6] * data_cost[1, 29]
    cost_mon_3 = cost_mon_3 / num_3

    cost_all_1 = data_sta[0, 1] * data_cost[3, 0] + data_sta[1, 1] * data_cost[3, 5] + data_sta[2, 1] * data_cost[3, 10] + \
             data_sta[3, 1] * data_cost[3, 15] + data_sta[4, 1] * data_cost[3, 20] + data_sta[5, 1] * data_cost[3, 25]
    cost_all_1 = cost_all_1 / num_1
    cost_all_2 = data_sta[0, 2] * data_cost[3, 1] + data_sta[1, 2] * data_cost[3, 6] + data_sta[2, 2] * data_cost[3, 11] + \
             data_sta[3, 2] * data_cost[3, 16] + data_sta[4, 2] * data_cost[3, 21] + data_sta[5, 2] * data_cost[3, 26] + \
             data_sta[0, 3] * data_cost[3, 2] + data_sta[1, 3] * data_cost[3, 7] + data_sta[2, 3] * data_cost[3, 12] + \
             data_sta[3, 3] * data_cost[3, 17] + data_sta[4, 3] * data_cost[3, 22] + data_sta[5, 3] * data_cost[3, 27]
    cost_all_2 = cost_all_2 / num_2
    cost_all_3 = data_sta[0, 4] * data_cost[3, 3] + data_sta[1, 4] * data_cost[3, 8] + data_sta[2, 4] * data_cost[3, 13] + \
             data_sta[3, 4] * data_cost[3, 18] + data_sta[4, 4] * data_cost[3, 23] + data_sta[5, 4] * data_cost[3, 28] + \
             data_sta[0, 5] * data_cost[3, 4] + data_sta[1, 5] * data_cost[3, 9] + data_sta[2, 5] * data_cost[3, 14] + \
             data_sta[3, 5] * data_cost[3, 19] + data_sta[4, 5] * data_cost[3, 24] + data_sta[5, 5] * data_cost[3, 29] + \
             data_sta[0, 6] * data_cost[3, 4] + data_sta[1, 6] * data_cost[3, 9] + data_sta[2, 6] * data_cost[3, 14] + \
             data_sta[3, 6] * data_cost[3, 19] + data_sta[4, 6] * data_cost[3, 24] + data_sta[5, 6] * data_cost[3, 29]
    cost_all_3 = cost_all_3 / num_3

    inj_cost_floor = np.array([[cost_med_1, cost_med_2, cost_med_3],
                               [cost_mon_1, cost_mon_2, cost_mon_3],
                               [cost_all_1, cost_all_2, cost_all_3]])
    np.save('inj_cost_floor', inj_cost_floor)


    # Calculate the ceiling of evaluation criterion.
    cost_med_1_ = (data_sta[0, 1] * data_cost[0, 0] + data_sta[1, 1] * data_cost[0, 5] + data_sta[2, 1] * data_cost[0, 10] + \
             data_sta[3, 1] * data_cost[0, 15] + data_sta[4, 1] * data_cost[0, 20] + data_sta[5, 1] * data_cost[0, 25])
    cost_med_1_ = cost_med_1_ / np.sum(data_sta[:, 1])
    cost_med_2_ = data_sta[0, 2] * data_cost[0, 1] + data_sta[1, 2] * data_cost[0, 6] + data_sta[2, 2] * data_cost[0, 11] + \
             data_sta[3, 2] * data_cost[0, 16] + data_sta[4, 2] * data_cost[0, 21] + data_sta[5, 2] * data_cost[0, 26]
    cost_med_2_ = cost_med_2_ / np.sum(data_sta[:, 2])
    cost_med_3_ = data_sta[0, 3] * data_cost[0, 2] + data_sta[1, 3] * data_cost[0, 7] + data_sta[2, 3] * data_cost[0, 12] + \
             data_sta[3, 3] * data_cost[0, 17] + data_sta[4, 3] * data_cost[0, 22] + data_sta[5, 3] * data_cost[0, 27]
    cost_med_3_ = cost_med_3_ / np.sum(data_sta[:, 3])
    cost_med_4_ = data_sta[0, 5] * data_cost[0, 4] + data_sta[1, 5] * data_cost[0, 9] + data_sta[2, 5] * data_cost[0, 14] + \
             data_sta[3, 5] * data_cost[0, 19] + data_sta[4, 5] * data_cost[0, 24] + data_sta[5, 5] * data_cost[0, 29]
    cost_med_4_ = cost_med_4_ / np.sum(data_sta[:, 4])
    cost_med_5_ = data_sta[0, 6] * data_cost[0, 4] + data_sta[1, 6] * data_cost[0, 9] + data_sta[2, 6] * data_cost[0, 14] + \
             data_sta[3, 6] * data_cost[0, 19] + data_sta[4, 6] * data_cost[0, 24] + data_sta[5, 6] * data_cost[0, 29]
    cost_med_5_ = cost_med_5_ / np.sum(data_sta[:, 5])
    cost_med_6_ = data_sta[0, 4] * data_cost[0, 3] + data_sta[1, 4] * data_cost[0, 8] + data_sta[2, 4] * data_cost[0, 13] + \
             data_sta[3, 4] * data_cost[0, 18] + data_sta[4, 4] * data_cost[0, 23] + data_sta[5, 4] * data_cost[0, 28]
    cost_med_6_ = cost_med_6_ / np.sum(data_sta[:, 6])

    cost_mon_1_ = (data_sta[0, 1] * data_cost[1, 0] + data_sta[1, 1] * data_cost[1, 5] + data_sta[2, 1] * data_cost[1, 10] + \
             data_sta[3, 1] * data_cost[1, 15] + data_sta[4, 1] * data_cost[1, 20] + data_sta[5, 1] * data_cost[1, 25])
    cost_mon_1_ = cost_mon_1_ / np.sum(data_sta[:, 1])
    cost_mon_2_ = data_sta[0, 2] * data_cost[1, 1] + data_sta[1, 2] * data_cost[1, 6] + data_sta[2, 2] * data_cost[1, 11] + \
             data_sta[3, 2] * data_cost[1, 16] + data_sta[4, 2] * data_cost[1, 21] + data_sta[5, 2] * data_cost[1, 26]
    cost_mon_2_ = cost_mon_2_ / np.sum(data_sta[:, 2])
    cost_mon_3_ = data_sta[0, 3] * data_cost[1, 2] + data_sta[1, 3] * data_cost[1, 7] + data_sta[2, 3] * data_cost[1, 12] + \
             data_sta[3, 3] * data_cost[1, 17] + data_sta[4, 3] * data_cost[1, 22] + data_sta[5, 3] * data_cost[1, 27]
    cost_mon_3_ = cost_mon_3_ / np.sum(data_sta[:, 3])
    cost_mon_4_ = data_sta[0, 5] * data_cost[1, 4] + data_sta[1, 5] * data_cost[1, 9] + data_sta[2, 5] * data_cost[1, 14] + \
             data_sta[3, 5] * data_cost[1, 19] + data_sta[4, 5] * data_cost[1, 24] + data_sta[5, 5] * data_cost[1, 29]
    cost_mon_4_ = cost_mon_4_ / np.sum(data_sta[:, 4])
    cost_mon_5_ = data_sta[0, 6] * data_cost[1, 4] + data_sta[1, 6] * data_cost[1, 9] + data_sta[2, 6] * data_cost[1, 14] + \
             data_sta[3, 6] * data_cost[1, 19] + data_sta[4, 6] * data_cost[1, 24] + data_sta[5, 6] * data_cost[1, 29]
    cost_mon_5_ = cost_mon_5_ / np.sum(data_sta[:, 5])
    cost_mon_6_ = data_sta[0, 4] * data_cost[1, 3] + data_sta[1, 4] * data_cost[1, 8] + data_sta[2, 4] * data_cost[1, 13] + \
             data_sta[3, 4] * data_cost[1, 18] + data_sta[4, 4] * data_cost[1, 23] + data_sta[5, 4] * data_cost[1, 28]
    cost_mon_6_ = cost_mon_6_ / np.sum(data_sta[:, 6])

    cost_all_1_ = (data_sta[0, 1] * data_cost[3, 0] + data_sta[1, 1] * data_cost[3, 5] + data_sta[2, 1] * data_cost[3, 10] + \
             data_sta[3, 1] * data_cost[3, 15] + data_sta[4, 1] * data_cost[3, 20] + data_sta[5, 1] * data_cost[3, 25])
    cost_all_1_ = cost_all_1_ / np.sum(data_sta[:, 1])
    cost_all_2_ = data_sta[0, 2] * data_cost[3, 1] + data_sta[1, 2] * data_cost[3, 6] + data_sta[2, 2] * data_cost[3, 11] + \
             data_sta[3, 2] * data_cost[3, 16] + data_sta[4, 2] * data_cost[3, 21] + data_sta[5, 2] * data_cost[3, 26]
    cost_all_2_ = cost_all_2_ / np.sum(data_sta[:, 2])
    cost_all_3_ = data_sta[0, 3] * data_cost[3, 2] + data_sta[1, 3] * data_cost[3, 7] + data_sta[2, 3] * data_cost[3, 12] + \
             data_sta[3, 3] * data_cost[3, 17] + data_sta[4, 3] * data_cost[3, 22] + data_sta[5, 3] * data_cost[3, 27]
    cost_all_3_ = cost_all_3_ / np.sum(data_sta[:, 3])
    cost_all_4_ = data_sta[0, 5] * data_cost[3, 4] + data_sta[1, 5] * data_cost[3, 9] + data_sta[2, 5] * data_cost[3, 14] + \
             data_sta[3, 5] * data_cost[3, 19] + data_sta[4, 5] * data_cost[3, 24] + data_sta[5, 5] * data_cost[3, 29]
    cost_all_4_ = cost_all_4_ / np.sum(data_sta[:, 4])
    cost_all_5_ = data_sta[0, 6] * data_cost[3, 4] + data_sta[1, 6] * data_cost[3, 9] + data_sta[2, 6] * data_cost[3, 14] + \
             data_sta[3, 6] * data_cost[3, 19] + data_sta[4, 6] * data_cost[3, 24] + data_sta[5, 6] * data_cost[3, 29]
    cost_all_5_ = cost_all_5_ / np.sum(data_sta[:, 5])
    cost_all_6_ = data_sta[0, 4] * data_cost[3, 3] + data_sta[1, 4] * data_cost[3, 8] + data_sta[2, 4] * data_cost[3, 13] + \
             data_sta[3, 4] * data_cost[3, 18] + data_sta[4, 4] * data_cost[3, 23] + data_sta[5, 4] * data_cost[3, 28]
    cost_all_6_ = cost_all_6_ / np.sum(data_sta[:, 6])


    cost_med_1 = cost_med_1_ * num_11
    cost_med_2 = np.sum(data_sta[:, 2]) / np.sum(data_sta[:, 2:4]) * (cost_med_2_ * num_22 + cost_med_1_ * num_21) +\
                 np.sum(data_sta[:, 3]) / np.sum(data_sta[:, 2:4]) * (cost_med_3_ * num_33 + cost_med_2_ * num_32 + cost_med_1_ * num_31)
    cost_med_3 = np.sum(data_sta[:, 4]) / np.sum(data_sta[:, 4:7]) * (cost_med_4_ * num_44 + cost_med_3_ * num_43 + cost_med_2_ * num_42 + cost_med_1_ * num_41) +\
                 np.sum(data_sta[:, 5]) / np.sum(data_sta[:, 4:7]) * (cost_med_5_ * num_55 + cost_med_4_ * num_54 + cost_med_3_ * num_53 + cost_med_2_ * num_52 + cost_med_1_ * num_51) +\
                 np.sum(data_sta[:, 6]) / np.sum(data_sta[:, 4:7]) * (cost_med_6_ * num_66 + cost_med_5_ * num_65 + cost_med_4_ * num_64 + cost_med_3_ * num_63 + cost_med_2_ * num_62 + cost_med_1_ * num_61)

    cost_mon_1 = cost_mon_1_ * num_11
    cost_mon_2 = np.sum(data_sta[:, 2]) / np.sum(data_sta[:, 2:4]) * (cost_mon_2_ * num_22 + cost_mon_1_ * num_21) +\
                 np.sum(data_sta[:, 3]) / np.sum(data_sta[:, 2:4]) * (cost_mon_3_ * num_33 + cost_mon_2_ * num_32 + cost_mon_1_ * num_31)
    cost_mon_3 = np.sum(data_sta[:, 4]) / np.sum(data_sta[:, 4:7]) * (cost_mon_4_ * num_44 + cost_mon_3_ * num_43 + cost_mon_2_ * num_42 + cost_mon_1_ * num_41) +\
                 np.sum(data_sta[:, 5]) / np.sum(data_sta[:, 4:7]) * (cost_mon_5_ * num_55 + cost_mon_4_ * num_54 + cost_mon_3_ * num_53 + cost_mon_2_ * num_52 + cost_mon_1_ * num_51) +\
                 np.sum(data_sta[:, 6]) / np.sum(data_sta[:, 4:7]) * (cost_mon_6_ * num_66 + cost_mon_5_ * num_65 + cost_mon_4_ * num_64 + cost_mon_3_ * num_63 + cost_mon_2_ * num_62 + cost_mon_1_ * num_61)

    cost_all_1 = cost_all_1_ * num_11
    cost_all_2 = np.sum(data_sta[:, 2]) / np.sum(data_sta[:, 2:4]) * (cost_all_2_ * num_22 + cost_all_1_ * num_21) +\
                 np.sum(data_sta[:, 3]) / np.sum(data_sta[:, 2:4]) * (cost_all_3_ * num_33 + cost_all_2_ * num_32 + cost_all_1_ * num_31)
    cost_all_3 = np.sum(data_sta[:, 4]) / np.sum(data_sta[:, 4:7]) * (cost_all_4_ * num_44 + cost_all_3_ * num_43 + cost_all_2_ * num_42 + cost_all_1_ * num_41) +\
                 np.sum(data_sta[:, 5]) / np.sum(data_sta[:, 4:7]) * (cost_all_5_ * num_55 + cost_all_4_ * num_54 + cost_all_3_ * num_53 + cost_all_2_ * num_52 + cost_all_1_ * num_51) +\
                 np.sum(data_sta[:, 6]) / np.sum(data_sta[:, 4:7]) * (cost_all_6_ * num_66 + cost_all_5_ * num_65 + cost_all_4_ * num_64 + cost_all_3_ * num_63 + cost_all_2_ * num_62 + cost_all_1_ * num_61)

    inj_cost_ceiling = np.array([[cost_med_1, cost_med_2, cost_med_3],
                                 [cost_mon_1, cost_mon_2, cost_mon_3],
                                 [cost_all_1, cost_all_2, cost_all_3]])
    np.save('inj_cost_ceiling', inj_cost_ceiling)


if __name__ == "__main__":
    main()
