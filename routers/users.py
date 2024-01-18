from fastapi import APIRouter, HTTPException
from pydantic import BaseModel  # Capacidad de crear una entidad (proporciona un constructor sin necesidad de crearlo nosotros mismos)

router_user = APIRouter(tags=["users"])

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
    
    # Lista para utilizar como si fuera una base de datos y poder hacer CRUD
users_list = [  User(id = 1, name = "Roberto", surname = "Díaz", age = 44, url = "https://rdo.com"),
                User(id = 2, name = "Sandra", surname = "Durán", age = 46, url = "https://sdo.com"),
                User(id = 3, name = "Lucía", surname = "Díaz", age = 44, url = "https://ldd.com"),
                User(id = 4, name = "Darío", surname = "Díaz", age = 44, url = "https://ddd.com")
            ]

@router_user.get("/usersJson")      ## función de prueba
async def usersJson():
    return {"name": "Roberto", "surname": "Díaz", "age": 44, "url": "https://rdo.com"}

@router_user.get("/users")
async def users():
    return users_list   # FastAPI lo convierte automáticamente en JSON 


# todo          ------------------------
# todo           PATH BÚSQUEDA USUARIOS
# todo          ------------------------

    # Búsqueda de usuarios a través del path
@router_user.get("/user/{id}")
async def searchUser(id: int):
    users = filter(lambda argumento: argumento.id == id, users_list)
    try:
        return list(users)[0]
    except:
        raise HTTPException(status_code=204, detail="Registro no encontrado en base de datos")
        # return {"error": "Registro no encontrado en base de datos"}
    
    # La búsqueda en navegador o consumidor de API sería:
    #       127.0.0.1:8000/user/3
    
    
# todo          -------------------------
# todo           PARÁMETROS POR QUERY
# todo          -------------------------

    # Búsqueda de usuarios a través de query
@router_user.get("/userQuery")
async def searchUser(id: int):
    return searchUser(id)
    
    # La búsqueda en navegador o consumidor de API sería:
    #       127.0.0.1:8000/userQuery/?id=2
    

 
# todo          ---------------
# todo           POST (create)
# todo          ---------------

@router_user.post("/user", response_model= User, status_code = 201)
async def newUser(user: User):
    if type(searchUser(user.id)) == User:
        raise HTTPException(status_code=204, detail="Registro ya existente")
    users_list.append(user)
    return user
        
        
# Nota: Lo más correcto sería crear una función externa que fuera llamada en la función async del decorador (Se evita la duplicidad de código)
def searchUser(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No existe registro en base de datos"}
    

# todo          ------------------
# todo           PUT (actualizar)
# todo          ------------------
                # Con PUT se actualiza el registro completo (tanto la parte modificada como la parte que no)
@router_user.put("/user")
async def updateUser(user: User):
    found = False
    
    for index, savedUser in enumerate(users_list):
        if savedUser.id == user.id:
            users_list[index] = user
            found = True
    
    if not found:
        return{"error": "Registro no actualizado"}    
    
    return user


# todo          ------------------
# todo           DELETE (eliminar)
# todo          ------------------

@router_user.delete("/user/{id}")
async def deleteUser(id: int):
    found = 0
    
    for index, deleteUser in enumerate(users_list):
        if deleteUser.id == id:
            del users_list[index]
            found = 1
    
    if not found:
        return {"error": "Registro no eliminado"}
    
    return {"success": "Registro eliminado con éxito"}


# todo          -------------------
# todo           HTTP STATUS CODES
# todo          -------------------

        # Se pueden controlar los códigos HTTP retornados en las peticiones
        
        # En decorador añadir parámetro "status_code=xxx"
        #   Ej. @app.post("/user", status_code=201)
        
        # EJEMPLO DE USO: líneas 45, 70, 72.


# todo          --------
# todo           ROUTES
# todo          --------

        # Server iniciado en fichero principal ("main.py"). 
        # En fichero principal se enruta hacía las distintas páginas existentes:
        #    Se utiliza método de la clase FastAPI .include_rotuer()
        
        # EJEMPLO DE USO: 
        #                  1º. fichero "products.py" líneas: 1, 3, 4
        #                  2º. fichero "main.py" líneas: 4, 9, 10
        

# todo          --------------------
# todo           RECURSOS ESTÁTICOS
# todo          --------------------

                # Rutas para mostrar por ejemplo imágenes.
                # Fichero "main.py" líneas: 5, 13


# todo          --------------------
# todo           AUTORIZACIÓN OAUTH2
# todo          --------------------

                # Ver fichero "routes/auth_basic_users.py"