
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# IMPORTACIÓN DE DATOS
# df = pd.read_csv("recomendacion_supermercado_dataset.csv")

# Generar un ID único para cada producto
# Obtén los valores únicos de la columna 'Product'
# unique_products = df['Product'].unique()

# Crea un diccionario que mapea cada producto a un ProductID
# product_id_map = {product: idx for idx, product in enumerate(unique_products, start=1)}

# Crear una nueva columna 'ProductID' mapeando desde 'Product'
# df['ProductID'] = df['Product'].map(product_id_map)

# Verificar el DataFrame actualizado
# print(df.head())

# Guardar el DataFrame actualizado en un nuevo archivo CSV
# df.to_csv('recomendacion_supermercado_dataset_2.csv', index=False)

# IMPORTACIÓN DE DATOS
df = pd.read_csv("recomendacion_supermercado_dataset_2.csv")

# Creamos una matriz item-usuario solo con los datos necesarios
iu = df.pivot_table(index='UserID', columns='ProductID', values='Quantity', fill_value=0)


# CÁLCULO DE LA SIMILITUD DE ITEMS
similitud_items = cosine_similarity(iu.to_numpy())

# CREACIÓN DE UNA MATRIZ DE RECOMENDACIONES
matriz_recomendaciones = pd.DataFrame(similitud_items, index=iu.index, columns=iu.index)

# Convertir el DataFrame de una matriz a un formato largo
matriz_recomendaciones_long = matriz_recomendaciones.stack().rename_axis(['id1', 'id2']).reset_index(name='similitud')
matriz_recomendaciones_long = matriz_recomendaciones_long[matriz_recomendaciones_long['id1'] != matriz_recomendaciones_long['id2']]
matriz_recomendaciones_long = matriz_recomendaciones_long[matriz_recomendaciones_long['id1'] < matriz_recomendaciones_long['id2']]

# Unir las imágenes de 'id2'
# matriz_recomendaciones_long = matriz_recomendaciones_long.join(images, on='id2')

# GUARDA LA MATRIZ DE RECOMENDACION A DISCO
matriz_recomendaciones_long.to_pickle("matriz_recomendaciones_long.pkl")



