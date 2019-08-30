from django.test import TestCase
from django.urls import reverse, resolve

from .views import fines_index, player_detail, high_score
from .models import Player, Payment, Fine


class FinesTests(TestCase):

    def setUp(self):
        Player.objects.create(name="Spelare 1")

    def test_fines_view_status_code(self):
        url = reverse('fines_index')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_fines_url_resolves_fines_view(self):
        view = resolve('/')
        self.assertEquals(view.func, fines_index)

    def test_player_detail_success_status_code(self):
        url = reverse('player_detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_player_detail_not_found_status_code(self):
        url = reverse('player_detail', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_player_detail_url_resolves_player_detail_view(self):
        view = resolve('/1/')
        self.assertEquals(view.func, player_detail)

    def test_high_score_view_status_code(self):
        url = reverse('high_score')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_high_score_url_resolves_high_score_view(self):
        view = resolve('/high_score')
        self.assertEquals(view.func, high_score)


