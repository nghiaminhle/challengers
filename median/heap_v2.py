import heapq
from heapq import heappush, heappop


class MedianStore:
    lower = []
    upper = []
    center = None

    def __init__(self):
        self.lower = []
        self.upper = []
        self.center = None

    def add_number(self, value):
        if self.center == None:
            self.center = value
            heappush(self.lower, -1 * value)
        elif value <= self.center:
            heappush(self.lower, -1 * value)
        else:
            heappush(self.upper, value)
        if len(self.lower) < len(self.upper) - 1:
            self.center = heappop(self.upper)
            heappush(self.lower, -1 * self.center)
        elif len(self.upper) < len(self.lower) - 1:
            self.center = -1 * heappop(self.lower)
            heappush(self.upper, self.center)
        elif len(self.lower) == len(self.upper) + 1:
            self.center = -1 * self.lower[0]
        elif len(self.upper) == len(self.lower) + 1:
            self.center = self.upper[0]

    def get_median(self):
        if len(self.upper) == len(self.lower):
            return (-1*self.lower[0]+self.upper[0]) / 2
        return self.center


def main():
    testcases = [
        [[1, 3, 9, 5, 7, 5, 0, 4, 3, 2, 9, 1, 0], [1, 2, 3, 4, 5, 5, 5, 4.5, 4, 3.5, 4, 3.5, 3]],
        [[6, 1, 2], [6, 3.5, 2]],
        [[3, 9, 2, 5, 2], [3, 6, 3, 4, 3]],
        [[5, 5, 5, 5], [5, 5, 5, 5]],
        [[9, 6, 4, 3, 1], [9, 7.5, 6, 5, 4]],
        [[1, 2, 3, 4], [1, 1.5, 2, 2.5]],
        [[1, 3, 2], [1, 2, 2]],
        [[1], [1]]
    ]

    for case in testcases:
        median_list = MedianStore()
        print('Executing test case %s' % case[0])
        for k, number in enumerate(case[0]):
            median_list.add_number(number)
            assert median_list.get_median() == case[1][k]


if __name__ == "__main__":
    main()