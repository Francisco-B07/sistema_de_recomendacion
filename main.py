# pip install fastapi uvicorn pandas
#para lanzarlo poner en el terminal:
#uvicorn recomendador_api:app
#curl http://127.0.0.1:8000/recomendaciones/0

import pandas as pd

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Montar el directorio estático
app.mount("/static",StaticFiles(directory="./public/static"),name="static")

# Configuración de las plantillas
templates = Jinja2Templates(directory="./public/templates")

# Configurar CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://127.0.0.1:5500"],  # Lista de orígenes permitidos
#     allow_credentials=True,
#     allow_methods=["*"],  # Métodos permitidos
#     allow_headers=["*"],  # Cabeceras permitidas
# )

# Leer el archivo CSV
df = pd.read_csv('recomendacion_supermercado_dataset_2.csv')

# Devolver 20 productos
def get_products():    
    products = df.head(20).to_dict(orient='records')
    return products



# Carga la matriz de recomendaciones del disco
matriz_recomendaciones_long = pd.read_pickle("matriz_recomendaciones_long.pkl")


@app.get("/",response_class=HTMLResponse)
def root():
    html_address = "./public/static/html/index.html"
    return FileResponse(html_address, status_code=200)

@app.get("/product/{productId}/{userId}",response_class=HTMLResponse)
def product(request: Request, productId:int, userId:str):
   
    producto =  df.loc[df['ProductID'] == productId].to_dict(orient='records')
    print(producto)
    return templates.TemplateResponse("product.html",{"request":request, "productId": productId, "userId": userId, "producto": producto[0]})

@app.get("/product/{productId}")
async def ver_producto(productId: int):

    producto =  df.loc[df['ProductID'] == productId].to_dict(orient='records')

    if producto:
        return producto[0]
    return {"error": "Producto no encontrado"}


@app.get("/recomendaciones/{item_id}")
async def hacer_recomendacion(item_id: int, n: int = 3):
    # Verifica que el item exista en la matriz
    if item_id in matriz_recomendaciones_long['id1'].unique():
        # Filtra donde 'id1' sea igual al item proporcionado
        recomendaciones = matriz_recomendaciones_long[matriz_recomendaciones_long['id1'] == item_id]
        
        # Ordena por similitud de manera descendente y selecciona los primeros n resultados
        recomendaciones = recomendaciones.sort_values(by='similitud', ascending=False).head(n)
        
        return recomendaciones.to_dict(orient="records")
    else:
        raise HTTPException(status_code=404, detail=f"Error: El ID {item_id} no se encuentra en las columnas del DataFrame.")

@app.get("/products")
async def all_products():
    products = df.head(80)
    return products.to_dict(orient='records')


