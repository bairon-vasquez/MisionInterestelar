from app.models import UniverseData
from typing import List, Tuple, Dict
import copy
import heapq

DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
MAX_SOLUCIONES = 3
MAX_PASOS = 2000000000

def resolver(universo: UniverseData):
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

## este es para diferentes rutas 

def resolver_varias_rutas(universo: UniverseData):
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

    # ⭐ Destruir agujeros con estrellas
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

    soluciones = []
    heap = []
    heapq.heappush(heap, (heuristica(*origen), 0, origen, energia_inicial, []))
    visitado = {}

    while heap and len(soluciones) < MAX_SOLUCIONES:
        estimado, costo_real, (x, y), energia_restante, camino = heapq.heappop(heap)

        if energia_restante < 0:
            continue

        camino_actual = camino + [(x, y)]

        if (x, y) == destino:
            # Detectar agujeros de gusano usados
            gusanos_usados = []
            for i in range(len(camino_actual) - 1):
                actual = camino_actual[i]
                siguiente = camino_actual[i + 1]
                if actual in gusanos and gusanos[actual] == siguiente:
                    gusanos_usados.append({
                        "entrada": list(actual),
                        "salida": list(siguiente)
                    })

            soluciones.append({
                "camino": camino_actual,
                "energiaRestante": energia_restante,
                "pasosEvaluados": len(visitado),
                "agujerosNegrosDestruidos": list(agujeros_destruidos),
                "estrellasUtilizadas": [list(e) for e in estrellas_utilizadas],
                "agujerosGusanoUsados": gusanos_usados
            })
            continue

        # Evitar volver a visitar un estado peor o igual
        if (x, y) in visitado and visitado[(x, y)] >= energia_restante:
            continue
        visitado[(x, y)] = energia_restante

        # 💫 Agujero de gusano
        if (x, y) in gusanos:
            salida = gusanos[(x, y)]
            heapq.heappush(heap, (
                costo_real + heuristica(*salida),
                costo_real,
                salida,
                energia_restante,
                camino_actual
            ))

        # 🚶 Movimientos normales
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

            nueva_energia = energia_restante - costo_celda
            if (nx, ny) in zonas_recarga:
                nueva_energia += zonas_recarga[(nx, ny)]

            heapq.heappush(heap, (
                costo_real + costo_celda + heuristica(nx, ny),
                costo_real + costo_celda,
                (nx, ny),
                nueva_energia,
                camino_actual
            ))

    if soluciones:
        return {
            "mensaje": f"Se encontraron {len(soluciones)} rutas posibles",
            "soluciones": soluciones
        }
    else:
        return {
            "mensaje": "No se encontró una ruta posible",
            "pasosEvaluados": len(visitado)
        }


def resolver_backtracking_recursivo(universo: UniverseData):
    import copy

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

    # ⭐ Destruir agujeros con estrellas
    agujeros_destruidos = set()
    estrellas_utilizadas = []
    for sx, sy in estrellas:
        destruidos = []
        for dx, dy in DIRECCIONES:
            nx, ny = sx + dx, sy + dy
            if (nx, ny) in agujeros_negros:
                agujeros_negros.remove((nx, ny))
                destruidos.append((nx, ny))
        if destruidos:
            estrellas_utilizadas.append((sx, sy))
            agujeros_destruidos.update(destruidos)

    soluciones = []
    pasos = [0]
    encontrado = [False]

    visitado_energia = [[-1] * columnas for _ in range(filas)]

    def manhattan(x, y):
        return abs(x - destino[0]) + abs(y - destino[1])

    def backtrack(x, y, energia, camino, gusanos_usados):
        if pasos[0] > MAX_PASOS or encontrado[0]:
            return

        if not (0 <= x < filas and 0 <= y < columnas):
            return
        if (x, y) in agujeros_negros:
            return
        if energia <= visitado_energia[x][y]:
            return

        pasos[0] += 1
        visitado_energia[x][y] = energia

        costo = matriz[x][y]
        if energia < costo:
            return
        if (x, y) in carga_requerida and energia < carga_requerida[(x, y)]:
            return

        energia -= costo
        if (x, y) in zonas_recarga:
            energia += zonas_recarga[(x, y)]

        camino.append((x, y))

        if (x, y) == destino:
            soluciones.append({
                "camino": list(camino),
                "energiaRestante": energia,
                "pasosEvaluados": pasos[0],
                "agujerosNegrosDestruidos": list(agujeros_destruidos),
                "estrellasUtilizadas": [list(e) for e in estrellas_utilizadas],
                "agujerosGusanoUsados": gusanos_usados.copy()
            })
            encontrado[0] = True
            camino.pop()
            return

        # Gusano
        if (x, y) in gusanos:
            ex, ey = gusanos[(x, y)]
            gusanos_usados.append({"entrada": [x, y], "salida": [ex, ey]})
            backtrack(ex, ey, energia, camino, gusanos_usados)
            gusanos_usados.pop()

        # Ordenar direcciones por cercanía al destino
        direcciones_ordenadas = sorted(DIRECCIONES, key=lambda d: manhattan(x + d[0], y + d[1]))
        for dx, dy in direcciones_ordenadas:
            nx, ny = x + dx, y + dy
            backtrack(nx, ny, energia, camino, gusanos_usados)

        camino.pop()

    backtrack(origen[0], origen[1], energia_inicial, [], [])

    if soluciones:
        return {
            "mensaje": "Ruta encontrada con backtracking optimizado",
            "solucion": soluciones[0]
        }
    else:
        return {
            "mensaje": "No se encontró una ruta posible",
            "pasosEvaluados": pasos[0]
        }
    
