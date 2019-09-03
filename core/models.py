from django.db import models
from django.conf import settings
from django.db.models.aggregates import Sum

from uuid import uuid4
# Create your models here.


class MovieManager(models.Manager):
    def all_with_related_persons(self):
        qs = self.get_queryset()
        qs = qs.select_related('director')
        qs = qs.prefetch_related('writers', 'actors')

        return qs

    def all_with_related_persons_and_scores(self):
        qs = self.all_with_related_persons()
        qs = qs.annotate(score=Sum('vote__value'))

        return qs


class Movie(models.Model):
    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3

    RATINGS = (
        (NOT_RATED, 'NR - Not Rated'),
        (RATED_G, 'G - General Audiences'),
        (RATED_PG, 'PG - Parental Guidance'),
        (RATED_R, 'R - Restricted'),
    )

    title = models.CharField(max_length=140)
    plot = models.TextField()
    year = models.PositiveIntegerField()
    rating = models.IntegerField(choices=RATINGS, default=NOT_RATED)
    runtime = models.PositiveIntegerField()
    website = models.URLField(blank=True)
    director = models.ForeignKey(
        to='Person', on_delete=models.SET_NULL, related_name='directed', blank=True, null=True)
    writers = models.ManyToManyField(
        to='Person', related_name='writing_credits', blank=True)
    actors = models.ManyToManyField(
        to='Person', through='Role', related_name='acting_credits', blank=True)

    objects = MovieManager()
    # descending order in year, its like ORDER BY year DESC, title

    class Meta:
        ordering = ('-year', 'title')

    def __str__(self):
        return f'{self.title} ({self.year})'


class Role(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    person = models.ForeignKey('Person', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=140)

    def __str__(self):
        return f'{self.movie_id} - {self.person_id} ({self.name})'

    class Meta:
        unique_together = ('movie', 'person', 'name')


class PersonManager(models.Manager):
    """ Custom Manager. Using prefetch_related() method, django will query all related data accross a single relationship ina a single addtional query. we're telling dajango to prefetch all the movies that a person has directed, written and had a role in as well as prefetch the role themselves. """

    def all_with_prefetch_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related(
            'directed',
            'writing_credits',
            'role_set__movie'
        )


class Person(models.Model):
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    born = models.DateField()
    died = models.DateField(null=True, blank=True)

    objects = PersonManager()

    class Meta:
        ordering = (
            'last_name', 'first_name'
        )

    def __str__(self):
        if self.died:
            return f'{self.last_name}, {self.first_name} ({self.born} to {self.died})'
        return f'{self.last_name}, {self.first_name} ({self.born})'


class VoteManager(models.Manager):
    def get_vote_or_unsaved_blank_vote(self, movie, user):
        try:
            return Vote.objects.get(
                movie=movie,
                user=user
            )
        except Vote.DoesNotExist:
            return Vote(
                movie=movie,
                user=user
            )


class Vote(models.Model):
    UP = 1
    DOWN = -1
    VALUE_CHOICES = (
        (UP, '👍'),
        (DOWN, '👎')
    )

    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now=True)

    objects = VoteManager()

    class Meta:
        """
            the unique together attribute creates a unique constraint on the table which prevent two rows having same value for both user and movie, enforcing rule one vote per user per one movie
        """
        unique_together = ('user', 'movie')

    def __str__(self):
        return self.user.username


def movie_directory_path_with_uuid(instance, filename):
    return '{}/{}'.format(instance.movie_id, uuid4())


class MovieImage(models.Model):
    image = models.ImageField(upload_to=movie_directory_path_with_uuid)
    uploaded = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.movie.title
