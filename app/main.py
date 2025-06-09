from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.universe_loader import cargar_desde_archivo
from app.solver import resolver_backtracking
from app.historial import guardar_historial
from app.historial import obtener_historial


app = FastAPI()

# Si usarás React en localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto luego
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

@app.post("/resolver/")
async def resolver_universo(file: UploadFile = File(...)):
    # Validar tipo de contenido
    if file.content_type != "application/json":
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser de tipo application/json"
        )

    try:
        data = await file.read()
        content = data.decode()
        
        # Validar JSON
        universo = cargar_desde_archivo(content)
        
        # Procesar universo
        resultado = resolver_backtracking(universo)
        guardar_historial(universo, resultado)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Universo resuelto exitosamente",
                "resultado": resultado
            }
        )
        
    except json.JSONDecodeError as e:
        logger.error(f"Error al decodificar JSON: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"El archivo contiene JSON inválido: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error al procesar el universo: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al procesar el universo: {str(e)}"
        )

@app.get("/historial/")
def ver_historial():
    return obtener_historial()



#esto es para hacer la prueba desde el back 
# if __name__ == "__main__":
#     universo = cargar_desde_archivo("data/universo.json")
#     resultado = resolver_backtracking(universo)
#     print(resultado)

# app = FastAPI()

