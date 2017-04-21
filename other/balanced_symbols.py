# Проверяет, не пропущен ли парный символ.
# Работает за один проход.


"""
>>> is_balanced("[]asdasdd()aqwe<asd")
False

>>> is_balanced("[]asdasdd()aqwe<asd>")
True
"""

def is_balanced(text, brackets = "()[]{}<>"):
    """
    >>> is_balanced("[]asdasdd()aqwe<asd>")
    True
    """

    counts = {}
    left_for_right = {}

    for left, right in zip(brackets[::2], brackets[1::2]):
        assert left != right, "The brackets must be differ"
        counts[left] = 0
        left_for_right[right] = left

    for c in text:
        if c in counts:
            counts[c] += 1
        elif c in left_for_right:
            left = left_for_right[c]
            if counts[left] == 0:
                return False
            counts[left] -= 1

    return not any(counts.values())


if __name__ == "__main__":
    import doctest
    doctest.testmod()
