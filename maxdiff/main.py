def maxdiff(a):
    n = len(a)
    maximum_values = {}
    max_value = a[n-1]
    for i in range(n-1, 0, -1):
        if max_value< a[i]:
            max_value = a[i]
        maximum_values[n-i] = max_value
    max_dif = a[1]-a[0]
    for i in range(n-1):
        if maximum_values[n-1-i] - a[i]> max_dif:
            max_dif = maximum_values[n-1-i] - a[i]
    return max_dif
    
def main():
    print('find maximum difference')
    inputs = [
        [1, 2],
        [4, 7, 1, 3, 2, 9],
        [1, 2, 3, 4, 5, 6],
        [4, 3, 2, 1],
        [3, 3, 3],
        [-1, 7, 1, 3, 2, 9],
        [4, 1, 3, 9, 2, -2, 3]
    ]
    outputs = [
        1,
        8,
        5,
        -1,
        0,
        10,
        8
    ]
    for i in range(len(inputs)):
        print('Executing test case: %s' % inputs[i])
        assert maxdiff(inputs[i]) == outputs[i]

if __name__ == "__main__":
    main()