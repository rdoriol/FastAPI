from fastapi import FastAPI
from pydantic import BaseModel  # Capacidad de crear una entidad (proporciona un constructor sin necesidad de crearlo nosotros mismos)

app = FastAPI()

# todo          -----------------
# todo           GET DE USUARIOS
# todo          -----------------

    # Clase ubicada en este fichero a modo Tutorial (en producción las clases en módulos independientes)
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    url: str 

users_list = [  User(id = 1, name = "Roberto", surname = "Díaz", age = 44, url = "https://rdo.com"),
                User(id = 2, name = "Sandra", surname = "Durán", age = 46, url = "https://sdo.com"),
                User(id = 3, name = "Lucía", surname = "Díaz", age = 44, url = "https://ldd.com"),
                User(id = 4, name = "Darío", surname = "Díaz", age = 44, url = "https://ddd.com")
            ]

@app.get("/usersJson")
async def usersJson():
    return {"name": "Roberto", "surname": "Díaz", "age": 44, "url": "https://rdo.com"}

@app.get("/users")
async def users():
    return users_list   # FastAPI lo convierte automáticamente en JSON 

# todo          -----------------
# todo           PATH DE USUARIOS
# todo          -----------------

    # Búsqueda de usuarios a través del path
@app.get("/user/{id}")
async def user(id: int):
    users = filter(lambda argumento: argumento.id == id, users_list)
    return list(users)[0]
    