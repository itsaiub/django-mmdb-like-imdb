from django.views.generic import (
    ListView, DetailView
)

from django.shortcuts import render


from core.models import Movie

# Create your views here.


class MovieList(ListView):
    model = Movie
    context_object_name = 'movies'


class MovieDetail(DetailView):
    model = Movie
    context_object_name = 'movie'
