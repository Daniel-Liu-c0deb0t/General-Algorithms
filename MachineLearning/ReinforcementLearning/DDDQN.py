from collections import deque
import time
import datetime
import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from gridworld import gameEnv
import random

# testing or training?
is_testing = True

# hyperparameters
learn_rate = 0.0001
num_noops = 5
num_rand_steps = 1000 # must be greater than batch size
total_episodes = 10000
episode_steps = 50

target_update_freq = 1000
online_update_freq = 4
print_freq = 10

img_width = 84
img_height = 84
img_channel = 3

tau = 0.001
gamma = 0.99

batch_size = 32
exp_buffer_size = 10000

# controls annealing rate for epsilon greedy
e_greedy_start = 1.0
e_greedy_end = 0.1
e_greedy_steps = 10000
e_greedy_test = 0.1

save_freq = 1000
save_path = "./dddqn_model_saves"
load_path = "./dddqn_model_saves/dddqn_model_final.ckpt"

e_greedy_diff = (e_greedy_start - e_greedy_end) / e_greedy_steps
os.makedirs(save_path, exist_ok = True)

# very simple experience buffer to get random samples
class ExperienceBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = deque(maxlen = size)

    def append(self, exp):
        self.buffer.append(exp)

    def sample(self, num):
        res = np.array(random.sample(self.buffer, num))
        return np.stack(res[:, 0]), res[:, 1], res[:, 2], np.stack(res[:, 3]), res[:, 4]

def to_flat_state(state):
    np_state = np.array(state)
    shape = np_state.shape
    return np.reshape(state, [shape[0], shape[1] * shape[2] * shape[3]]) / 255.0

def clip_loss(loss):
    return tf.where(tf.abs(loss) < 1.0, 0.5 * tf.square(loss), tf.abs(loss) - 0.5)

def create_env():
    return gameEnv(False, 7, False)

def reset_env(env):
    noops = random.randrange(num_noops)
    state = env.reset()
    for i in range(noops):
        state, _, _ = env.step(env.actions)
    return state

def create_model(num_actions):
    flattened_state = tf.placeholder(tf.float32, [None, img_width * img_height * img_channel])
    reshaped_state = tf.reshape(flattened_state, [-1, img_channel, img_height, img_width])
    inputs = tf.transpose(reshaped_state, [0, 2, 3, 1])

    init = tf.contrib.layers.xavier_initializer()

    # model: 3 conv + split into advantage and value fully connected layers
    # dueling q network approach

    # output size, kernel size, stride size
    conv = tf.layers.conv2d(inputs, 32, 8, 4, "VALID", activation = tf.nn.relu, kernel_initializer = init)
    conv = tf.layers.conv2d(conv, 64, 4, 2, "VALID", activation = tf.nn.relu, kernel_initializer = init)
    conv = tf.layers.conv2d(conv, 64, 3, 1, "VALID", activation = tf.nn.relu, kernel_initializer = init)

    conv = tf.layers.flatten(conv)

    advantage_dense = tf.layers.dense(conv, 512, tf.nn.relu, kernel_initializer = init)
    value_dense = tf.layers.dense(conv, 512, tf.nn.relu, kernel_initializer = init)

    advantage = tf.layers.dense(advantage_dense, num_actions)
    value = tf.layers.dense(value_dense, 1)

    q_values = value + (advantage - tf.reduce_mean(advantage, 1, True))

    return flattened_state, q_values

def create_graph(num_actions):
    curr_state, online_q_values = create_model(num_actions)
    online_params = tf.trainable_variables()

    next_state, target_q_values = create_model(num_actions)
    target_params = tf.trainable_variables()[len(online_params):]

    update_target_smooth = []
    for i in range(len(target_params)):
        update_target_smooth.append(target_params[i].assign(tau * target_params[i] + (1 - tau) * online_params[i]))

    update_target = []
    for i in range(len(target_params)):
        update_target.append(target_params[i].assign(online_params[i]))

    predict_action = tf.argmax(online_q_values, 1)
    target = tf.placeholder(tf.float32, [None])
    action = tf.placeholder(tf.int32, [None])
    one_hot_action = tf.one_hot(action, num_actions, dtype = tf.float32)
    loss = tf.reduce_mean(clip_loss(target - tf.reduce_sum(online_q_values * one_hot_action, 1)))

    optimizer = tf.train.AdamOptimizer(learning_rate = learn_rate)
    update_online = optimizer.minimize(loss, var_list = online_params)

    return curr_state, online_q_values, predict_action, target, action, \
           update_online, next_state, target_q_values, update_target, update_target_smooth

