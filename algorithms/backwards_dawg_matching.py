from algorithms.dawg import dawg

def backwards_dawg_matching(patron, texto):
    """
    Busca las ocurrencias de un patrón en un texto utilizando el algoritmo BDM
    adaptado a la implementación del DAWG de tu amigo.

    Argumentos:
        patron: La cadena de caracteres del patrón a buscar.
        texto: La cadena de caracteres en la que se buscará el patrón.

    Retorna:
        Una lista de los índices (basados en 1) donde se encuentra el patrón en el texto.
    """
    D = dawg(patron[::-1])
    m = len(patron)
    n = len(texto)
    pos = 0
    ocurrencias = []

    while pos <= n - m:
        j = m
        last = m
        estado_actual = D.initial_state

        while estado_actual is not None:
            simbolo = texto[pos + j - 1]
            next_state = estado_actual.get_next_state(simbolo)
            estado_actual = next_state
            j -= 1

            if estado_actual is not None and estado_actual.is_accepting:
                if j > 0:
                    last = j
                else:
                    ocurrencias.append(pos + 1)
                break 

        pos += last

    return ocurrencias

# Ejemplo de uso
if __name__ == "__main__":
    patron_ejemplo = "aba"
    texto_ejemplo = "ababaaba"
    resultados = buscar_patron_bdm_adaptado(patron_ejemplo, texto_ejemplo)
    print(f"Ocurrencias del patrón '{patron_ejemplo}' en '{texto_ejemplo}': {resultados}")