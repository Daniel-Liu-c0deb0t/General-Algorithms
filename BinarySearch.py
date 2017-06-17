def binary_search(arr, val, left_most):
    l, r, res = 0, len(arr) - 1, None
    while l <= r:
        mid = l + (r - l) // 2
        if arr[mid] == val:
            res = mid
            if left_most:
                r = mid - 1
            else:
                l = mid + 1
        elif arr[mid] > val:
            r = mid - 1
        else:
            l = mid + 1
    return res

print(binary_search([1, 2, 3, 4, 5, 5, 5, 8, 9, 10], 5, True))
