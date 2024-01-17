from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# A modo de ejemplo/aprendizaje se introduce clase user y atributos

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool
    
class UserDB(User):
    password: str
    

# Se simula base de datos NO RELACIONAL (las cuales suelen tener estructuras tipo JSON)
user_db = {
    "roberto": {
        "username": "rdoriol",
        "full_name": "Roberto Díaz",
        "email": "rd@gmail.com",
        "disabled": False,
        "password": "1234" # (se debe encriptar)
    },
    "sandra": {
        "username": "sduran",
        "full_name": "Sandra Durán",
        "email": "sd@gmail.com",
        "disabled": True,
        "password": "4321" # (se debe encriptar)
    }
}

## TODO --> CONTINUAR POR 4:13