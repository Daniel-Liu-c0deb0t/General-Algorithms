# Reinforcement Learning

## DDDQN
### Description
Implementation of a Dueling Double Deep Q Network using TensorFlow. It also depends on Numpy and Matplotlib.

It uses three convolution layers and two layers each for the advantage and the value calculation. Two networks are used for double Q learning. The learning algorthm uses an e-greedy approach to pick the best action for each state (exploitation), with a random chance of picking a random action (exploration). The epsilon value is annealed over time. Simple experience replay that allows previous experiences to be sampled is implemented.

The environment is a simple implementation of a grid with red (score of -1) and green (score of 1) blocks. The goal is to reach the green blocks by moving the blue character. Naturally, the four movement directions (available actions) are up, down, left, and right. I did not write the environment by myself, but I made a few edits.

### References
[Medium post on DDDQNs](https://medium.com/@awjuliani/simple-reinforcement-learning-with-tensorflow-part-4-deep-q-networks-and-beyond-8438a3e2b8df)

Actually, the whole series of posts helped me understand reinforcement learning. I recommend reading them.

[Implementation with TensorFlow + TFLearn](https://github.com/gokhanettin/dddqn-tf)

[Deep Reinforcement Learning with Double Q-Learning](https://arxiv.org/pdf/1509.06461v3.pdf)

[Dueling Network Architectures for Deep Reinforcement Learning](https://arxiv.org/pdf/1511.06581.pdf)