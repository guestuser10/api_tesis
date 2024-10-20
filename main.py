from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ctypes
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# Definir modelo de entrada
class TopsisInput(BaseModel):
    attributes: list[str]
    candidates: list[str]
    raw_data: list[list[float]]
    weights: list[float]
    benefit_attributes: list[int]

# Función para convertir JSON a cadenas formateadas
def json_to_formatted_strings(data):
    attributes = data["attributes"]
    candidates = data["candidates"]
    raw_data = data["raw_data"]
    weights = data["weights"]
    benefit_attributes = data["benefit_attributes"]

    attributes_str = ','.join(attributes).encode('utf-8')
    candidates_str = ','.join(candidates).encode('utf-8')
    weights_str = ','.join(map(str, weights)).encode('utf-8')
    benefit_attributes_str = ','.join(map(str, benefit_attributes)).encode('utf-8')
    raw_data_str = ';'.join([','.join(map(str, row)) for row in raw_data]).encode('utf-8')

    return attributes_str, candidates_str, weights_str, benefit_attributes_str, raw_data_str

# Ruta de la librería .so
dll_path = os.path.abspath("./topsislib.so")
dll = ctypes.CDLL(dll_path)

#argumento y retorno de la función procesarDatos
dll.procesarDatos.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_char_p
]
dll.procesarDatos.restype = ctypes.c_char_p

@app.post("/topsis")
async def run_topsis(data: TopsisInput):
    # Convertir JSON a cadenas formateadas
    attributes_str, candidates_str, weights_str, benefit_attributes_str, raw_data_str = json_to_formatted_strings(data.dict())

    # Llamar a la función de la biblioteca .so
    result = dll.procesarDatos(attributes_str, candidates_str, weights_str, benefit_attributes_str, raw_data_str)

    # Convertir el resultado a una cadena de texto
    result_str = result.decode('utf-8')

    # Devolver el resultado como JSON
    return {"result": result_str}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
