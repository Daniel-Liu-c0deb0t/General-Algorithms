import numpy as np
import tflearn


def generate_answers(data):
    answers = []
    for row in data:
        answers.append(sum(row))
    return np.array(answers)

train_data_count = 50000
test_data_count = 10000
num_count = 2

net = tflearn.input_data(shape=(None, num_count))
net = tflearn.fully_connected(net, 4)
net = tflearn.fully_connected(net, 2)
net = tflearn.fully_connected(net, 1, activation="linear")
net = tflearn.reshape(net, [-1])
net = tflearn.regression(net, optimizer="adam", loss="mean_square", learning_rate=0.01)
model = tflearn.DNN(net)

train_data = np.random.randint(500, size=(train_data_count, num_count))
train_answers = generate_answers(train_data)
model.fit(train_data, train_answers, n_epoch=10, batch_size=1000, show_metric=True)

test_data = np.random.randint(500, size=(test_data_count, num_count))
test_answers = generate_answers(test_data)
predictions = model.predict(test_data)

count = 0
deviation = 0
for i in range(test_data_count):
    print("answer:", test_answers[i], "prediction:", predictions[i])
    deviation += abs(test_answers[i] - predictions[i])
    if abs(test_answers[i] - predictions[i]) < 5:
        count += 1
print("correct:", count, "/", test_data_count)
print("deviation:", deviation / test_data_count)
