from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

from .models import Movie

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name':'Lucas Higuita'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render (request, 'home.html', {'searchTerm':searchTerm, 'movies':movies})

def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})

def statistics_view(request):
    matplotlib.use('Agg')
    # Obtener todas las peliculas
    all_movies = Movie.objects.all()

    # Crear un diccionario para almacenar la cantidad de peliculas por año
    movie_counts_by_year = {}

    # Filtrar las peliculas por año y contar la cantidad de peliculas por año
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

    # Ancho de las barras
    bar_width = 0.5
    # Posiciones de las barras
    bar_positions = range(len(movie_counts_by_year))

    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')

    # Personalizar la grafica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    # Ajustar el espacio entre las barras
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en un objeto BytesIO
    buffer_year = io.BytesIO()
    plt.savefig(buffer_year, format='png')
    buffer_year.seek(0)
    plt.close()

    # Convertir la gráfica en formato base64
    image_year_png = buffer_year.getvalue()
    buffer_year.close()
    graphic_year = base64.b64encode(image_year_png)
    graphic_year = graphic_year.decode('utf-8')

    # Grafica de peliculas por genero (Solo el primer genero)
    # Crear un diccionario para almacenar la cantidad de peliculas por genero
    movie_counts_by_genre = {}

    # Filtrar las peliculas por genero y contar la cantidad de peliculas por genero
    for movie in all_movies:
        genre = movie.genre.split(',')[0]
        if genre in movie_counts_by_genre:
            movie_counts_by_genre[genre] += 1
        else:
            movie_counts_by_genre[genre] = 1
    
    # Ancho de las barras
    bar_width = 0.5
    # Posiciones de las barras
    bar_positions = range(len(movie_counts_by_genre))

    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center')

    # Personalizar la grafica
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=90)

    # Ajustar el espacio entre las barras
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en un objeto BytesIO
    buffer_genre = io.BytesIO()
    plt.savefig(buffer_genre, format='png')
    buffer_genre.seek(0)
    plt.close()

    # Convertir la gráfica en formato base64
    image_genre_png = buffer_genre.getvalue()
    buffer_genre.close()
    graphic_genre = base64.b64encode(image_genre_png)
    graphic_genre = graphic_genre.decode('utf-8')

    # Renderizar la plantilla statistics.html con la gráfica
    return render(request, 'statistics.html', {'graphic_year': graphic_year, 'graphic_genre': graphic_genre})