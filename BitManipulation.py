def one(data, i):
    return data | (1 << i)


def zero(data, i):
    return data & ~(1 << i)


def toggle(data, i):
    return data ^ (1 << i)


def get(data, i):
    return (data >> i) & 1


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


def trailing_zeros(data):
    return (data & -data).bit_length() - 1

test = 0
test = one(test, 1)
test = one(test, 2)
test = zero(test, 1)
test = toggle(test, 0)
print(get(test, 0), get(test, 1), get(test, 2))
print(str(bin(test))[2:])
print(test)
for j in ones(test):
    print(j)
print(count_ones(test))
print(trailing_zeros(test))
