import json
from app.models import UniverseData

def cargar_desde_archivo(contenido_json: str) -> UniverseData:
    data = json.loads(contenido_json)
    return UniverseData(**data)
