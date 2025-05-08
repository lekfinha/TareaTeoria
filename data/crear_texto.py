def crear_texto(alphabet: list[str], n: int = 2**20) -> str:
    """
    Crea un texto aleatorio de longitud n utilizando el alfabeto dado.
    :param alphabet: Alfabeto a utilizar.
    :param n: Longitud del texto a crear.
    :return: Texto aleatorio.
    """
    # verificamos que n sea positivo
    if n <= 0:
        raise ValueError("n debe ser positivo")
    # creamos el texto
    texto = ""
    for i in range(n):
        # elegimos un character aleatorio del alfabeto
        texto += alphabet[i % len(alphabet)]
    # retornamos el texto
    return texto
