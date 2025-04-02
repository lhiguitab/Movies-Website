import os
from django.core.files import File
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie images in the database by matching filenames in 'media/movie/images/' with format m_TITLE.png"

    def handle(self, *args, **kwargs):
        images_dir = 'media/movie/images/'
        supported_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        updated_count = 0

        # 🔍 Recorremos todos los archivos en la carpeta
        for filename in os.listdir(images_dir):
            name, ext = os.path.splitext(filename)

            # Solo procesamos si tiene una extensión válida y empieza con 'm_'
            if ext.lower() in supported_extensions and name.startswith('m_'):
                # 🧠 Extraemos el nombre real de la película (quitamos el prefijo 'm_')
                movie_title = name[2:]  # Elimina 'm_'

                try:
                    movie = Movie.objects.get(title=movie_title)

                    image_path = os.path.join(images_dir, filename)
                    with open(image_path, 'rb') as img_file:
                        movie.image.save(filename, File(img_file), save=True)
                    updated_count += 1

                    self.stdout.write(self.style.SUCCESS(f"Image updated for: {movie_title}"))

                except Movie.DoesNotExist:
                    self.stderr.write(f"Movie not found: {movie_title}")
                except Exception as e:
                    self.stderr.write(f"Error updating {movie_title}: {str(e)}")

        self.stdout.write(self.style.SUCCESS(f"Finished updating images for {updated_count} movies."))
