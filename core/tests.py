from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.test.client import \
    RequestFactory
from django.urls.base import reverse

from core.models import Movie
from core.views import MovieList


class MovieListPaginationTestCase(TestCase):
    ACTIVE_PAGINATION_HTML = """
      <li class='page-item active'>
        <a href='{}?page={}' class='page-link'>{}</a>
      </li>
    """

    def setUp(self):
        for n in range(15):
            Movie.objects.create(
                title='Title {}'.format(n),
                year=1990 + n,
                runtime=100,
            )

    def testFirstPage(self):
        movie_list_path = reverse('core:MovieList')
        request = RequestFactory().get(path=movie_list_path)
        reponse = MovieList.as_view()(request)
        self.assertEquals(200, reponse.status_code)
        self.assertTrue(reponse.context_data['is_paginated'])
        self.assertInHTML(
            self.ACTIVE_PAGINATION_HTML.format(
                movie_list_path, 1, 1
            ),
            reponse.rendered_content
        )
