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

@app.post("/resolver/")
async def resolver_universo(file: UploadFile = File(...)):
    data = await file.read()
    universo = cargar_desde_archivo(data.decode())
    resultado = resolver_backtracking(universo)
    guardar_historial(universo, resultado)
    return resultado

@app.get("/historial/")
def ver_historial():
    return obtener_historial()



#esto es para hacer la prueba desde el back 
# if __name__ == "__main__":
#     universo = cargar_desde_archivo("data/universo.json")
#     resultado = resolver_backtracking(universo)
#     print(resultado)

# app = FastAPI()

