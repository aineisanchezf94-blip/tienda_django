from django.test import TestCase
from django.urls import reverse


class ProductSearchByInitialTest(TestCase):
    def test_search_by_initial_letter_returns_matching_products(self):
        response = self.client.get(reverse('index'), {'q': 'm'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Resultados para:')
        self.assertContains(response, 'Mac')
