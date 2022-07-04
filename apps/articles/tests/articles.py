from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class ArticleTests(APITestCase):
    def test_list_articles(self):
        """
        Ensure we can get the list of articles.
        """
        url = reverse('article-list')
        
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
