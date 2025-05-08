def crear_patron(j: int, alphabet: list[str]) -> str:
    """
    Crea un patrón de texto con j caracteres repetidos.
    :param j: Número de caracteres a repetir.
    :param alphabet: Alfabeto a utilizar.
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

