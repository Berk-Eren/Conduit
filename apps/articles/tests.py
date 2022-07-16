from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.articles.models import Article
from apps.user.models import CustomUser

class ArticleTests(APITestCase):
    def setUp(self):
        credentials = {"username": "test", "password": "test"}
        CustomUser.objects.create(**credentials)
        self.client.login(**credentials)

    def test_list_articles(self):
        """
        Ensure we can get the list of articles.
        """
        url = reverse('article-list')
        
        response = self.client.get(url, format='json')
        breakpoint()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
