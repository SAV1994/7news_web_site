import tempfile
from django.test import TestCase
from django.shortcuts import reverse

from ..models import User, News, Comment


class ApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='test@test.com', first_name='Ivan', last_name='Ivanov')
        News.objects.create(author=User.objects.get(id=1), header='Header', sub_header='Sub header',
                            image=tempfile.NamedTemporaryFile(suffix=".jpg").name, teaser='Teaser',
                            full_text='Full text')
        for _ in range(15):
            Comment.objects.create(news=News.objects.get(id=1), author=User.objects.get(id=1), text='Comment')

    def test_api_url_exists_at_desired_location(self):
        resp = self.client.get('/api/1/')
        self.assertEqual(resp.status_code, 200)

    def test_api_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:counter', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)

    def test_api_can_return_correct_data(self):
        resp = self.client.get('/api/1/')
        data = '{"number_of_comments":15}'
        self.assertEqual(resp.content.decode(), data)
