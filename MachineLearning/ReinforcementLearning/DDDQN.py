import ExperienceReplay
import time
import datetime
import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from gridworld import gameEnv
import random

# testing or training?
is_testing = False

# hyperparameters
learn_rate = 0.00025
num_noops = 3
total_episodes = 5000
episode_steps = 50

target_update_freq = 5000
print_freq = 10

img_width = 84
img_height = 84
img_channel = 3

tau = 0.001
gamma = 0.99

batch_size = 32
# will take random steps in the beginning to fill buffer
exp_buffer_size = 10000
priority_replay = True
priority_e = 0.01
priority_a = 0.6

# controls annealing rate for epsilon greedy
e_greedy_start = 1.0
e_greedy_end = 0.1
e_greedy_steps = 10000
e_greedy_test = 0.1

save_freq = 1000
save_path = "./dddqn_saves_priority"
load_path = "./dddqn_saves_priority/dddqn_model_final.ckpt"

e_greedy_diff = (e_greedy_start - e_greedy_end) / e_greedy_steps
os.makedirs(save_path, exist_ok = True)

def to_flat_state(state):
    np_state = np.array(state)
    shape = np_state.shape
    return np.reshape(state, [shape[0], shape[1] * shape[2] * shape[3]]) / 255.0

def huber_loss(loss):
    return tf.where(tf.abs(loss) < 1.0, 0.5 * tf.square(loss), tf.abs(loss) - 0.5)

def to_priority(error):
    return (error + priority_e) ** priority_a

def create_env():
    return gameEnv(False, 5, True)

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

    # updates the target network towards the online network
    update_target_smooth = []
    for i in range(len(target_params)):
        update_target_smooth.append(target_params[i].assign(tau * target_params[i] + (1 - tau) * online_params[i]))

    update_target = []
    for i in range(len(target_params)):
        update_target.append(target_params[i].assign(online_params[i]))

    target = tf.placeholder(tf.float32, [None])
    action = tf.placeholder(tf.int32, [None])
    one_hot_action = tf.one_hot(action, num_actions, dtype = tf.float32)
    loss = tf.reduce_mean(huber_loss(target - tf.reduce_sum(online_q_values * one_hot_action, 1)))

    optimizer = tf.train.AdamOptimizer(learning_rate = learn_rate)
    update_online = optimizer.minimize(loss, var_list = online_params)

    return curr_state, online_q_values, target, action, \
           update_online, next_state, target_q_values, update_target, update_target_smooth

