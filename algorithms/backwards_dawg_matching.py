from algorithms.dawg import dawg

def backwards_dawg_matching(pattern: str, text: str) -> list[int]:
    """
    Implementación del algoritmo BDM para encontrar todas las ocurrencias
    de 'pattern' en 'text'.
    Las ocurrencias se reportan con índice base 1.
    """
    m = len(pattern)
    n = len(text)
    occurrences = []

    if m == 0: # El patrón es vacío
        return list(range(1, n + 2))
    if m > n: # El patrón es más largo que el texto
        return []

    # --- Preprocesamiento --- #
    pr = pattern[::-1]
    dawg_pr = dawg(pr) # Construcción del DAWG para el patrón invertido

    # --- Búsqueda ---
    pos = 0 # indice base 0 para la posición de inicio de la ventana en el texto
    while pos <= n - m:
        j = m
        last = m # Valor de desplazamiento por defecto

        current_dawg_state_idx = dawg_pr.initial_state.name # estado <- D.q0
        while True:
            # Si current_dawg_state_idx es None, la transición anterior falló.
            if current_dawg_state_idx is None:
                break

            if j == 0:
                break

            char_from_text = text[pos + j - 1]
            # estado <- D.delta(estado, t_pos+j)
            current_dawg_state_idx = dawg_pr.get_transition_idx(current_dawg_state_idx, char_from_text)

            # j <- j-1
            j -= 1

            if current_dawg_state_idx is None:
                break

                # Si estado ∈ D.F entonces:
            if dawg_pr.is_accepting_state(current_dawg_state_idx):
                if j > 0: # Si j > 0 entonces last <- j
                    last = j
                else:
                    occurrences.append(pos + 1)
            if j == 0 and current_dawg_state_idx is not None:
                break

        pos += last

    return occurrences