def train(sess):
    env = create_env()
    num_actions = env.actions

    op_curr_state, op_online_q_values, op_predict_action, op_target, op_action, \
    op_update_online, op_next_state, op_target_q_values, op_update_target, op_update_target_smooth = create_graph(num_actions)

    saver = tf.train.Saver()

    sess.run(tf.global_variables_initializer())

    sess.run(op_update_target)

    e_greedy_curr = e_greedy_start
    exp_buffer = ExperienceBuffer(exp_buffer_size)

    total_steps = 0
    reward_list = []
    step_list = []

    for episode in range(1, total_episodes + 1):
        curr_state = reset_env(env)
        ep_reward = 0.0
        steps = 0

        for steps in range(1, episode_steps + 1):
            total_steps += 1

            # epsilon greedy action selection
            if total_steps <= num_rand_steps or random.random() < e_greedy_curr:
                action = random.randrange(num_actions)
            else:
                online_q_values = sess.run(op_online_q_values, feed_dict = {op_curr_state: to_flat_state([curr_state])})
                action = np.argmax(online_q_values)

            next_state, reward, done = env.step(action)
            ep_reward += reward

            exp_buffer.append([curr_state, action, reward, next_state, done])

            if total_steps > num_rand_steps:
                if e_greedy_curr > e_greedy_end:
                    e_greedy_curr -= e_greedy_diff

                # update offline model (less frequent)
                if total_steps % target_update_freq == 0:
                    sess.run(op_update_target_smooth)

                # update online model (more frequent)
                # double q network approach
                if total_steps % online_update_freq == 0:
                    # gets a batch of randomly selected experiences
                    batch = exp_buffer.sample(batch_size)
                    batch_prev_state, batch_action, batch_reward, batch_state, batch_done = batch
                    batch_prev_state = to_flat_state(batch_prev_state)
                    batch_state = to_flat_state(batch_state)

                    actions = sess.run(op_predict_action, feed_dict = {op_curr_state: batch_state})
                    target_q_values = sess.run(op_target_q_values, feed_dict = {op_next_state: batch_state})
                    double_q_values = target_q_values[range(batch_size), actions]
                    not_done = -(batch_done - 1)
                    target = batch_reward + (gamma * double_q_values * not_done)
                    sess.run(op_update_online, feed_dict = {op_curr_state: batch_prev_state,
                                                            op_action: batch_action,
                                                            op_target: target})

            curr_state = next_state

            if done:
                break

        reward_list.append(ep_reward)
        step_list.append(steps)

        if episode % print_freq == 0:
            print("is pre training:", total_steps <= num_rand_steps,
                  "| ep:", episode,
                  "| step:", total_steps,
                  "| avg reward:", np.mean(reward_list[-print_freq:]),
                  "| avg ep length:", np.mean(step_list[-print_freq:]))

        if episode % save_freq == 0:
            saver.save(sess, save_path + "/dddqn_model_" + str(episode) + ".ckpt")
            print("Saved current model!")

    saver.save(sess, save_path + "/dddqn_model_final.ckpt")
    print("Saved final model!")

    skip = 100
    reward_avg = np.average(np.reshape(reward_list, [len(reward_list) // skip, skip]), 1)
    step_avg = np.average(np.reshape(step_list, [len(step_list) // skip, skip]), 1)

    plt.subplot(2, 1, 1)
    plt.plot([(x + 1) * skip for x in range(len(reward_avg))], reward_avg)
    plt.xlabel("Ep")
    plt.ylabel("Average Reward Per " + str(skip) + " Ep")

    plt.subplot(2, 1, 2)
    plt.plot([(x + 1) * skip for x in range(len(step_avg))], step_avg)
    plt.xlabel("Ep")
    plt.ylabel("Average Ep Length Per " + str(skip) + " Ep")

    plt.show()

def test(sess):
    env = create_env()
    num_actions = env.actions

    op_curr_state, op_online_q_values, op_predict_action, op_target, op_action, \
    op_update_online, op_next_state, op_target_q_values, op_update_target, op_update_target_smooth = create_graph(num_actions)

    saver = tf.train.Saver()
    saver.restore(sess, load_path)
    print("Loaded saved model!")

    while True:
        curr_state = reset_env(env)
        ep_reward = 0.0
        steps = 0

        for steps in range(1, episode_steps + 1):
            env.renderEnv(True)

            if random.random() < e_greedy_test:
                action = random.randrange(num_actions)
            else:
                online_q_values = sess.run(op_online_q_values, feed_dict={op_curr_state: to_flat_state([curr_state])})
                action = np.argmax(online_q_values)

            next_state, reward, done = env.step(action)
            ep_reward += reward

            if done:
                break

        print("ep reward:", ep_reward, "| ep length:", steps)

if __name__ == "__main__":
    start = time.process_time()

    if is_testing:
        print("Started testing.")

        tf.reset_default_graph()
        with tf.Session() as sess:
            test(sess)

        print("Ended testing.")
    else:
        print("Started training.")

        tf.reset_default_graph()
        with tf.Session() as sess:
            train(sess)

        print("Ended training.")

    print("End time:", datetime.timedelta(seconds = time.process_time() - start))
