# from app.models import UniverseData
# from typing import List, Tuple

# DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
# MAX_PASOS = 10000000

# def resolver_backtracking(universo: UniverseData):
#     filas = universo.matriz.filas
#     columnas = universo.matriz.columnas
#     matriz = universo.matrizInicial
#     origen = universo.origen
#     destino = universo.destino
#     energia_inicial = universo.cargaInicial

#     agujeros_negros = set(tuple(pos) for pos in universo.agujerosNegros)
#     estrellas = set(tuple(pos) for pos in universo.estrellasGigantes)
#     zonas_recarga = {(x, y): rec for x, y, rec in universo.zonasRecarga}
#     carga_requerida = {tuple(c.coordenada): c.cargaGastada for c in universo.celdasCargaRequerida}
#     gusanos = {tuple(g.entrada): tuple(g.salida) for g in universo.agujerosGusano}

#     # Destruir agujeros negros adyacentes a estrellas
#     for sx, sy in estrellas:
#         for dx, dy in DIRECCIONES:
#             nx, ny = sx + dx, sy + dy
#             agujeros_negros.discard((nx, ny))

#     visitado = [[False for _ in range(columnas)] for _ in range(filas)]
#     camino = []
#     pasos = [0]

#     exito = backtrack(origen[0], origen[1], energia_inicial, matriz, destino,
#                       agujeros_negros, zonas_recarga, carga_requerida, gusanos,
#                       visitado, camino, pasos)

#     if exito:
#         return {
#             "mensaje": "Ruta encontrada",
#             "camino": camino,
#             "energiaRestante": energia_inicial - calcular_energia_usada(camino, matriz, zonas_recarga),
#             "pasosEvaluados": pasos[0]
#         }
#     else:
#         return {
#             "mensaje": "No se encontró una ruta posible",
#             "pasosEvaluados": pasos[0]
#         }

# def backtrack(x, y, energia, matriz, destino, agujeros, zonas_recarga, carga_requerida,
#               gusanos, visitado, camino, pasos) -> bool:
#     pasos[0] += 1
#     if pasos[0] > MAX_PASOS:
#         return False

#     if not posicion_valida(x, y, matriz, agujeros, visitado, energia, carga_requerida):
#         return False

#     energia -= matriz[x][y]
#     if energia < 0:
#         return False

#     if (x, y) in zonas_recarga:
#         energia += zonas_recarga[(x, y)]

#     camino.append((x, y))

#     if (x, y) == tuple(destino):
#         return True

#     visitado[x][y] = True

#     if (x, y) in gusanos:
#         sx, sy = gusanos[(x, y)]
#         if not visitado[sx][sy]:
#             if backtrack(sx, sy, energia, matriz, destino, agujeros, zonas_recarga,
#                          carga_requerida, gusanos, visitado, camino, pasos):
#                 return True

#     for dx, dy in DIRECCIONES:
#         nx, ny = x + dx, y + dy
#         if backtrack(nx, ny, energia, matriz, destino, agujeros, zonas_recarga,
#                      carga_requerida, gusanos, visitado, camino, pasos):
#             return True

#     camino.pop()
#     visitado[x][y] = False
#     return False

# def posicion_valida(x, y, matriz, agujeros, visitado, energia, carga_requerida) -> bool:
#     filas = len(matriz)
#     columnas = len(matriz[0])

#     if x < 0 or x >= filas or y < 0 or y >= columnas:
#         return False
#     if (x, y) in agujeros:
#         return False
#     if visitado[x][y]:
#         return False
#     if energia < matriz[x][y]:
#         return False
#     if (x, y) in carga_requerida and energia < carga_requerida[(x, y)]:
#         return False
#     return True

# def calcular_energia_usada(camino: List[Tuple[int, int]], matriz: List[List[int]], zonas_recarga: dict) -> int:
#     energia = 0
#     for x, y in camino:
#         energia += matriz[x][y]
#         if (x, y) in zonas_recarga:
#             energia -= zonas_recarga[(x, y)]
#     return energia

from app.models import UniverseData
from typing import List, Tuple
import heapq

DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def resolver_backtracking(universo: UniverseData):
    filas = universo.matriz.filas
    columnas = universo.matriz.columnas
    matriz = universo.matrizInicial
    origen = tuple(universo.origen)
    destino = tuple(universo.destino)
    energia_inicial = universo.cargaInicial

    agujeros_negros = set(tuple(pos) for pos in universo.agujerosNegros)
    estrellas = set(tuple(pos) for pos in universo.estrellasGigantes)
    zonas_recarga = {(x, y): rec for x, y, rec in universo.zonasRecarga}
    carga_requerida = {tuple(c.coordenada): c.cargaGastada for c in universo.celdasCargaRequerida}
    gusanos = {tuple(g.entrada): tuple(g.salida) for g in universo.agujerosGusano}

    # Las estrellas destruyen agujeros negros adyacentes
    for sx, sy in estrellas:
        for dx, dy in DIRECCIONES:
            nx, ny = sx + dx, sy + dy
            agujeros_negros.discard((nx, ny))

    # Heap para A*: (costo total estimado, costo real, (x, y), energia, camino)
    def heuristica(x, y):
        return abs(x - destino[0]) + abs(y - destino[1])

    heap = []
    heapq.heappush(heap, (heuristica(*origen), 0, origen, energia_inicial, []))
    visitado = dict()  # (x, y) -> max energía alcanzada

    while heap:
        estimado, costo_real, (x, y), energia_restante, camino = heapq.heappop(heap)

        if energia_restante < 0:
            continue
        if (x, y) == destino:
            return {
                "mensaje": "Ruta encontrada",
                "camino": camino + [(x, y)],
                "energiaRestante": energia_restante,
                "pasosEvaluados": len(visitado)
            }

        if (x, y) in visitado and visitado[(x, y)] >= energia_restante:
            continue

        visitado[(x, y)] = energia_restante
        nuevo_camino = camino + [(x, y)]

        # Si es agujero de gusano
        if (x, y) in gusanos:
            salida = gusanos[(x, y)]
            heapq.heappush(heap, (
                costo_real + heuristica(*salida),
                costo_real,
                salida,
                energia_restante,
                nuevo_camino
            ))

        # Movimientos normales
        for dx, dy in DIRECCIONES:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < filas and 0 <= ny < columnas):
                continue
            if (nx, ny) in agujeros_negros:
                continue

            costo_celda = matriz[nx][ny]
            if energia_restante < costo_celda:
                continue
            if (nx, ny) in carga_requerida and energia_restante < carga_requerida[(nx, ny)]:
                continue

            energia_nueva = energia_restante - costo_celda
            if (nx, ny) in zonas_recarga:
                energia_nueva += zonas_recarga[(nx, ny)]

            heapq.heappush(heap, (
                costo_real + costo_celda + heuristica(nx, ny),
                costo_real + costo_celda,
                (nx, ny),
                energia_nueva,
                nuevo_camino
            ))

    return {
        "mensaje": "No se encontró una ruta posible",
        "pasosEvaluados": len(visitado)
    }
