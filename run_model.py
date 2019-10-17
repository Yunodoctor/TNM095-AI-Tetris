from builtins import range
import numpy as np
from dqn_agent import DQNAgent
from tetris_game import TetrisApp
import time

# Configuration
environment = TetrisApp()
agent = DQNAgent()


# Function to train a model and save it
def run_dqn_train():

    batch_size = 32
    num_of_episodes = 200
    time_steps_per_episode = 10000  # Amount of allowed actions for each game
    highest_reward = 0

    for e in range(0, num_of_episodes):
        # Initialize variables
        terminated = False

        environment.start_game(terminated)
        state = environment.get_state()
        state = np.reshape(state, [-1, 1])

        start_timer = time.time()

        for time_step in range(time_steps_per_episode):
            # Run Action
            action = agent.act(state)

            # Take action
            next_state, reward, terminated, bumpiness = environment.play(action)
            next_state = np.reshape(next_state, [-1, 1])

            agent.store(state, action, reward, next_state, terminated, bumpiness)

            # Get the highest reward
            if reward > highest_reward:
                highest_reward = reward

            state = next_state

            if terminated:
                print("\n\nI DIED :( :(")
                agent.alighn_target_model()
                break

            if len(agent.experience_replay) > batch_size:
                agent.retrain(batch_size)

        end_timer = time.time()

        print("**********************************")
        print("-Time for one game: -")
        print(end_timer - start_timer)
        print("**********************************")

        if (e + 1) % 10 == 0:
            print("**********************************")
            print("Episode: {}".format(e + 1))
            print("**********************************")

    print("The highest reward was: ", highest_reward)
    agent.q_network.summary()
    agent.save_model()


# Function to play the game with a loaded model
def run_dqn():
    # Load the model you want to play with
    agent.load_model()


if __name__ == '__main__':
    run_dqn_train()
