from random import randint


def obtener_patron(text: str, j: int) -> str:
    """
    Obtiene un patrón de texto con j caracteres repetidos.
    :param text: Texto de entrada.
    :param j: Número de caracteres a repetir.
    :return: Patrón de texto.
    """
    # verificamos que este en {6, 7, 8, 9, 10}
    if j not in {6, 7, 8, 9, 10}:
        raise ValueError("j debe estar en {6, 7, 8, 9, 10}")
    # calculamos i max
    n = len(text)
    i_max = n - 2 ** j - 1
    # obtenemos un numero aleatorio entre 0 y i_max
    i = randint(0, i_max)
    # obtenemos el patron
    patron = text[i:i + 2 ** j]
    # retornamos el patron
    return patron
