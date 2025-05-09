from DAWG_Gemini import *



def buscar_patron(patron, texto):
    """
    Busca las ocurrencias de un patrón en un texto utilizando una estructura DAWG.

    Args:
        patron: La cadena de caracteres del patrón a buscar.
        texto: La cadena de caracteres en la que se buscará el patrón.

    Returns:
        Una lista de los índices (basados en 1) donde se encuentra el patrón en el texto.
    """
    D = DAWG(patron[::-1])  # Construir el DAWG con el patrón invertido
    m = len(patron)
    n = len(texto)
    pos = 0
    ocurrencias = []

    while pos <= n-m:
        j = m
        last = m
        estado = D.q0

        while estado is not None:  # Asumimos que None representa el estado⊥
            estado = D.delta(estado, texto[pos + j - 1]) # Accedemos al texto con el índice correcto
            j -= 1
            if estado in D.F:  # Revisar si el estado es de aceptación en tiempo O(1)
                if j > 0:
                    last = j
                else:
                    ocurrencias.append(pos + 1)
                break  # Salimos del bucle interno al encontrar una posible coincidencia
        pos += last

    return ocurrencias

# Ejemplo de uso (asumiendo que DAWG está implementado)
if __name__ == "__main__":
    # Necesitarías una implementación real de la clase DAWG para que esto funcione completamente.
    # Aquí solo mostramos cómo se llamaría a la función.
    class MockDAWG:
        def __init__(self, inverted_pattern):
            self.inverted_pattern = inverted_pattern
            self.q0 = "estado_inicial"
            self.F = {"estado_aceptacion"} # Un conjunto de estados de aceptación

        def delta(self, estado_actual, simbolo):
            # Simulación muy básica de la función de transición
            if estado_actual == "estado_inicial" and simbolo == self.inverted_pattern[len(self.inverted_pattern) - 1]:
                return "estado_aceptacion"
            return None

    def mock_DAWG(inverted_pattern):
        return MockDAWG(inverted_pattern)

    DAWG = mock_DAWG # Asignamos nuestra "implementación" mock

    patron_ejemplo = "aba"
    texto_ejemplo = "ababaaba"
    resultados = buscar_patron(patron_ejemplo, texto_ejemplo)
    print(f"Ocurrencias del patrón '{patron_ejemplo}' en '{texto_ejemplo}': {resultados}")
