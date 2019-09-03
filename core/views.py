from django.views.generic import (
    ListView, DetailView
)

from django.shortcuts import render


from core.models import Movie, Person

# Create your views here.


class MovieList(ListView):
    model = Movie
    context_object_name = 'movies'


class MovieDetail(DetailView):
    queryset = Movie.objects.all_with_prefetch_persons()
    context_object_name = 'movie'


class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()
