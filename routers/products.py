from fastapi import APIRouter
#                                               "tags" para agrupar en documentación
router_products = APIRouter(prefix="/products", tags=["products"], responses={404: {"mensaje": "Registro no encontrado"}})  # Con prefix ya no hace falta especificar patch en decorador --> 1*

products_list = ["Producto 1", "Producto 2", "Producto 3", "Producto 4"]

@router_products.get("/")    # 1*
async def products():
    return products_list

@router_products.get("/{id}")
async def product(id: int):
    return products_list[id]