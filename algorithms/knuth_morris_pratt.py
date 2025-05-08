def compute_lps(pattern):
    """Construye la tabla de los prefijos más largos que también son sufijos (LPS)."""
    lps = [0] * len(pattern)
    length = 0  # longitud del prefijo más largo que también es sufijo
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(text, pattern):
    """
    Busca todas las apariciones del patrón en el texto usando el algoritmo KMP.

    Example of usage:

    text = "abxabcabcaby"
    pattern = "abcaby"
    result = kmp_search(text, pattern)
    print("Patrón encontrado en las posiciones:", result)
    """
    if not pattern:
        return []

    lps = compute_lps(pattern)
    matches = []

    i = j = 0  # i para el texto, j para el patrón

    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == len(pattern):
            matches.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches