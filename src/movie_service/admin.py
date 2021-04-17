from django.contrib import admin
from .models import Movie, Genre, MovieGenre, User, Rating

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(MovieGenre)
admin.site.register(User)
admin.site.register(Rating)
