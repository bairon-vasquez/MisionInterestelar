import json
import os
from datetime import datetime

HISTORIAL_PATH = "data/historial.json"

def guardar_historial(universo, resultado):
    historial = []

    if os.path.exists(HISTORIAL_PATH):
        with open(HISTORIAL_PATH, "r") as f:
            try:
                historial = json.load(f)
            except json.JSONDecodeError:
                historial = []

    nuevo_registro = {
        "origen": universo.origen,
        "destino": universo.destino,
        "rutaEncontrada": resultado.get("camino") is not None,
        "pasosEvaluados": resultado.get("pasosEvaluados"),
        "energiaRestante": resultado.get("energiaRestante", None),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    historial.append(nuevo_registro)

    with open(HISTORIAL_PATH, "w") as f:
        json.dump(historial, f, indent=2)


def obtener_historial():
    if os.path.exists(HISTORIAL_PATH):
        with open(HISTORIAL_PATH, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []
