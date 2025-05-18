import sys
sys.setrecursionlimit(10000)


def hay_camino_simple(x, y, destino, matriz, agujeros, visitado):
    filas, columnas = len(matriz), len(matriz[0])
    if x < 0 or x >= filas or y < 0 or y >= columnas:
        return False
    if (x, y) in agujeros or visitado[x][y]:
        return False
    if (x, y) == destino:
        return True

    visitado[x][y] = True

    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        if hay_camino_simple(x+dx, y+dy, destino, matriz, agujeros, visitado):
            return True

    return False

# Desde tu universo.json
import json
with open("data/universo.json") as f:
    data = json.load(f)

matriz = data["matrizInicial"]
filas = data["matriz"]["filas"]
columnas = data["matriz"]["columnas"]
origen = tuple(data["origen"])
destino = tuple(data["destino"])
agujeros = set(tuple(pos) for pos in data["agujerosNegros"])
visitado = [[False]*columnas for _ in range(filas)]

if hay_camino_simple(origen[0], origen[1], destino, matriz, agujeros, visitado):
    print("✅ Hay un camino posible (sin considerar energía)")
else:
    print("❌ No hay camino posible")
