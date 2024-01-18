from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# A modo de ejemplo/aprendizaje se introduce clase user y atributos

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool
    
class UserDB(User):
    password: str
    

# Se simula BBDD NO RELACIONAL (las cuales suelen tener estructuras tipo JSON)
users_db = {
    "rdoriol": {
        "username": "rdoriol",
        "full_name": "Roberto Díaz",
        "email": "rd@gmail.com",
        "disabled": False,
        "password": "1234" # (se debe encriptar)
    },
    "sduran": {
        "username": "sduran",
        "full_name": "Sandra Durán",
        "email": "sd@gmail.com",
        "disabled": True,
        "password": "4321" # (se debe encriptar)
    }
}

def searchUser(username: str):
    try:
        if username.lower() in users_db:
            return UserDB(**users_db[username.lower()])
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Registro no encontrado en search()")
  
    
    # Crear criterio de dependencia para ser utilizado en me(user: User = Depends())
async def currentToken(token: str = Depends(oauth2)):
    user = searchUser(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas", header={"WWW-Authenticate": "Bearer"})
    
    if user.disabled:
        return "Usuario desactivado"
    
    return user


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
        # 1º se comprueba si existe el username introducido en el formulario
    userDB = users_db.get(form.username.lower())    
    if not userDB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username no encontrado en login()")
    
        # 2º si el username existe
    userData = searchUser(form.username)
    if not form.password == userData.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contraseña incorrecta")
    
        # Retorna un access token (estandar que hay que seguir obligatoriamente)
    return {"access_token": userData.username, "token_type": "bearer"}
    

# Una vez autenticaddo con username y password en login() se genera método para obtener el token con el que 
# me he autenticado. Así, en cada operación que se realice en backen se solicitará este método para 
# comprobar que la autenticación fue correcta en su momento y no tener que volver a solicitarla
    # Método para devolver el token generado en login()
@app.get("/users/me")
async def me(user: User = Depends(currentToken)):
    return user
    