# -*- coding: utf-8 -*-
'''
-------------------------------------------------------------------------------------------------
This code accompanies the paper titled "Human injury-based safety decision of automated vehicles"
Author: Qingfan Wang, ***,
Corresponding author: Bingbing Nie (nbb@tsinghua.edu.cn)
-------------------------------------------------------------------------------------------------
'''


import sys
import os
import time
import argparse
import random
import numpy as np

import torch
from torch import nn
from torch.nn.utils import weight_norm
import torch.utils.data as Data

import imblearn
from imblearn.combine import SMOTEENN
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import EditedNearestNeighbours

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


__author__ = "Qingfan Wang"


class FNN(nn.Module):
    ''' Develop FNN-based occupant injury prediction model. '''

    def __init__(self, in_dim, n_hidden, dropout, flag):
        super(FNN, self).__init__()
        ''' Develop the model structure. '''

        # Develop embedding layers for eight input valuables.
        # The size of embedding tables depends on the discretization of valuables.
        self.embed_1 = nn.Linear(1, in_dim)  # collision delta-v
        self.embed_2 = nn.Linear(1, in_dim)  # collision angle
        self.embed_3 = nn.Embedding(22, in_dim)  # POI of the ego vehicle
        self.embed_4 = nn.Embedding(22, in_dim)  # POI of the opposing vehicle
        self.embed_5 = nn.Embedding(4, in_dim)  # occupant age
        self.embed_6 = nn.Embedding(2, in_dim)  # occupant gender
        self.embed_7 = nn.Embedding(2, in_dim)  # belt usage
        self.embed_8 = nn.Embedding(2, in_dim)  # airbag usage
        self.embed_9 = nn.Embedding(5, in_dim)  # vehicle mass ratio

        self.flag = flag

        # The key data processing module.
        self.layer1 = nn.Sequential(nn.Linear(in_dim, n_hidden), nn.BatchNorm1d(n_hidden), nn.ReLU(), nn.Dropout(dropout))
        self.layer2 = nn.Sequential(nn.Linear(n_hidden, n_hidden), nn.BatchNorm1d(n_hidden), nn.ReLU(), nn.Dropout(dropout))
        self.layer3 = nn.Sequential(nn.Linear(n_hidden, n_hidden), nn.BatchNorm1d(n_hidden), nn.ReLU(), nn.Dropout(dropout))
        if flag:
            self.layer4 = nn.Sequential(nn.Linear(n_hidden, n_hidden), nn.BatchNorm1d(n_hidden), nn.ReLU(), nn.Dropout(dropout))
            self.layer5 = nn.Sequential(nn.Linear(n_hidden, n_hidden), nn.BatchNorm1d(n_hidden), nn.ReLU(), nn.Dropout(dropout))
            self.layer6 = nn.Sequential(nn.Linear(n_hidden, n_hidden), nn.BatchNorm1d(n_hidden), nn.ReLU(), nn.Dropout(dropout))

        # Map the outputs to the four defined injury levels.
        self.layer = nn.Sequential(nn.Linear(n_hidden, 4))

    def forward(self, x):
        ''' The forward propagation of information. '''

        # Embedding the nine input valuables into a high-dimensional space based on embedding lookup tables.
        e_1 = self.embed_1(x[:, 0].unsqueeze(1))
        e_2 = self.embed_2(x[:, 1].unsqueeze(1))
        e_3 = self.embed_3(x[:, 2].long())
        e_4 = self.embed_4(x[:, 3].long())
        e_5 = self.embed_5(x[:, 4].long())
        e_6 = self.embed_6(x[:, 5].long())
        e_7 = self.embed_7(x[:, 6].long())
        e_8 = self.embed_8(x[:, 7].long())
        e_9 = self.embed_9(x[:, 8].long())

        # Concatenate the nine Embedded input valuables in the high-dimensional space.
        z = e_1 + e_2 + e_3 + e_4 + e_5 + e_6 + e_7 + e_8 + e_9

        # Process the input data with FNN.
        z = self.layer3(self.layer2(self.layer1(z)))
        if self.flag:
            z = self.layer6(self.layer5(self.layer4(z)))

        # Map the outputs to the four defined injury levels.
        outputs = self.layer(z)

        return outputs


