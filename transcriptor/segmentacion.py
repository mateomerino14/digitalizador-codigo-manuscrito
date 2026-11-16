import numpy as np


# Separa la imagen en lineas de texto
def segmentar_lineas(imagen):
    tinta = np.asarray(imagen.convert("L")) < 128
    por_fila = tinta.sum(axis=1)
    partes = []
    for arriba, abajo in _buscar_franjas(por_fila >= 2):
        partes = partes + _dividir(por_fila, arriba, abajo)
    lineas = []
    for arriba, abajo in _unir(partes):
        if abajo - arriba >= 10:
            columnas = np.where(tinta[arriba:abajo].any(axis=0))[0]
            lineas.append((int(columnas[0]), arriba, int(columnas[-1]) + 1, abajo))
    return lineas


def _buscar_franjas(con_tinta):
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
    # print(franjas)
    return franjas


def _dividir(por_fila, arriba, abajo):
    tramo = por_fila[arriba:abajo]
    umbral = tramo.max() * 0.10
    partes = []
    for inicio, fin in _buscar_franjas(tramo >= umbral):
        partes.append((arriba + inicio, arriba + fin))
    return partes


def _unir(partes):
    if len(partes) == 0:
        return []
    referencia = _altura_tipica(partes)
    lineas = []
    pequenas = []
    for arriba, abajo in partes:
        if abajo - arriba >= referencia * 0.3:
            lineas.append([arriba, abajo])
        else:
            pequenas.append((arriba, abajo))
    for arriba, abajo in pequenas:
        cercana = None
        menor = None
        for linea in lineas:
            distancia = _distancia(linea, arriba, abajo)
            if menor is None or distancia < menor:
                menor = distancia
                cercana = linea
        if cercana is not None and menor < referencia / 2:
            cercana[0] = min(cercana[0], arriba)
            cercana[1] = max(cercana[1], abajo)
    unidas = []
    for linea in lineas:
        unidas.append((linea[0], linea[1]))
    # print(unidas)
    return unidas


def _altura_tipica(partes):
    alturas = []
    for arriba, abajo in partes:
        alturas.append(abajo - arriba)
    mayor = max(alturas)
    altas = []
    for altura in alturas:
        if altura >= mayor * 0.3:
            altas.append(altura)
    altas.sort()
    return altas[len(altas) // 2]


def _distancia(linea, arriba, abajo):
    if abajo <= linea[0]:
        return linea[0] - abajo
    if arriba >= linea[1]:
        return arriba - linea[1]
    return 0
