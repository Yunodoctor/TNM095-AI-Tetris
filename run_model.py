from builtins import range
import numpy as np
from dqn_agent import DQNAgent
from tetris_game import TetrisApp
import progressbar


# Run dqn with Tetris
def run_dqn():
    environment = TetrisApp()
    agent = DQNAgent(environment)

    batch_size = 32
    num_of_episodes = 100
    time_steps_per_episode = 1000
    agent.q_network.summery()

    for e in range(0, num_of_episodes):
        # Reset the environment
        state = environment.reset()
        state = np.reshape(state, [1, 1])

        # Initialize variables
        reward = 0
        terminated = False

        bar = progressbar.ProgressBar(maxval=time_steps_per_episode / 10,
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
