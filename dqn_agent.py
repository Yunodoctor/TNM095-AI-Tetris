from tensorflow.keras import Sequential
from tensorflow.keras import Embedding, Dense
from collections import deque
import numpy as np
import random

class DQNAgent:

    def __init__(self, enviroment):
        # Initialize atributes
        self.start_size = 1000
        self.state_size = 4 # Vi tror att det ar de olika rotationerna som shapesen kan utfora
        self._action_size = enviroment.action_space.n
        self.memory_size = 2000
        self.experience_replay = deque(maxlen=self.memory_size)
        self.discount = 0.95
        self.neurons = [32, 32]
        self.loss = 'mse'
        self.optimizer = 'adam'

        # Initialize discount exploration rate
        self.epsilon = 1
        self.epsilon_min = 0
        self.epsilon_max = 500
        self.gamma = 0.6

        # Build networks
        self.q_network = self.build_model()
        self.target_network = self.build_model()

    def build_model(self):
        model = Sequential()
       #Embedding(layer_size, number of dimensions, length of input seq) behover vi?
        model.add(Dense(self.neurons[0], input_dim=self.state_size, activation='relu'))
        model.add(Dense(self.neurons[0], input_dim=self.state_size, activation='relu'))
        model.add(Dense(self.neurons[0], activation='linear'))

        model.compile(loss=self.loss, optimizer=self.optimizer)

        return model

    # Exploration function
    def act(self, state):
        """Returns the best state of a given collection of states after exploring"""
        state = np.reshape(state, [1, self.state_size])
        if random.random() <= self.epsilon:
            return random.random()
        else:
            q_values = self.q_network.predic(state)
            return np.argmax(q_values[0])

    def retrain(self, batch_size):
        """Training the agent"""
        minibatch = random.sample(self.experience_replay, batch_size)

        for state, action,reward, next_state, terminated in minibatch:
            target = self.q_network.predic(state)

            if terminated:
                target[0][action] = reward
            else:
                t = self.target_network.predict(next_state)
                target[0][action] = reward + self.gamma * np.amax(t)

            self.q_network.fit(state, target, epochs=1, verbose=0)









