# Take a string as input and extract all digits in the string, delimited by any non-digit characters.
# It should then sum those digits in the order they were provided and display the result.


class Solution(object):
    def sum_digit(self, s):
        res = []
        temp = []

        def maybe_add_num():
            if temp and temp[-1] != '-':
                res.append(int(''.join(temp)))
            temp.clear()

        for ch in s:
            if ch.isdigit():
                temp.append(ch)
            elif ch == '-':
                maybe_add_num()
                temp.append(ch)
            else:
                maybe_add_num()

        maybe_add_num()

        if len(res) == 0:
            return ''
        return sum(res)
