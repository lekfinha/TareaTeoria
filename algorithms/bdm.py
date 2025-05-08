from .dawg import dawg

def BDM_search(dawg, text, pattern_length):
    """
    Implementación del algoritmo Backwards DAWG Matching (BDM).
    
    Argumentos:
        dawg (DAWG): Autómata de sufijos del patrón invertido (DAWG).
        text (str): Texto donde buscar.
        pattern_length (int): Longitud del patrón original (m).
    
    Retorna:
        lista: Posiciones donde se encuentra el patrón.
    """
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


# testing
if __name__ == "__main__":
    from automata.afd import construir_DAWG

    pattern = "ACTG"
    reversed_pattern = pattern[::-1] 
    dawg = construir_DAWG(reversed_pattern)  

    text = "XXACTGYYACTGZZ"
    occurrences = BDM_search(dawg, text, len(pattern))
    print(f"Patrón encontrado en posiciones: {occurrences}")