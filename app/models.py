from pydantic import BaseModel
from typing import List, Tuple, Dict

class Gusano(BaseModel):
    entrada: Tuple[int, int]
    salida: Tuple[int, int]

class Portal(BaseModel):
    desde: Tuple[int, int]
    hasta: Tuple[int, int]

class CargaRequerida(BaseModel):
    coordenada: Tuple[int, int]
    cargaGastada: int

class Matriz(BaseModel):
    filas: int
    columnas: int

class UniverseData(BaseModel):
    matriz: Matriz
    origen: Tuple[int, int]
    destino: Tuple[int, int]
    agujerosNegros: List[Tuple[int, int]]
    estrellasGigantes: List[Tuple[int, int]]
    agujerosGusano: List[Gusano]
    zonasRecarga: List[Tuple[int, int, int]]
    celdasCargaRequerida: List[CargaRequerida]
    cargaInicial: int
    matrizInicial: List[List[int]]
