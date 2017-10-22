"""
The idea of algorithm is to find a maximum values of the rest set when iterate over each element.
It's made by iterated array in reverse to find the maximum value for each set.
"""

def maxdiff(a):
    max_value = a[len(a) - 1]
    max_dif = a[1] - a[0]
    for i in range(len(a) - 1, 0, -1):
        max_value = a[i] if max_value < a[i] else max_value
        max_dif = (max_value-a[i - 1]) if (max_value - a[i - 1] > max_dif) else max_dif
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
