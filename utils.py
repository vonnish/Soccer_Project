'''
DQN Soccer Robot Simulation with Unity Environment.

Author : Shinhyeok Hwang
Course : CoE202
Algorithm : DQN(Deep Q-Network Learning)
https://arxiv.org/pdf/1312.5602.pdf
'''

from mlagents_envs.base_env import DecisionSteps

#preprocess sensor data
def sensor_front_sig(data):
    player=[]
    sensor_data=[]
    for sensor in range(33):
        player.append(data[8*sensor:(8*sensor)+8])
    
    for stack in range(3):
        sensor_data.append(player[11*stack:(11*stack)+11])

    return sensor_data

def sensor_back_sig(data):
    player=[]
    sensor_data=[]
    for sensor in range(9):
        player.append(data[8*sensor:(8*sensor)+8])
    
    for stack in range(3):
        sensor_data.append(player[3*stack:(3*stack)+3])

    return sensor_data

def step(decision_steps):

    #Get Signal From Agent 1
    signal_front_1 = sensor_front_sig(decision_steps.obs[0][0,:])
    signal_back_1 = sensor_back_sig(decision_steps.obs[1][0,:])

    #Get Signal From Agent 2
    signal_front_2 = sensor_front_sig(decision_steps.obs[0][1,:])
    signal_back_2 = sensor_back_sig(decision_steps.obs[1][1,:])

    reward = decision_steps.reward

    return signal_front_1, signal_back_1, signal_front_2, signal_back_2, reward

    #return state, reward