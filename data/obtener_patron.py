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
    # calculamos el largo del patron
    m = 2**j
    # creamos el patron
    patron = ""
    for i in range(m):
        # elegimos un character aleatorio del alfabeto
        patron += alphabet[i % len(alphabet)]
    # retornamos el patron
    return patron