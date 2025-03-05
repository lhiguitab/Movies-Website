import pandas as pd
import json

# Lee el archivo CSV
df = pd.read_csv('movies_initial.csv')

#Guardar el DataFrame en un archivo JSON
df.to_json('movies.json', orient='records')

with open('movies.json') as file:
    movies = json.load(file)

for i in range(100):
    movie = movies[i]
    print(movie)
    break