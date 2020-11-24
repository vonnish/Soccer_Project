'''
DQN Soccer Robot Simulation with Unity Environment.

Author : Shinhyeok Hwang
Course : CoE202
Algorithm : DQN(Deep Q-Network Learning)
https://arxiv.org/pdf/1312.5602.pdf
'''

import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F


#Network Architectures
class DQN(nn.Module):

    def __init__(self, ,input_shape, action_dim):
        '''
        input shape: (C, H, W) = (3, 14, 8)
        action_dim: 3
        '''
        super(DQN, self).__init__()
        self.conv1 = nn.Conv2d(input_shape[0], 16, kernel_size=5, stride=2)
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5, stride=2)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32, 32, kernel_size=5, stride=2)
        self.bn3 = nn.BatchNorm2d(32)

        def conv2d_size_out(size, kernel_size = 2, stride = 1):
            return (size - (kernel_size - 1) - 1) // stride  + 1

        self.convw = conv2d_size_out(conv2d_size_out(conv2d_size_out(input_shape[1])))
        self.convh = conv2d_size_out(conv2d_size_out(conv2d_size_out(input_shape[2])))

        self.fc4 = nn.Linear(convw * convh * 32, 256)
        self.fc5 = nn.Linear(256, action_dim)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        return self.head(x.view(x.size(0), -1))