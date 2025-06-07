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

    # 🧨 Estrellas destruyen agujeros negros adyacentes
    agujeros_destruidos = set()
    estrellas_utilizadas = []
    for sx, sy in estrellas:
        destruidos = []
        for dx, dy in DIRECCIONES:
            nx, ny = sx + dx, sy + dy
            if (nx, ny) in agujeros_negros:
                agujeros_negros.discard((nx, ny))
                destruidos.append((nx, ny))
        if destruidos:
            estrellas_utilizadas.append((sx, sy))
            agujeros_destruidos.update(destruidos)

    def heuristica(x, y):
        return abs(x - destino[0]) + abs(y - destino[1])

    heap = []
    heapq.heappush(heap, (heuristica(*origen), 0, origen, energia_inicial, []))
    visitado = dict()  # (x, y) -> energía máxima

    while heap:
        estimado, costo_real, (x, y), energia_restante, camino = heapq.heappop(heap)

        if energia_restante < 0:
            continue
        if (x, y) == destino:
            camino_final = camino + [(x, y)]

            # 🌀 Detectar agujeros de gusano usados
            agujeros_gusano_usados = []
            for i in range(len(camino_final) - 1):
                actual = camino_final[i]
                siguiente = camino_final[i + 1]
                if actual in gusanos and gusanos[actual] == siguiente:
                    agujeros_gusano_usados.append({
                        "entrada": list(actual),
                        "salida": list(siguiente)
                    })

            return {
                "mensaje": "Ruta encontrada",
                "camino": camino_final,
                "energiaRestante": energia_restante,
                "pasosEvaluados": len(visitado),
                "agujerosNegrosDestruidos": list(agujeros_destruidos),
                "estrellasUtilizadas": [list(e) for e in estrellas_utilizadas],
                "agujerosGusanoUsados": agujeros_gusano_usados
            }

        if (x, y) in visitado and visitado[(x, y)] >= energia_restante:
            continue
        visitado[(x, y)] = energia_restante

        nuevo_camino = camino + [(x, y)]

        # 🚀 Agujero de gusano
        if (x, y) in gusanos:
            salida = gusanos[(x, y)]
            heapq.heappush(heap, (
                costo_real + heuristica(*salida),
                costo_real,
                salida,
                energia_restante,
                nuevo_camino
            ))

        # 👣 Movimientos normales
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
