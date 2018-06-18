import tflearn as tf
import numpy as np

net = tf.input_data(shape=(None, 2))
net = tf.fully_connected(net, 2, activation="sigmoid")
net = tf.fully_connected(net, 1, activation="linear")
net = tf.reshape(net, [-1])
net = tf.regression(net, optimizer="adam", loss="mean_square", learning_rate=0.1)
model = tf.DNN(net)

trainX = [[0, 0], [1, 0], [0, 1], [1, 1]]
trainY = [0, 1, 1, 0]

model.fit(trainX, trainY, n_epoch=2000, batch_size=4)

print("Predict [0, 0]:", np.round(model.predict([[0, 0]])).astype(int))
print("Predict [1, 0]:", np.round(model.predict([[1, 0]])).astype(int))
print("Predict [0, 1]:", np.round(model.predict([[0, 1]])).astype(int))
print("Predict [1, 1]:", np.round(model.predict([[1, 1]])).astype(int))
