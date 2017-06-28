def mask(start, end):
    return ((1 << start) - 1) ^ ((1 << end) - 1)


def one(data, i):
    return data | (1 << i)


def one_range(data, start, end):
    return data | mask(start, end)


def zero(data, i):
    return data & ~(1 << i)


def zero_range(data, start, end):
    return data & ~mask(start, end)


def flip(data, i):
    return data ^ (1 << i)


def flip_range(data, start, end):
    return data ^ mask(start, end)


def flip_all(data):
    return data ^ ((1 << data.bit_length()) - 1)


def get(data, i):
    return (data >> i) & 1


def get_range(data, start, end):
    return (data >> start) & mask(0, end - start)


def ones(data):
    while data > 0:
        yield (data & -data).bit_length() - 1
        data &= data - 1


def count_ones(data):
    count = 0
    while data > 0:
        data &= data - 1
        count += 1
    return count


def zeroes(data):
    data = flip_all(data)
    while data > 0:
        yield (data & -data).bit_length() - 1
        data &= data - 1


def count_zeroes(data):
    data = flip_all(data)
    count = 0
    while data > 0:
        data &= data - 1
        count += 1
    return count


def trailing_zeros(data):
    return (data & -data).bit_length() - 1

test = 0
test = one(test, 1)
test = one(test, 2)
test = zero(test, 1)
test = flip(test, 0)
print(str(bin(flip_all(test))))
print(get(test, 0), get(test, 1), get(test, 2))
print(str(bin(test)))
print(test)
print([j for j in ones(test)])
print(count_ones(test))
print(trailing_zeros(test))
print([j for j in zeroes(test)])
print(count_zeroes(test))
print(str(bin(mask(1, 10))))
print(str(bin(one_range(0, 1, 10))))
print(str(bin(zero_range(0b111111111111, 1, 10))))
print(str(bin(flip_range(0, 5, 10))))
print(str(bin(get_range(0b10110011100011110000, 1, 12))))
