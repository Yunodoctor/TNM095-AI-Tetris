from keras.models import Sequential, load_model
from keras.layers import Embedding, Dense
from collections import deque
import numpy as np
import random


class DQNAgent:

    def __init__(self):
        # Initialize attributes
        self.start_size = 1000
        self.state_size = 2
        self.memory_size = 2000
        self.experience_replay = deque(maxlen=self.memory_size)
        self.discount = 0.95
        self.neurons = [32, 32]
        self.loss = 'mse'
        self.optimizer = 'adam'
        self.actions = [0, 1, 2, 3]
        self.action_size = 4

        # Initialize discount exploration rate
        self.epsilon = 0.2
        self.gamma = 0.6

        # Build networks
        self.q_network = self.build_model()
        self.target_network = self.build_model()
        self.alighn_target_model()

    def store(self, state, action, reward, next_state, terminated):
        self.experience_replay.append((state, action, reward, next_state, terminated))

    def build_model(self):
        model = Sequential()
        # Embedding(layer_size, number of dimensions, length of input seq) behover vi?
        model.add(Dense(self.neurons[0], activation='relu'))
        model.add(Dense(self.neurons[0], activation='relu'))
        model.add(Dense(self.neurons[0], activation='linear'))

        model.compile(loss=self.loss, optimizer=self.optimizer)

        return model

    def alighn_target_model(self):
        self.target_network.set_weights(self.q_network.get_weights())

    # Exploration function
    def act(self, state):
        """Returns the best state of a given collection of states after exploring"""
        #state = np.reshape(state, [1, self.state_size])
        if np.random.rand() <= self.epsilon:
            return random.sample(self.actions, 1)
        else:
            q_values = self.q_network.predict(state)
            return np.argmax(q_values[0][self.actions])

    def retrain(self, batch_size):
        """Training the agent"""
        minibatch = random.sample(self.experience_replay, batch_size)

        for state, action, reward, next_state, terminated in minibatch:
            target = self.q_network.predict(state)

            if terminated:
                target[0][action] = reward
            else:
                t = self.target_network.predict(next_state)
                target[0][action] = reward + self.gamma * np.amax(t)

            self.q_network.fit(state, target, epochs=1, verbose=0)

    def save_model(self):
        # save model and architecture to single file
        self.q_network.save("q_network.h5")
        print("Saved model to disk")

    def load_model(self):
        # load model
        model = load_model('q_network.h5')
        print("Loaded model from the disk")
