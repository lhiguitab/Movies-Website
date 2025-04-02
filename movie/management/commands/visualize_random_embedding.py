import numpy as np
import random
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Select a random movie and display the first values of its embedding"

    def handle(self, *args, **kwargs):
        movies = list(Movie.objects.exclude(emb=None))

        if not movies:
            self.stderr.write("No movies found with embeddings.")
            return

        movie = random.choice(movies)

        try:
            embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)
            self.stdout.write(self.style.SUCCESS(f"🎬 Movie: {movie.title}"))
            self.stdout.write("🔢 Embedding (first 10 values):")
            self.stdout.write(str(embedding_vector[:10]))
        except Exception as e:
            self.stderr.write(f"Error reading embedding for {movie.title}: {str(e)}")
