from fastapi.routing import APIRouter
from typing import Annotated
from fastapi import Path

from .settings import Settings
from .models import model, on_memory_db
from .parser import Parser
from .saver import Saver

'''
Write few endpoints on one of the following libs ( Flask, FastAPI )
get: /all_products/ - return all information about all products
get: /products/{product_name} - return information about exact
product
get: //products/{product_name}/{product_field} - return information
about exact field exact product
'''


settings = Settings()
router = APIRouter()
# on memory database
database = on_memory_db.OnMemoryDatabase()
# and saver
saver = Saver(settings.base_saving_dir)

if database.isEmpty():
    # parsing all data
    products: list[dict[str, str]] = Parser(
        'https://www.mcdonalds.com/dnaapp/itemList?country=UA&language=uk&showLiveData=true&item={}()&nutrient_req=Y',
        'https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html'
    ).parse()

    # saving it and adding to database
    for product in products:
        database.create( model.Product(**product) )
        saver.save(product)



@router.get("/all_products")
def all_products():
    return database.getAll()


@router.get("/products/{product_name}")
def product(product_name: Annotated[str, Path(title="The name of product")]):
    return database.findByName(product_name) if database.findByName(product_name) else {}


@router.get("/products/{product_name}/{product_field}")
def product(
        product_name: Annotated[str, Path(title="The name of product")],
        product_field: Annotated[str, Path(title="The name of field")]
    ):
    product = database.findByName(product_name)
    if not product: return {}

    # will return { name: "not found" } if nothing found
    return {
        'data': {
            'key': product_field,
            'value': getattr(product, product_field, None)
        }
    }

