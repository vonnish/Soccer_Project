'''
DQN Soccer Robot Simulation with Unity Environment.

Author : Shinhyeok Hwang
Course : CoE202
Algorithm : DQN(Deep Q-Network Learning)
https://arxiv.org/pdf/1312.5602.pdf
'''

import math
import random
import numpy as np
from copy import copy, deepcopy

import torch

from utils import step
from dqn_agent import Agent
from mlagents_envs.environment import UnityEnvironment


#Hyperparameters for tuning
num_episodes = 100
num_steps = 500

PRINT_EVERY = 10

#set GPU for faster training
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#Set Unity Environment
env = UnityEnvironment(file_name = 'CoE202')
env.reset()


#p : Purple Team, b: Blue Team
behavior_name_1 = list(env.behavior_specs)[0]
behavior_name_2 = list(env.behavior_specs)[1]

decision_steps_p, terminal_steps_p = env.get_steps(behavior_name_1)
decision_steps_b, terminal_steps_b = env.get_steps(behavior_name_2)

state_b1, state_b2, reward_b = step(decision_steps_b)
state_p1, state_p2, reward_p = step(decision_steps_p)

agent_b = Agent(state_dim=3, action_dim=3, device=device)
agent_p = Agent(state_dim=3, action_dim=3, device=device)

best_reward = -np.inf
saved_reward = -np.inf
saved_ep = 0
average_reward = 0
global_step = 0

for episode in range(num_episodes):

    agent_b.reset()
    agent_p.reset()

    ep_reward = 0
    
    #Receive Initial Observation state.
    decision_steps_p, terminal_steps_p = env.get_steps(behavior_name_1)
    decision_steps_b, terminal_steps_b = env.get_steps(behavior_name_2)
    
    state_b1, state_b2, reward_b = step(decision_steps_b)
    state_p1, state_p2, reward_p = step(decision_steps_p)

    for step in range(num_steps):
        global_step += 1

        #select action
        action_b = agent_b.select_action(state, step)   #(2,3): [(a1, a2, a3), (b1, b2, b3)]
        action_p = agent_p.select_action(state, step)   #(2,3)

        #Execute action a_t
        env.set_actions(behavior_name_1, action_p) #p
        env.set_actions(behavior_name_2, action_b) #b
        env.step()

        #Observe reward r_t and next state s_(t+1)
        decision_steps_p, terminal_steps_p = env.get_steps(behavior_name_1)
        decision_steps_b, terminal_steps_b = env.get_steps(behavior_name_2)
        
        next_state_b1, next_state_b2, reward_b = step(decision_steps_b)
        next_state_p1, next_state_p2, reward_p = step(decision_steps_p)

        #Store Transition to Memory
        agent_b.store_transtion(state_b1, action_b1, reward_b, next_state_b)
        agent_b.store_transtion(state_b2, action_b2, reward_b, next_state_b)
        agent_p.store_transtion(state_p1, action_p1, reward_p, next_state_p1)
        agent_p.store_transtion(state_p2, action_p2, reward_p, next_state_p2)

        #train agent
        agent_b.train()
        agent_p.train()

        ep_reward_b += reward_b
        ep_reward_p += reward_p

        if (terminal_steps_b or terminal_steps_p):
                agent_b.reset()
                agent_p.reset()
                break
    
    if ep_reward > best_reward:
    #Save the actor model for future testing
    torch.save(agents.policy_net.state_dict(), 'best_model.pkl')
    best_reward = ep_reward
    saved_reward = ep_reward
    saved_ep = episode + 1

    #Print every print_every episodes
    if (episode % PRINT_EVERY) == (PRINT_EVERY-1):
        print('[%6d episode, %8d total steps] average reward for past {} iterations: %.3f'.format(PRINT_EVERY) %
              (episode + 1, global_step, average_reward / PRINT_EVERY))
        print("Last model saved with reward: {:.2f}, at episode {}.".format(saved_reward, saved_ep))
        average_reward = 0 #reset average reward


env.close()