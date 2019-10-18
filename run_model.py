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
    num_of_episodes = 10
    time_steps_per_episode = 20000  # Amount of allowed actions for each game
    best_episode = [-100, 0, 0]  # Reward, Episode, Time


    for e in range(0, num_of_episodes):
        # Initialize variables
        terminated = False
        episodes_reward = 0

        environment.start_game(terminated)
        state = environment.get_state()
        state = np.reshape(state, [-1, 1])

        start_timer = time.time()

        for time_step in range(time_steps_per_episode):
            # Run Action
            environment.reset_reward()
            action = agent.act(state)

            # Take action
            next_state, reward, terminated, bumpiness, total_height = environment.play(action)
            next_state = np.reshape(next_state, [-1, 1])
            agent.store(state, action, reward, next_state, terminated, bumpiness, total_height)
            state = next_state
            episodes_reward += reward

            if terminated:
                agent.alighn_target_model()
                break

            if len(agent.experience_replay) > batch_size:
                agent.retrain(batch_size)

        end_timer = time.time()
        total_time = end_timer - start_timer

        # Get the highest reward
        if episodes_reward > best_episode[0]:
            best_episode[0] = episodes_reward
            best_episode[1] = e
            best_episode[2] = total_time

        print("**********************************")
        print("Episode/Game: ", e)
        print("Total time: ", total_time, "Seconds")
        print("Episodes total reward: ", episodes_reward)
        print("**********************************")

    print("______________________________________")
    print("The highest reward was: ", best_episode[0], "in game: ", best_episode[1])
    print("With the time", best_episode[2], "Seconds")
    print("______________________________________")
    agent.q_network.summary()
    agent.save_model()


# Function to play the game with a loaded model
def run_dqn():
    # Load the model you want to play with
    agent.load_model()


if __name__ == '__main__':
    run_dqn_train()
