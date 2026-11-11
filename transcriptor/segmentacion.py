import numpy as np
from PIL import Image

#Separa la imagen en lineas de texto
def segmentar_lineas(imagen: Image.Image):
    tinta = np.asarray(imagen.convert("L")) < 128
    franjas = _franjas(tinta.sum(axis=1) >= 2)
    lineas = []
    for arriba, abajo in _unir(franjas):
        if abajo - arriba >= 10:
            columnas = np.where(tinta[arriba:abajo].any(axis=0))[0]
            lineas.append((int(columnas[0]), arriba, int(columnas[-1]) + 1, abajo))
    return lineas


def _franjas(con_tinta):
    franjas = []
    inicio = None
    for y, hay in enumerate(con_tinta):
        if hay and inicio is None:
            inicio = y
        elif not hay and inicio is not None:
            franjas.append((inicio, y))
            inicio = None
    if inicio is not None:
        franjas.append((inicio, len(con_tinta)))
    #print(franjas)
    return franjas


def _unir(franjas):
    unidas = []
    for arriba, abajo in franjas:
        if unidas and arriba - unidas[-1][1] < 15:
            unidas[-1] = (unidas[-1][0], abajo)
        else:
            unidas.append((arriba, abajo))
    #print(unidas)
    return unidas