def distancia(a, b):
    anterior = list(range(len(b) + 1))
    for i, x in enumerate(a, start=1):
        actual = [i]
        for j, y in enumerate(b, start=1):
            costo = 0 if x == y else 1
            actual.append(min(anterior[j] + 1, actual[j - 1] + 1, anterior[j - 1] + costo,))
        anterior = actual
    return anterior[-1]


def cer(referencia, reconocido):
    if not referencia:
        raise ValueError("la referencia esta vacia")
    return distancia(referencia, reconocido) / len(referencia)


def wer(referencia, reconocido):
    palabras = referencia.split()
    if not palabras:
        raise ValueError("la referencia esta vacia")
    return distancia(palabras, reconocido.split()) / len(palabras)