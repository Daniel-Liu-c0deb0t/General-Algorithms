def kmp_preprocess(pattern):
    partial_match = [0] * (len(pattern) + 1)
    i, j, partial_match[0] = 0, -1, -1
    while i < len(pattern):
        while j >= 0 and pattern[i] != pattern[j]:
            j = partial_match[j]
        i += 1
        j += 1
        partial_match[i] = j
    return partial_match


def kmp_match(string, pattern, partial_match):
    i, j = 0, 0
    result = []
    while i < len(string):
        while j >= 0 and string[i] != pattern[j]:
            j = partial_match[j]
        i += 1
        j += 1
        if j == len(pattern):
            result.append(i - j)
            j = partial_match[j]
    if result:
        return result
    else:
        return None

s = "coding is a very cool activity that involves a lot of typing code on the computer, which can be tiring"
p = "writing"
print(kmp_match(s, p, kmp_preprocess(p)))
