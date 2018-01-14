# range max, single replace
class SegmentTree1:
    def __init__(self, data):
        self.size = len(data)
        self.tree = ([0] * self.size) + data
        for i in reversed(range(self.size)):
            self.tree[i] = max(self.tree[i * 2], self.tree[i * 2 + 1])

    def single_replace(self, p, val):
        p += self.size
        self.tree[p] = val
        while p > 1:
            self.tree[p // 2] = max(self.tree[p], self.tree[p - 1])
            p //= 2

    def range_max(self, start, end):
        res = -10000000000
        start += self.size
        end += self.size
        while start < end:
            if start % 2 == 1:
                res = max(res, self.tree[start])
                start += 1
            if end % 2 == 1:
                end -= 1
                res = max(res, self.tree[end])
            start //= 2
            end //= 2
        return res


# range max, range increment
class SegmentTree2:
    def __init__(self, data):
        self.size = len(data)
        self.tree = ([0] * self.size) + data
        self.lazy = [0] * self.size
        for i in reversed(range(self.size)):
            self.tree[i] = max(self.tree[i * 2], self.tree[i * 2 + 1])

    def build(self, p):
        while p > 1:
            p //= 2
            self.tree[p] = max(self.tree[p * 2], self.tree[p * 2 + 1]) + self.lazy[p]

    def apply(self, p, val):
        self.tree[p] += val
        if p < self.size:
            self.lazy[p] += val

    def push(self, p):
        for s in range(self.size.bit_length() - 1, 0, -1):
            i = p // 2 ** s
            if self.lazy[i] != 0:
                self.apply(i * 2, self.lazy[i])
                self.apply(i * 2 + 1, self.lazy[i])
                self.lazy[i] = 0

    def range_increment(self, start, end, val):
        start += self.size
        end += self.size
        start2, end2 = start, end
        while start < end:
            if start % 2 == 1:
                self.apply(start, val)
                start += 1
            if end % 2 == 1:
                end -= 1
                self.apply(end, val)
            start //= 2
            end //= 2
        self.build(start2)
        self.build(end2 - 1)

    def range_max(self, start, end):
        res = -10000000000
        start += self.size
        end += self.size
        self.push(start)
        self.push(end - 1)
        while start < end:
            if start % 2 == 1:
                res = max(res, self.tree[start])
                start += 1
            if end % 2 == 1:
                end -= 1
                res = max(res, self.tree[end])
            start //= 2
            end //= 2
        return res


# range sum, range replace
class SegmentTree3:
    def __init__(self, data):
        self.size = len(data)
        self.tree = ([0] * self.size) + data
        self.lazy = [0] * self.size
        for i in reversed(range(self.size)):
            self.tree[i] = max(self.tree[i * 2], self.tree[i * 2 + 1])

#    def build(self, start, end):
#        k = 2
#        start += self.size
#        end += self.size - 1
#        while start > 1:
#            start //= 2
#            end //= 2
#            for i in range(end, start - 1, -1):
#                self.calc(i, k)
#            k *= 2

    def apply(self, p, val, k):
        self.tree[p] = val * k
        if p < self.size:
            self.lazy[p] = val

    def calc(self, p, k):
        if self.lazy[p] == 0:
            self.tree[p] = self.tree[p * 2] + self.tree[p * 2 + 1]
        else:
            self.tree[p] = self.lazy[p] * k

    def push(self, start, end):
        start += self.size
        end += self.size - 1
        s = self.size.bit_length() - 1
        k = 2 ** (s - 1)
        while s > 0:
            for i in range(start // 2 ** s, end // 2 ** s + 1):
                if self.lazy[i] != 0:
                    self.apply(i * 2, self.lazy[i], k)
                    self.apply(i * 2 + 1, self.lazy[i], k)
                    self.lazy[i] = 0
            s -= 1
            k //= 2

    def range_replace(self, start, end, val):
        self.push(start, start + 1)
        self.push(end - 1, end)
        c_start, c_end = False, False
        k = 1
        start += self.size
        end += self.size
        while start < end:
            if c_start:
                self.calc(start - 1, k)
            if c_end:
                self.calc(end, k)
            if start % 2 == 1:
                self.apply(start, val, k)
                start += 1
                c_start = True
            if end % 2 == 1:
                end -= 1
                self.apply(end, val, k)
                c_end = True
            start //= 2
            end //= 2
            k *= 2
        start -= 1
        while end > 0:
            if c_start:
                self.calc(start, k)
            if c_end and (not c_start or start != end):
                self.calc(end, k)
            start //= 2
            end //= 2
            k *= 2

    def range_sum(self, start, end):
        res = 0
        self.push(start, start + 1)
        self.push(end - 1, end)
        start += self.size
        end += self.size
        while start < end:
            if start % 2 == 1:
                res += self.tree[start]
                start += 1
            if end % 2 == 1:
                end -= 1
                res += self.tree[end]
            start //= 2
            end //= 2
        return res

tree1 = SegmentTree1([1, 2, 3, 4, 5, 6])
tree1.single_replace(2, 10)
print(tree1.range_max(0, tree1.size))

tree2 = SegmentTree2([1, 2, 3, 4, 5, 6])
tree2.range_increment(3, tree2.size, 10)
tree2.range_increment(0, 3, 14)
tree2.range_increment(0, tree2.size, 0)
print(tree2.range_max(0, tree2.size))

tree3 = SegmentTree3([1, 2, 3, 4, 5, 6])
tree3.range_replace(0, tree3.size, 10)
tree3.range_replace(0, 3, 5)
tree3.range_replace(2, tree3.size, 0)
print(tree3.range_sum(0, tree3.size))
