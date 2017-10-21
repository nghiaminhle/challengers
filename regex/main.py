
def regex_matcher(s, pattern):
    return match(s, '', 0, pattern)


def match(s, prefix_str, p_index, pattern):
    if s == prefix_str and p_index == len(pattern):
        return True
    if p_index == len(pattern):
        return False
    if pattern[p_index] == '.':
        if s == prefix_str:
            return False
        return match(s, prefix_str + s[len(prefix_str)], p_index + 1, pattern)
    elif pattern[p_index] == '*':
        while p_index < len(pattern)-1 and pattern[p_index+1] == '*':
            p_index +=1
        if s == prefix_str:
            return match(s, prefix_str, p_index + 1, pattern)
        elif match(s, prefix_str, p_index + 1, pattern):
            return True
        new_prefix = prefix_str
        s_index = len(prefix_str)
        while s_index < len(s):
            new_prefix = new_prefix + s[s_index]
            if match(s, new_prefix, p_index, pattern) or match(s, new_prefix, p_index + 1, pattern):
                return True
            s_index += 1
        return match(s, new_prefix, p_index + 1, pattern)
    else:
        if s == prefix_str or s[len(prefix_str)] != pattern[p_index]:
            return False
        return match(s, prefix_str + s[len(prefix_str)], p_index + 1, pattern)


def simple_test():
    testcases = [
        ['a', 'a', True],
        ['a', 'b', False],
        ['c', '.', True],
        ['df', '*', True],
        ['abcd', 'a.c', False],
        ['abcabfxyza', '*ab*klm', False],
        ['abcabf', '*abf', True],
        ['abccccc', '*ccc', True],
        ['abc', 'c*', False],
        ['abc', '*d', False],
        ['abcd', 'a*d', True],
        ['abcd', 'a***d', True],
        ['abcd', '*', True],
        ['', '*', True],
        ['abc', '*c*', True],
        ['bedc', '*b*c', True],
        ['abcd', 'a.c*', True],
        ['abcd', 'a.c*.', True],
        ['', '*.', False]
    ]

    for case in testcases:
        print('Executing test case %s %s %s' % (case[0], case[1], case[2]))
        assert regex_matcher(case[0], case[1]) == case[2]

    #print(regex_matcher('abcd', 'a***d'))

def test_per():
    s= 'abcd'
    pattern = 'a'
    for i in range(99):
        pattern +='*'
    pattern += 'f'
    print(regex_matcher('abcd', pattern))

if __name__ == "__main__":
    #simple_test()
    test_per()
