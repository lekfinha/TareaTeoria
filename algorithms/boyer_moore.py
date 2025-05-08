"""

"""


def bad_character_table(pattern):
    """Creates the bad character table."""
    table = {}
    for i in range(len(pattern)):
        table[pattern[i]] = i
    return table

def boyer_moore(text, pattern) -> list[int]:
    """
    Searches for occurrences of 'pattern' in 'text' using the Boyer-Moore algorithm.

    Example of usage:
    text = "abacaabadcabacabaabb"
    pattern = "abacab"
    result = boyer_moore(text, pattern)
    print("Pattern found at positions:", result)
    """
    if len(pattern) == 0:
        return []

    bad_char = bad_character_table(pattern)
    matches = []
    m = len(pattern)
    n = len(text)
    s = 0  # shift of the pattern with respect to text

    while s <= n - m:
        j = m - 1

        # Keep reducing index j while characters of pattern and text are matching
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            matches.append(s)
            s += m - bad_char.get(text[s + m], -1) if s + m < n else 1
        else:
            s += max(1, j - bad_char.get(text[s + j], -1))

    return matches