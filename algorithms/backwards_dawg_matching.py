from algorithms.dawg import dawg

# el return revisar, ya que a priori no devuelve nada
def backwards_dawg_matching(text: str, pattern: str) -> list[int]:
    """
    Searches for occurrences of 'pattern' in 'text' using the backwards DAWG matching algorithm.

    Example of usage:
    text = "abxabcabcaby"
    pattern = "abcaby"
    result = backwards_dawg_matching(text, pattern)
    print("Pattern found at positions:", result)
    """
    # preprocesamiento
    d = dawg(pattern)
    # buscamos el patron
    i = 0

    ...
