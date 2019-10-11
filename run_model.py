from builtins import range
import numpy as np
from dqn_agent import DQNAgent
from tetris_game import TetrisApp

# Run dqn with Tetris
def run_dqn():
    enviroment = TetrisApp()
    agent = DQNAgent(enviroment)

    batch_size = 32
    num_of_episodes = 100
    timesteps_per_episode = 1000
    agent.q_network.summery()

    for e in range(0, num_of_episodes):
        # Reset the enviroment
        state  = enviroment.reset()
        state = np.reshape(sate, [1,1])

        # Initialize variables
        reward = 0
        terminated = False

        bar = progressbar.ProgressBar(maxval=timesteps_per_episode/10, widgets=/10, widgets=[progressbar._Bar('=', '[', ']'), '', progressbar.Percentage()])
        bar.start()