def train(sess):
    start = time.perf_counter()

    env = create_env()
    num_actions = env.actions

    op_curr_state, op_online_q_values, op_target, op_action, op_update_online, \
    op_next_state, op_target_q_values, op_update_target, op_update_target_smooth = create_graph(num_actions)

    saver = tf.train.Saver()

    sess.run(tf.global_variables_initializer())

    sess.run(op_update_target)

    e_greedy_curr = e_greedy_start

    if priority_replay:
        exp_buffer = ExperienceReplay.PriorityBuffer(exp_buffer_size)
    else:
        exp_buffer = ExperienceReplay.UniformBuffer(exp_buffer_size)

    total_steps = 0
    reward_list = []
    step_list = []

    for episode in range(1, total_episodes + 1):
        curr_state = reset_env(env)
        ep_reward = 0.0
        steps = 0

        for steps in range(1, episode_steps + 1):
            total_steps += 1

            online_q_values = None
            # epsilon greedy action selection
            if total_steps <= exp_buffer_size or random.random() < e_greedy_curr:
                action = random.randrange(num_actions)
            else:
                online_q_values = sess.run(op_online_q_values,
                                           feed_dict = {op_curr_state: to_flat_state([curr_state])})
                action = np.argmax(online_q_values)

            next_state, reward, done = env.step(action)
            ep_reward += reward
            error = abs(reward) # default error is reward

            if total_steps > exp_buffer_size:
                if e_greedy_curr > e_greedy_end:
                    e_greedy_curr -= e_greedy_diff

                # update offline model (less frequent)
                if total_steps % target_update_freq == 0:
                    sess.run(op_update_target_smooth)

                # update online model (more frequent)
                # double q network approach
                # gets a batch of randomly selected experiences
                idx, batch = exp_buffer.sample(batch_size)
                batch_prev_state, batch_action, batch_reward, batch_state, batch_done = batch
                batch_prev_state = to_flat_state(batch_prev_state)
                batch_state = to_flat_state(batch_state)

                if priority_replay:
                    if online_q_values is None:
                        online_q_values = sess.run(op_online_q_values,
                                                   feed_dict = {op_curr_state: to_flat_state([curr_state])})

                    # calculate the error for the current (s, a, r, s', d)
                    online_next_q = sess.run(op_online_q_values,
                                             feed_dict = {op_curr_state: to_flat_state([next_state])})
                    target_next_q = sess.run(op_target_q_values,
                                             feed_dict = {op_next_state: to_flat_state([next_state])})
                    double_q_value = target_next_q[0][np.argmax(online_next_q)]
                    target = reward + (gamma * double_q_value * (1 - done))
                    error = abs(target - online_q_values[0][action])

                    # calculate the batch targets for training and the errors
                    batch_online_q = sess.run(op_online_q_values, feed_dict = {op_curr_state: batch_state})
                    actions = np.argmax(batch_online_q, 1)
                    batch_target_q = sess.run(op_target_q_values, feed_dict = {op_next_state: batch_state})
                    batch_double_q = batch_target_q[range(batch_size), actions]
                    target = batch_reward + (gamma * batch_double_q * (1 - batch_done))
                    errors = abs(target - batch_online_q[range(batch_size), actions])

                    # update the priorities for the batch elements with new errors
                    for i in range(batch_size):
                        exp_buffer.update(idx[i], errors[i])

                    # train online model
                    sess.run(op_update_online, feed_dict = {op_curr_state: batch_prev_state,
                                                            op_action: batch_action,
                                                            op_target: target})
                else:
                    # just update online model with target values
                    batch_online_q = sess.run(op_online_q_values, feed_dict = {op_curr_state: batch_state})
                    actions = np.argmax(batch_online_q, 1)
                    batch_target_q = sess.run(op_target_q_values, feed_dict = {op_next_state: batch_state})
                    batch_double_q = batch_target_q[range(batch_size), actions]
                    target = batch_reward + (gamma * batch_double_q * (1 - batch_done))
                    sess.run(op_update_online, feed_dict = {op_curr_state: batch_prev_state,
                                                            op_action: batch_action,
                                                            op_target: target})

            if priority_replay:
                exp_buffer.append([curr_state, action, reward, next_state, done], to_priority(error))
            else:
                exp_buffer.append([curr_state, action, reward, next_state, done])

            curr_state = next_state

            if done:
                break

        reward_list.append(ep_reward)
        step_list.append(steps)

        if episode % print_freq == 0:
            print("is pre training:", total_steps <= exp_buffer_size,
                  "| ep:", episode,
                  "| step:", total_steps,
                  "| avg reward:", np.mean(reward_list[-print_freq:]),
                  "| avg ep length:", np.mean(step_list[-print_freq:]))

        if episode % save_freq == 0:
            saver.save(sess, save_path + "/dddqn_model_" + str(episode) + ".ckpt")
            print("Saved current model!")

    saver.save(sess, save_path + "/dddqn_model_final.ckpt")
    print("Saved final model!")

    print("Total time:", datetime.timedelta(seconds = time.perf_counter() - start))

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

    plt.savefig(save_path + "/dddqn_train_result.png")
    plt.show()

def test(sess):
    env = create_env()
    num_actions = env.actions

    op_curr_state, op_online_q_values, op_target, op_action, op_update_online, \
    op_next_state, op_target_q_values, op_update_target, op_update_target_smooth = create_graph(num_actions)

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
                online_q_values = sess.run(op_online_q_values, feed_dict = {op_curr_state: to_flat_state([curr_state])})
                action = np.argmax(online_q_values)

            next_state, reward, done = env.step(action)
            ep_reward += reward
            curr_state = next_state

            if done:
                break

        print("ep reward:", ep_reward, "| ep length:", steps)

if __name__ == "__main__":
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
