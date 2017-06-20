class SegmentTreeSum:
    seg_tree = []
    size = 0

    def __init__(self, data):
        self.size = len(data)
        tree_size = 2 * len(data) - 1
        # max, lazy
        self.seg_tree = [[0, 0] for i in range(tree_size)]
        self.recursive_init(data, 0, len(data) - 1, 0)

    def recursive_init(self, data, curr_start, curr_end, i):
        if curr_start > curr_end:
            return
        if curr_start == curr_end:
            self.seg_tree[i][0] = data[curr_start]
            return
        mid = curr_start + (curr_end - curr_start) // 2
        self.recursive_init(data, curr_start, mid, i * 2 + 1)
        self.recursive_init(data, mid + 1, curr_end, i * 2 + 2)
        self.seg_tree[i][0] = self.seg_tree[i * 2 + 1][0] + self.seg_tree[i * 2 + 2][0]

    def range_add(self, seg_start, seg_end, val):
        self.recursive_range_add(0, self.size - 1, seg_start, seg_end, 0, val)

    def recursive_range_add(self, curr_start, curr_end, seg_start, seg_end, i, val):
        if self.seg_tree[i][1] != 0:
            self.seg_tree[i][0] += self.seg_tree[i][1] * (curr_end - curr_start + 1)
            if curr_start != curr_end:
                self.seg_tree[i * 2 + 1][1] += self.seg_tree[i][1]
                self.seg_tree[i * 2 + 2][1] += self.seg_tree[i][1]
            self.seg_tree[i][1] = 0
        if curr_start > curr_end or curr_start > seg_end or curr_end < seg_start:
            return
        if curr_start >= seg_start and curr_end <= seg_end:
            self.seg_tree[i][0] += val * (curr_end - curr_start + 1)
            if curr_start != curr_end:
                self.seg_tree[i * 2 + 1][1] += val
                self.seg_tree[i * 2 + 2][1] += val
            return
        mid = curr_start + (curr_end - curr_start) // 2
        self.recursive_range_add(curr_start, mid, seg_start, seg_end, i * 2 + 1, val)
        self.recursive_range_add(mid + 1, curr_end, seg_start, seg_end, i * 2 + 2, val)
        self.seg_tree[i][0] = self.seg_tree[i * 2 + 1][0] + self.seg_tree[i * 2 + 2][0]

    def range_sum(self, seg_start, seg_end):
        return self.recursive_range_sum(0, self.size - 1, seg_start, seg_end, 0)

    def recursive_range_sum(self, curr_start, curr_end, seg_start, seg_end, i):
        if self.seg_tree[i][1] != 0:
            self.seg_tree[i][0] += self.seg_tree[i][1] * (curr_end - curr_start + 1)
            if curr_start != curr_end:
                self.seg_tree[i * 2 + 1][1] += self.seg_tree[i][1]
                self.seg_tree[i * 2 + 2][1] += self.seg_tree[i][1]
            self.seg_tree[i][1] = 0
        if curr_start > curr_end or curr_start > seg_end or curr_end < seg_start:
            return 0
        if curr_start >= seg_start and curr_end <= seg_end:
            return self.seg_tree[i][0]
        mid = curr_start + (curr_end - curr_start) // 2
        return self.recursive_range_sum(curr_start, mid, seg_start, seg_end, i * 2 + 1) + \
               self.recursive_range_sum(mid + 1, curr_end, seg_start, seg_end, i * 2 + 2)


class SegmentTreeMax:
    seg_tree = []
    size = 0

    def __init__(self, data):
        self.size = len(data)
        tree_size = 2 * len(data)
        # start, end, max, offset
        self.seg_tree = [[None, None, 0, 0] for i in range(tree_size)]
        self.recursive_init(data, 1, len(data), 1)

    def recursive_init(self, data, curr_start, curr_end, i):
        if curr_start == curr_end:
            self.seg_tree[i] = [curr_start, curr_end, data[curr_start - 1], 0]
            return
        else:
            self.seg_tree[i] = [curr_start, curr_end, 0, 0]
        mid = curr_start + (curr_end - curr_start) // 2
        self.recursive_init(data, curr_start, mid, i * 2)
        self.recursive_init(data, mid + 1, curr_end, i * 2 + 1)
        self.seg_tree[i][2] = max(self.seg_tree[i * 2][2], self.seg_tree[i * 2 + 1][2])

    def range_add(self, seg_start, seg_end, val):
        seg_start += 1
        seg_end += 1
        self.recursive_range_add(1, self.size, seg_start, seg_end, 1, val)

    def recursive_range_add(self, curr_start, curr_end, seg_start, seg_end, i, val):
        if curr_start > curr_end or curr_start > seg_end or curr_end < seg_start:
            return
        if curr_start >= seg_start and curr_end <= seg_end:
            self.seg_tree[i][2] += val
            self.seg_tree[i][3] += val
            return
        mid = curr_start + (curr_end - curr_start) // 2
        self.recursive_range_add(curr_start, mid, seg_start, seg_end, i * 2, val)
        self.recursive_range_add(mid + 1, curr_end, seg_start, seg_end, i * 2 + 1, val)
        self.seg_tree[i][2] = max(self.seg_tree[i * 2][2], self.seg_tree[i * 2 + 1][2]) + self.seg_tree[i][3]

    def range_max(self, range_start, range_end):
        range_start += 1
        range_end += 1
        return self.recursive_range_max(range_start, range_end, 1, 0)

    def recursive_range_max(self, range_start, range_end, i, offset):
        if self.seg_tree[i][0] == range_start and self.seg_tree[i][1] == range_end:
            return self.seg_tree[i][2] + offset
        mid = self.seg_tree[i][0] + (self.seg_tree[i][1] - self.seg_tree[i][0]) // 2
        offset += self.seg_tree[i][3]
        if range_end <= mid:
            return self.recursive_range_max(range_start, range_end, i * 2, offset)
        elif range_start > mid:
            return self.recursive_range_max(range_start, range_end, i * 2 + 1, offset)
        else:
            return max(self.recursive_range_max(range_start, mid, i * 2, offset),
                       self.recursive_range_max(mid + 1, range_end, i * 2 + 1, offset))

tree = SegmentTreeSum([1, 3, 6, 2, 0, 9, 8, 10, 11])
print(tree.range_sum(0, 3))
tree.range_add(0, 3, 10)
print(tree.range_sum(0, 7))
print([tree.range_sum(i, i) for i in range(tree.size)])

tree2 = SegmentTreeMax([1, 3, 6, 2, 0, 9, 8, 10, 11])
print(tree2.range_max(0, 3))
tree2.range_add(3, 3, 11)
print(tree2.range_max(0, 3))
tree2.range_add(3, 5, 11)
print(tree2.range_max(0, 8))
print([tree2.range_max(i, i) for i in range(tree2.size)])
