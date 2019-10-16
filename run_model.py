from builtins import range
import numpy as np
from dqn_agent import DQNAgent
from tetris_game import TetrisApp


# Run dqn with Tetris
def run_dqn():
    environment = TetrisApp()
    agent = DQNAgent()

    batch_size = 32
    num_of_episodes = 3
    time_steps_per_episode = 1000  # Amount of allowed actions for each game

    for e in range(0, num_of_episodes):
        # Initialize variables
        terminated = False

        environment.start_game(terminated)
        state = environment.get_state()
        state = np.reshape(state, [-1, 1])

        for time_step in range(time_steps_per_episode):

            # Run Action
            action = agent.act(state)

            # Take action
            next_state, reward, terminated = environment.play(action)
            next_state = np.reshape(next_state, [-1, 1])

            agent.store(state, action, reward, next_state, terminated)

            state = next_state

            if terminated:
                print("\n\nI DIED :( :(")
                agent.alighn_target_model()
                break

            if len(agent.experience_replay) > batch_size:
                agent.retrain(batch_size)

        if (e + 1) % 10 == 0:
            print("**********************************")
            print("Episode: {}".format(e + 1))
            print("**********************************")

    agent.q_network.summary()


if __name__ == '__main__':
    run_dqn()
