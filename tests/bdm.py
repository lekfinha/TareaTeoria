# test for bdb function
from algorithms.backwards_dawg_matching import backwards_dawg_matching


def test_backwards_dawg_matching():
    """
    Test the backwards_dawg_matching function.
    """
    # Test case 1: Basic test
    text = "abxabcabcaby"
    pattern = "abcaby"
    result = backwards_dawg_matching(text, pattern)
    assert result == [6], f"Expected [6], but got {result}"

    # Test case 2: Pattern not found
    text = "abcdefgh"
    pattern = "xyz"
    result = backwards_dawg_matching(text, pattern)
    assert result == [], f"Expected [], but got {result}"

    # Test case 3: Empty text
    text = ""
    pattern = "abc"
    result = backwards_dawg_matching(text, pattern)
    assert result == [], f"Expected [], but got {result}"

    # Test case 4: Empty pattern
    text = "abcdefgh"
    pattern = ""
    result = backwards_dawg_matching(text, pattern)
    assert result == [], f"Expected [], but got {result}"