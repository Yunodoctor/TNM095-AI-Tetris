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
    time_steps_per_episode = 1000 # Amount of allowed actions for each game
    agent.q_network.summery()

    for e in range(0, num_of_episodes):
        """ ???? Reset the environment ???? """
        state = environment.get_state()
        state = np.reshape(state, [-1, 1])

        # Initialize variables
        reward = 0
        terminated = False

        bar = progressbar.ProgressBar(maxval=time_steps_per_episode / 10,
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

        for timestep in range(time_steps_per_episode):
            # Run Action
            action = agent.act(state)

            # Take action
            next_state, reward, terminated = environment.play(action)
            next_state = np.reshape(next_state, [-1, 1])
            agent.store(state, action, reward, next_state, terminated)

            state = next_state

            if terminated:
                agent.alighn_target_model()
                break

            if len(agent.experience_replay) > batch_size:
                agent.retrain(batch_size)

            if timestep % 10 == 0:
                bar.update(timestep / 10 + 1)

        bar.finish()
        if (e + 1) % 10 == 0:
            print("**********************************")
            print("Episode: {}".format(e + 1))
            print("**********************************")
