from collections import deque
import random
import numpy as np

# simple buffer where the probability of selecting an experience is uniform
class UniformBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = deque(maxlen = size)

    def append(self, exp):
        self.buffer.append(exp)

    def sample(self, num):
        res = np.array(random.sample(self.buffer, num))
        return None, [np.stack(res[:, 0]), res[:, 1], res[:, 2], np.stack(res[:, 3]), res[:, 4]]

# buffer where the probability of selecting an experience is based on a priority
# higher priority = selected more often
# why calculate prefix sum?
# - consider each priority as a segment on a line (higher priority = longer segment)
# - pick one location on the line as find the segment containing that location
# - longer segments are picked more often, achieving the goal
# prefix sum allows the above situation to be replicated without making the line
class PriorityBuffer:
    def __init__(self, size):
        self.size = size
        self.write_pos = 0
        # tree with n leaves has 2 * n - 1 nodes
        self.priority = [0 for i in range(2 * size - 1)]
        self.buffer = [None for i in range(size)]

    def append(self, exp, priority):
        idx = self.size + self.write_pos - 1
        self.update(idx, priority)
        self.buffer[self.write_pos] = exp

        # make the write pointer circle back if the end is reached
        self.write_pos += 1
        if self.write_pos >= self.size:
            self.write_pos = 0

    def update_diff(self, idx, diff):
        self.priority[idx] += diff
        if idx > 0:
            self.update_diff((idx - 1) // 2, diff)

    def update(self, idx, priority):
        self.update_diff(idx, priority - self.priority[idx])

    def sample(self, num):
        res = []
        idx = []
        for i in range(num):
            # get random experiences using random numbers less than the sum of all priorities
            rand = random.uniform(0, self.priority[0])
            j = self.get(0, rand)
            idx.append(j)
            res.append(self.buffer[j - self.size + 1])
        res = np.array(res)
        return idx, [np.stack(res[:, 0]), res[:, 1], res[:, 2], np.stack(res[:, 3]), res[:, 4]]

    def get(self, idx, priority):
        lo = idx * 2 + 1
        hi = idx * 2 + 2
        if lo >= len(self.priority): # if current node is leaf
            return idx

        if priority <= self.priority[lo]:
            return self.get(lo, priority)
        else:
            return self.get(hi, priority - self.priority[lo])

if __name__ == "__main__":
    b = PriorityBuffer(5)
    b.append([1] * 5, 0.1)
    b.append([2] * 5, 1)
    b.append([3] * 5, 1)
    b.append([4] * 5, 1)
    b.append([5] * 5, 1)
    b.append([6] * 5, 5)
    for _ in range(10):
        print(b.sample(2))