from fastapi import FastAPI
from typing import Union

app = FastAPI()


@app.get("/")
async def test_rob():
    return {"Hola": "caracola"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# Iniciar servidor uvicorn "nombre_fichero":"nombre_variable_instanciada" --reload
# En este ejemplo:  uvicorn main:app --reload

# Detener el server uvicorn CTRL+C

# FastAPI genera documentación de forma automática:
    # Documentación Swagger: http://127.0.0.1:8000/docs
    # Documentación Redocly: http://127.0.0.1:8000/redoc