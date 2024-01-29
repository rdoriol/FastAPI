from fastapi import FastAPI
from typing import Union

from routers import products, users, jwt_auth_users
from fastapi.staticfiles import StaticFiles     # para recursos estáticos

app = FastAPI()

# Routers
app.include_router(products.router_products)
app.include_router(users.router_user)
app.include_router(jwt_auth_users.router_jwt)

app.mount("/static", StaticFiles(directory="static"), name="mi_imagen_estática")

@app.get("/")
async def test_rob():
    return {"main": "enrutador"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# Iniciar servidor uvicorn "nombre_fichero":"nombre_variable_instanciada_clase_FastAPI" --reload
# En este ejemplo:  uvicorn main:app --reload

# Detener el server uvicorn CTRL+C


# todo      -------------------------------------------------
# todo      FastAPI genera documentación de forma automática
# todo      -------------------------------------------------

            # Documentación Swagger: http://127.0.0.1:8000/docs
            # Documentación Redocly: http://127.0.0.1:8000/redoc