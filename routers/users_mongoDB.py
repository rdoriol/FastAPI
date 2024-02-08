from fastapi import APIRouter, HTTPException, status
from db_mongo.models.user import User      # Se importa modelo de la clase User ubicado en db_mongo/models/user.py
from db_mongo.client import db_client       # Se importa fichero para conectar con la BBDD.
from db_mongo.schemas.user import user_schema, users_schema
from bson import ObjectId   # Clase para crear objetos id, necesario para trabajar con _id generado auto por mongoDB

router_userdb = APIRouter(prefix= "/usersdb", tags=["users"])

# todo          -----------------
# todo           GET DE USUARIOS
# todo          -----------------


@router_userdb.get("/", response_model= list[User])
async def users():
    
    return users_schema(db_client.users.find())


# todo          ------------------------
# todo           PATH BÚSQUEDA USUARIOS
# todo          ------------------------

    # Búsqueda de usuarios a través del path
@router_userdb.get("/{username}")
async def searchUser(username: str):
    user = searchUserDB("username", username)
    try:
        return user
    except:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Registro no encontrado en base de datos")
    # La búsqueda en navegador o consumidor de API sería:
    #       127.0.0.1:8000/usersdb/3
    
    
# todo          -------------------------
# todo           PARÁMETROS POR QUERY
# todo          -------------------------

    # Búsqueda de usuarios a través de query
@router_userdb.get("/usersdbQuery")
async def searchUser(username: str):
    
    user = searchUserDB("username", username)
    try:
        return user
    except:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Registro no encontrado en BBDD")
    
    # La búsqueda en navegador o consumidor de API sería:
    #       127.0.0.1:8000/userQuery/?username=rdoriol
    

 
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
    id = db_client.users.insert_one(user_dict).inserted_id
    
        # Para retornar el regitro completo del usuario se realiza una búsqueda en la BBDD. Para la búsqueda se utiliza el método user_schema con el _id
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    
        # Se retorna el diccionario recibido de BBDD en un objeto de la clase User
    return User(**new_user)
            
        
    # Nota: Lo más correcto sería crear una función externa que fuera llamada en la función async del decorador (Se evita la duplicidad de código)
def searchUserDB(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se encuentra usuario en BBDD pepe"}

    

# todo          ------------------
# todo           PUT (actualizar)
# todo          ------------------
                # Con PUT se actualiza el registro completo (tanto la parte modificada como la parte que no)
@router_userdb.put("/")
async def updateUser(user: User):
    
    user_dict = dict(user)
    del user_dict["id"]
    
    try:
        db_client.users.find_one_and_replace({"username": user_dict["username"]}, user_dict)
                
    except:
        return {"error": "No se ha actualizado el usuario"}
    
    return searchUserDB("username", user.username)
    


# todo          ------------------
# todo           DELETE (eliminar)
# todo          ------------------

@router_userdb.delete("/{username}", status_code= status.HTTP_204_NO_CONTENT)
async def deleteUser(username: str):
  
    found = db_client.users.find_one_and_delete({"username": username}) 
    
    if not found:
        return {"error": "Usuario no encontrado. Registro no eliminado"}
    
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