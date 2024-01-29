from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

router_jwt = APIRouter(prefix="/usersDB", tags=["userDB"])

ALGORITHM = "HS256"
    # openssl rand -hex 32 ## Clave/Semilla que unicamente será conocida por nuestro backend. Se utilizará para asegurar fuertemente la generación del token de login
SECRET_KEY = "f84b7df028c662556b87e3e9871980a18cd4611b33c2da43ac943be3e43e7ee4"
ACCESS_TOKEN_DURATION = 1

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


# todo--> --------------------------------------------------------------
    # todo-->       API CON COMPROBACIÓN DE LOGIN Y GENERACIÓN DE TOKEN 
    # todo-->       UTILIZANDO OAUTH2 Y JWT
# todo--> --------------------------------------------------------------


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str
    
users_db = {
    "rdoriol": {
        "username": "rdoriol",
        "full_name": "Roberto Díaz",
        "email": "rdoriol@gmail.com",
        "disabled": True,
        "password": "$2b$12$EiEax.u8yf/slw4/pk9Gz.uqBmaztKK6bST1oTqwZG30R3DWsV5L6"
    },
    "sduran": {
        "username": "sduran",
        "full_name": "Sandra Durán",
        "email": "sduran@gmail.com",
        "disabled": False,
        "password": "$2b$12$HUYnM/h3byss0w/G5gn0E.M7xuDX78uWbAa6bHk1pk2awoIYZFQmW"
    }
}


    # Consulta de todo el listado de la base de datos
@router_jwt.get("/all")
async def get_users():
    return users_db


   
    # Método para buscar registro concreto
def search_user(username: str):
    user = users_db.get(username)     
                # if username in users_db:                # 1. Forma igual de válida para buscar registro
    try:
        return UserDB(**user)     
                # return UserDB(**users_db[username])     # 1. Forma igual de válida para buscar registro
    except:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "No existe registro en BBDD")
    
    
    # # Método para comprobar validez de token actual generado al hacer login
async def auth_user_token(token: str = Depends(oauth2)):
    
    exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Credenciales de autenticación no válidas", headers = {"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    
    return search_user(username)
    
    
    
    #  Por ejemplo para comprobar si el usuario con token validado está "disabled"
async def current_user(user: User = Depends(auth_user_token)):
    if user.disabled:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Usuario inactivo")
    return user

    
    # LOGIN
@router_jwt.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):   
    user = users_db.get(form.username)           # Alternativa de búsqueda de username en BBDD
    
    if not user:    # Este bloque de if se podría eliminar, pues con el método search_user() se lanza una excepción en caso de no existir username en BBDD
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No existe username introducido.")
    
    user = search_user(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "La contraseña no es correcta.")

    access_token = {"sub": user.username, "exp": datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_DURATION)}
  
    return {"access_token": jwt.encode(access_token, SECRET_KEY, algorithm = ALGORITHM), "token_type": "bearer"}


@router_jwt.get("/me")
async def me(user: User = Depends(current_user)):
    return user

    
        