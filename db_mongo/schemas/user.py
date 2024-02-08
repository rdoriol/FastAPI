    # Función que formatea los datos recibidos de BBDD a diccionario para servir/mostrar a cliente
def user_schema(user_db) -> dict:
    return {"id": str(user_db["_id"]),
            "username": user_db["username"],
            "email": user_db["email"]
            }

def users_schema(users_db) -> list:
            # Comprenhesive lists. Mismo resultado que en método users_schema2222 pero en una sola línea
    return [user_schema(user) for user in users_db]




    # Método de prueba para comprender mejor las Comprenhesive list
# def users_schema2222(users_db) -> list:
#   lists = []    
#   for i in users_db:
#      lists.append(user_schema(i))    
#   return lists
    