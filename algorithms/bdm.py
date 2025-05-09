from algorithms.dawg import dawg

def BDM_search(dawg, text):
    """
    Implementación del algoritmo Backwards DAWG Matching (BDM).
    
    Argumentos:
        dawg (DAWG): Autómata de sufijos del patrón invertido (DAWG).
        text (str): Texto donde buscar.
    
    Retorna:
        lista: Posiciones donde se encuentra el patrón.
    """
    pattern_length = len(pattern)
    n = len(text)
    pos = 0
    occurrences = []

    while pos <= n - pattern_length:
        j = pattern_length
        last = pattern_length
        current_state = dawg.q0  

        while current_state is not None and j > 0:
            char = text[pos + j - 1]
            current_state = dawg.delta(current_state, char)

            if current_state is not None:
                j -= 1
                if current_state in dawg.F:  
                    if j > 0:
                        last = j  
                    else:
                        occurrences.append(pos)

        pos += last  

    return occurrences


# Ejemplo de uso
if __name__ == "__main__":
    text = "AACTGCCCTG"
    pattern = "CTG"
    print(BDM_search(pattern, text))
