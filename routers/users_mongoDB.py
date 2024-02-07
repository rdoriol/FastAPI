from fastapi import APIRouter, HTTPException, status
from db_mongo.models.user import User      # Se importa modelo de la clase User ubicado en db_mongo/models/user.py
from db_mongo.client import db_client       # Se importa fichero para conectar con la BBDD.
from db_mongo.schemas.user import user_schema

router_userdb = APIRouter(prefix= "/usersdb", tags=["users"])

# todo          -----------------
# todo           GET DE USUARIOS
# todo          -----------------

    
    # Lista para utilizar como si fuera una base de datos y poder hacer CRUD
users_list = []


@router_userdb.get("/")
async def users():
    
    return user_schema(db_client.local.users.find()) # todo SOLUCIONAR   # FastAPI lo convierte automáticamente en JSON 


# todo          ------------------------
# todo           PATH BÚSQUEDA USUARIOS
# todo          ------------------------

    # Búsqueda de usuarios a través del path
@router_userdb.get("/{id}")
async def searchUser(id: int):
    users = filter(lambda argumento: argumento.id == id, users_list)
    try:
        return list(users)[0]
    except:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Registro no encontrado en base de datos")
        # return {"error": "Registro no encontrado en base de datos"}
    
    # La búsqueda en navegador o consumidor de API sería:
    #       127.0.0.1:8000/user/3
    
    
# todo          -------------------------
# todo           PARÁMETROS POR QUERY
# todo          -------------------------

    # Búsqueda de usuarios a través de query
@router_userdb.get("/userdbQuery")
async def searchUser(id: int):
    return searchUser(id)
    
    # La búsqueda en navegador o consumidor de API sería:
    #       127.0.0.1:8000/userQuery/?id=2
    

 
# todo          ---------------
# todo           POST (create)
# todo          ---------------

@router_userdb.post("/", status_code= status.HTTP_201_CREATED)
async def newUserDB(user: User):
    
        # Se comprueba si el user que se quiere insertar ya existe    
    if type(searchUserDB("username", user.username)) == User:
        raise HTTPException(status_code= status.HTTP_406_NOT_ACCEPTABLE, detail= "Ya existe username.")
        
        # Se convierte el user a insertar a formato diccionario para a continuación insertarlo en la BBDD
    user_dict = dict(user)
    
        # Se elmina el campo "id" del diccionario creado, para que no se grabe en base de datos a null. El id lo generará automaticamente MongoDB
    del user_dict["id"]
    
        # Conectar con BBDD, clase instanciada db_client y llamar a método para introducir un registro (con formato de diccionario)
        # En la siguiente línea, al mísmo tiempo se inserta registro en BBDD y se almacena en variable id el _id generado de forma auto por MongoDB
    id = db_client.local.users.insert_one(user_dict).inserted_id
    
        # Para retornar el regitro completo del usuario se realiza una búsqueda en la BBDD. Para la búsqueda se utiliza el método user_schema con el _id
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    
        # Se retorna el diccionario recibido de BBDD en un objeto de la clase User
    return User(**new_user)
            
        
    # Nota: Lo más correcto sería crear una función externa que fuera llamada en la función async del decorador (Se evita la duplicidad de código)
def searchUserDB(field: str, key):
    try:
        user = db_client.local.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se encuentra usuario en BBDD"}

    

# todo          ------------------
# todo           PUT (actualizar)
# todo          ------------------
                # Con PUT se actualiza el registro completo (tanto la parte modificada como la parte que no)
@router_userdb.put("/")
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

@router_userdb.delete("/{id}")
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