class Logger(object):
    ''' Save a log file. '''

    def __init__(self, file_name="Default.log", stream=sys.stdout):
        self.terminal = stream
        self.log = open(file_name, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


def load_data(data, resample, seed):
    ''' Load and process the crash data. '''

    # Divide the dataset into three parts: training, validation, and testing.
    shuffle = np.random.permutation(len(data))
    data = data[shuffle]
    data_train = data[:int(len(data) * 0.7)]
    data_test = data[int(len(data) * 0.7):int(len(data) * 0.85)]
    data_val = data[int(len(data) * 0.85):]

    # Data re-sampling to reduce imbalance problems.
    if resample == 'US':
        enn = EditedNearestNeighbours(sampling_strategy=[0], n_neighbors=5, kind_sel="all")
        X_enn, y_enn = enn.fit_resample(data_train[:, :-1], data_train[:, -1])
        data_train = np.zeros((len(X_enn), 10))
        data_train[:, :-1], data_train[:, -1] = X_enn, y_enn
        enn = EditedNearestNeighbours(sampling_strategy=[1], n_neighbors=3, kind_sel="all")
        X_enn, y_enn = enn.fit_resample(data_train[:, :-1], data_train[:, -1])
        data_train = np.zeros((len(X_enn), 10))
        data_train[:, :-1], data_train[:, -1] = X_enn, y_enn

    elif resample == 'OS':
        smo = SMOTE(random_state=seed, sampling_strategy={1: 1900, 2: 1400, 3: 1000})
        X_smo, y_smo = smo.fit_resample(data_train[:, :-1], data_train[:, -1])
        data_train = np.zeros((len(X_smo), 10))
        data_train[:, :-1], data_train[:, -1] = X_smo, y_smo

    elif resample == 'CS':
        smo = SMOTE(random_state=seed, sampling_strategy={1: 2000, 2: 1200, 3: 800})
        enn = EditedNearestNeighbours(sampling_strategy=[0, 1, 2, 3], n_neighbors=3)
        smo_enn = SMOTEENN(random_state=seed, smote=smo, enn=enn)
        X_enn, y_enn = smo_enn.fit_resample(data_train[:, :-1], data_train[:, -1])
        data_train = np.zeros((len(X_enn), 10))
        data_train[:, :-1], data_train[:, -1] = X_enn, y_enn

    else:
        print('Wrong re-sampling method!')
        return

    # tranform the data into torch.
    data_train = torch.from_numpy(data_train).float().data.cuda()
    data_val = torch.from_numpy(data_val).float().data.cuda()
    data_test = torch.from_numpy(data_test).float().data.cuda()

    return data_train, data_val, data_test


def train_model(model, loader, optimizer, criterion, Loss, Num_data):
    ''' Train the model. '''

    # Switch to the training mode.
    model.train()

    # Training batch.
    loss_batch = []
    for step, (batch_x,) in enumerate(loader):
        prediction = model(batch_x[:, :-1])
        loss = criterion(prediction, batch_x[:, -1].long())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        loss_batch.append(loss.detach().data.cpu().numpy() * (float(len(prediction))))

    # Record the training loss.
    loss = np.around(np.sum(loss_batch) / Num_data, decimals=3)
    Loss.append(loss)


def evaluate_model(model, loader_eva, criterion, Loss, Num_data):
    ''' Evaluate the model. '''

    # Switch to the evaluation mode.
    model.eval()

    # Evaluation batch.
    loss_batch = []
    test_true = np.zeros(Num_data)
    test_pred = np.zeros(Num_data)
    for step, (batch_x,) in enumerate(loader_eva):
        prediction = model(batch_x[:, :-1])
        loss = criterion(prediction, batch_x[:, -1].long())
        loss_batch.append(
            np.around(loss.detach().data.cpu().numpy() * (float(len(prediction))), decimals=3))

        # Record the target and predicted injuries.
        if step < len(loader_eva) - 1:
            test_true[(step) * 256:(step + 1) * 256] = batch_x[:, -1].cpu().numpy()
            test_pred[(step) * 256:(step + 1) * 256] = prediction.data.max(1)[1].cpu().numpy()
        else:
            test_true[(step) * 256:] = batch_x[:, -1].cpu().numpy()
            test_pred[(step) * 256:] = prediction.data.max(1)[1].cpu().numpy()

    # Record the Evaluation loss.
    loss = np.around(np.sum(loss_batch) / Num_data, decimals=3)
    Loss.append(loss)

    # Calculate the prediction accuracy.
    accu = 100. * (1 - np.count_nonzero(test_true - test_pred) / float(len(test_pred)))
    G_mean = imblearn.metrics.geometric_mean_score(test_true, test_pred)
    conf_mat = confusion_matrix(test_true, test_pred)

    return np.around(accu, 1), np.around(G_mean, 3), conf_mat


def main():
    ''' Train and test the FNN-based occupant injury prediction model. '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--rand_seed', type=int, default=123, help='Random seed')
    parser.add_argument('--re_samp', type=str, default='OS', help='Re-sampling methods: US, OS, CS')
    parser.add_argument('--epoch', type=int, default=30, help='Training epochs')
    parser.add_argument('--print_inf', action='store_false', help='print the information of the training process')
    parser.add_argument('--save_para', action='store_false', help='save the model parameters')
    parser.add_argument('--save_loss', action='store_true', help='save the loss curves of the training process')
    opt = parser.parse_args()

    # Define the random seed.
    seed = opt.rand_seed
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True

    # Save a log file.
    log_path = './Logs/'
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file_name = log_path + 'log-' + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + '.log'
    sys.stdout = Logger(log_file_name)
    sys.stderr = Logger(log_file_name)

    # Load the real-world crash data.
    data = np.load('dataset/data_pro.npy')
    data_train, data_val, data_test = load_data(data, opt.re_samp, seed)

    # Define the parameter matrix for grid search.
    Flag_layer = [True, False]
    Batch_Size = [256, 128, 64, 32] * 2
    In_Hid_dim = [(16, 16), (16, 32), (32, 64), (64, 128), (128, 128)] * 8
    Dropout = [0.2, 0.5] * 40
    Learning_Rate = [0.0001, 0.0003, 0.001, 0.003, 0.01] * 80

    # Start the grid search for the optimal parameter combination.
    for num_mesh in range(400):
        # Obtain parameters.
        flag = Flag_layer[num_mesh // 200]
        Batch_size = Batch_Size[num_mesh // 50]
        (In_dim, Hid_dim) = In_Hid_dim[num_mesh // 10]
        dropout = Dropout[num_mesh // 5]
        Learning_rate = Learning_Rate[num_mesh]

        if opt.print_inf:
            print('\nGrid search epoch: ', num_mesh + 1, '/400')
            print('Parameters: ', flag, Batch_size, In_dim, Hid_dim, dropout, Learning_rate)

        # Load the datasets.
        dataset = Data.TensorDataset(data_train)
        loader = Data.DataLoader(dataset=dataset, batch_size=Batch_size, shuffle=True)
        dataset_val = Data.TensorDataset(data_val)
        loader_val = Data.DataLoader(dataset=dataset_val, batch_size=256, shuffle=True)
        dataset_test = Data.TensorDataset(data_test)
        loader_test = Data.DataLoader(dataset=dataset_test, batch_size=256, shuffle=True)

        # Load the model, optimizer, and criterion.
        model = FNN(in_dim=In_dim, n_hidden=Hid_dim, dropout=dropout, flag=flag).cuda()
        optimizer = torch.optim.Adam(model.parameters(), lr=Learning_rate)
        criterion = nn.CrossEntropyLoss().cuda()

        LossCurve, LossCurve_val, LossCurve_test = [], [], []

        # Start the training of the model.
        for epoch in range(opt.epoch):
            # Train the model.
            train_model(model, loader, optimizer, criterion, LossCurve, len(data_train))

            # Learning rate attenuation.
            for p in optimizer.param_groups:
                p['lr'] = Learning_rate / np.sqrt(epoch + 1)

            # Validate and test the model.
            if (epoch + 1) % 1 == 0:
                if opt.print_inf:
                    print('Epoch: ', epoch + 1, '/', opt.epoch)

                if opt.save_para:
                    torch.save(model.state_dict(),
                               'Saved_Model_params/FNN_%s %s %s.pkl' % (opt.re_samp, num_mesh + 1, epoch + 1))

                # Validate the model.
                accu, G_mean, conf_mat = evaluate_model(model, loader_val, criterion, LossCurve_val, len(data_val))
                if opt.print_inf:
                    print('Validation | Accuracy: ' + str(accu) + '%')
                    print('Validation | G-mean: ', G_mean)
                    print(conf_mat)

                # Test the model.
                accu, G_mean, conf_mat = evaluate_model(model, loader_test, criterion, LossCurve_test, len(data_test))
                if opt.print_inf:
                    print('Test | Accuracy: ' + str(accu) + '%')
                    print('Test | G-mean: ', G_mean)
                    print(conf_mat)

            # Early Stopping.
            if len(LossCurve_val) > 5 and LossCurve_val[-1] > LossCurve_val[-2] > LossCurve_val[-3] > LossCurve_val[
                -4] > LossCurve_val[-5]:
                if opt.print_inf:
                    print('Early Stop!')
                break

        # Save the loss curves of the training process.
        if opt.save_loss:
            plt.plot(LossCurve[1:], label='Loss Train')
            plt.plot(LossCurve_val[1:], label='Loss Val')
            plt.plot(LossCurve_test[1:], label='Loss Test')
            plt.legend()
            plt.savefig('Prediction_IMAGE/Loss FNN_%s %s.png' % (opt.re_samp, num_mesh + 1))
            plt.close()


if __name__ == "__main__":
    main()
