
"""

The algorithm is to iterate over string S by one. At every step,
find the most optimized windows size that contain all characters of T. When a windows is found:
- if it's size is equal length of T, stop because it is the best solution
- else compare with already solution for choose the better.
- then remove the left element of the windows to continue find a other better windows size

"""
import collections

def find_minimum_windows(s, t):
    if len(t) > len(s):
        return None
    t_chars = {}
    for i in range(len(t)):
        if not t[i] in t_chars.keys():
            t_chars[t[i]] = 0
        t_chars[t[i]] += 1
    best_from = 0
    best_to = len(s) - 1
    count = len(t)
    has_solution = False
    found_chars = {}
    windows = collections.OrderedDict()
    for i in range(len(s)):
        if s[i] in t_chars.keys():
            if not s[i] in found_chars.keys():
                found_chars[s[i]] = []
            if len(found_chars[s[i]]) < t_chars[s[i]]:
                found_chars[s[i]].append(i)
                count -= 1
            else:
                j = found_chars[s[i]].pop(0)
                if len(found_chars[s[i]]) == 0:
                    del found_chars[s[i]]
                found_chars[s[i]] = [i]                
                del windows[j]
            windows[i] = s[i]
            if count == 0:
                has_solution = True
                left = next(iter(windows.keys()))
                size = i - left + 1
                if size == len(t):
                    best_from = left
                    best_to = i
                    break
                if size < (best_to - best_from  + 1):
                    best_from = left
                    best_to = i
                left_char = windows[left]
                if len(found_chars[left_char]) == 1:
                    del found_chars[left_char]
                else:
                    found_chars[left_char].pop(0)
                del windows[left]
                count += 1

    if has_solution:
        return s[best_from:best_to + 1]
    return None


def run_test():
    testcases = [
        ["ADOBECODEBANC", "ABC", "BANC"],
        ["ADOBECODEBANC", "ABBC", "BECODEBA"],
        ["ABC", "A", "A"],
        ["ABC", "AAC", None],
        ["AXXBXBXAXXAC", "AB", "BXA"],
        ["AACCBBA", "BCA", "ACCB"]
    ]

    for case in testcases:
        print('Executing test case %s - %s' % (case[0], case[1]))
        assert find_minimum_windows(case[0], case[1]) == case[2]

if __name__ == "__main__":
    run_test()
    #s = 'AACCBBA'
    #t = 'BCA'
    #print(s, len(s))
    #print(t, len(t))
    #print(find_minimum_windows(s, t))
