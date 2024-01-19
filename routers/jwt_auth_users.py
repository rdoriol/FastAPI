from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime, time

app = FastAPI()

ALGORITHM = "PHS256"

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

    # todo--> API CON COMPROBACIÓN DE LOGIN Y GENERACIÓN DE TOKEN 
    # todo--> UTILIZANDO OAUTH2 Y JWT
# 1. Enrutar fichero para que se tenga acceso desde el fichero principal
# 2. Simmular base de datos 
# 3. Crear clases con herenecias con las definiciones de atributos
# 4. Definir función buscador usuario en base de datos simulada
# 5. Definir decorador login para que usuario comprobar login correcto que generará un token de autenticación
# 6. Definir decorador para comprobar token generado al hacer login
# 7. Generar funciones para comprobar actual token de usuario (current_user) y (auth_user)
# 8. Todo ello con OAuth2 y JWT, Bearer y Hash con algoritmo PHS256