def resolver_backtracking_varias_rutas(universo: UniverseData):
    import copy

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

    # ⭐ Destruir agujeros con estrellas
    agujeros_destruidos = set()
    estrellas_utilizadas = []
    for sx, sy in estrellas:
        destruidos = []
        for dx, dy in DIRECCIONES:
            nx, ny = sx + dx, sy + dy
            if (nx, ny) in agujeros_negros:
                agujeros_negros.remove((nx, ny))
                destruidos.append((nx, ny))
        if destruidos:
            estrellas_utilizadas.append((sx, sy))
            agujeros_destruidos.update(destruidos)

    soluciones = []
    pasos = [0]
    visitado_energia = [[-1] * columnas for _ in range(filas)]

    def manhattan(x, y):
        return abs(x - destino[0]) + abs(y - destino[1])

    def backtrack(x, y, energia, camino, gusanos_usados):
        if pasos[0] > MAX_PASOS or len(soluciones) >= MAX_SOLUCIONES:
            return

        if not (0 <= x < filas and 0 <= y < columnas):
            return
        if (x, y) in agujeros_negros:
            return
        if energia <= visitado_energia[x][y]:
            return

        pasos[0] += 1
        visitado_energia[x][y] = energia

        costo = matriz[x][y]
        if energia < costo:
            return
        if (x, y) in carga_requerida and energia < carga_requerida[(x, y)]:
            return

        energia -= costo
        if (x, y) in zonas_recarga:
            energia += zonas_recarga[(x, y)]

        camino.append((x, y))

        if (x, y) == destino:
            soluciones.append({
                "camino": list(camino),
                "energiaRestante": energia,
                "pasosEvaluados": pasos[0],
                "agujerosNegrosDestruidos": list(agujeros_destruidos),
                "estrellasUtilizadas": [list(e) for e in estrellas_utilizadas],
                "agujerosGusanoUsados": copy.deepcopy(gusanos_usados)
            })
            camino.pop()
            return

        # Gusano
        if (x, y) in gusanos:
            ex, ey = gusanos[(x, y)]
            gusanos_usados.append({"entrada": [x, y], "salida": [ex, ey]})
            backtrack(ex, ey, energia, camino, gusanos_usados)
            gusanos_usados.pop()

        # Direcciones ordenadas hacia el destino
        for dx, dy in sorted(DIRECCIONES, key=lambda d: manhattan(x + d[0], y + d[1])):
            backtrack(x + dx, y + dy, energia, camino, gusanos_usados)

        camino.pop()

    backtrack(origen[0], origen[1], energia_inicial, [], [])

    if soluciones:
        return {
            "mensaje": f"Se encontraron {len(soluciones)} rutas con backtracking",
            "soluciones": soluciones
        }
    else:
        return {
            "mensaje": "No se encontró una ruta posible",
            "pasosEvaluados": pasos[0]
        }
