    # Función que formatea los datos recibidos de BBDD a diccionario para servir/mostrar a cliente
def user_schema(user_db) -> dict:
    return {"id": str(user_db["_id"]),
            "username": user_db["username"],
            "email": user_db["email"]
            }