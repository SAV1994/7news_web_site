import tempfile
from django.test import TestCase

from ..models import User, Rule, News, Comment


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='test@test.com', password='123qwe321', first_name='Anton',
                            last_name='Gorodetskiy')

    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_email_unique(self):
        field_unique = self.user._meta.get_field('email').unique
        self.assertEqual(field_unique, True)

    def test_email_label(self):
        field_label = self.user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_first_name_label(self):
        field_label = self.user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_firs_name_max_length(self):
        field_max_length = self.user._meta.get_field('first_name').max_length
        self.assertEqual(field_max_length, 20)

    def test_last_name_label(self):
        field_label = self.user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_last_name_max_length(self):
        field_max_length = self.user._meta.get_field('last_name').max_length
        self.assertEqual(field_max_length, 20)


class RuleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Rule.objects.create(rule='be polite')

    def setUp(self):
        self.rule = Rule.objects.get(id=1)

    def test_rule_label(self):
        field_label = self.rule._meta.get_field('rule').verbose_name
        self.assertEqual(field_label, 'rule')

    def test_rule_max_length(self):
        field_max_length = self.rule._meta.get_field('rule').max_length
        self.assertEqual(field_max_length, 256)


class NewsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='test@test.com', password='123qwe321', first_name='Anton',
                            last_name='Gorodetskiy')
        News.objects.create(author=User.objects.get(id=1), header='Header', sub_header='Sub header',
                            image=tempfile.NamedTemporaryFile(suffix=".jpg").name, teaser='Teaser',
                            full_text='Full text')

    def setUp(self):
        self.news = News.objects.get(id=1)

    def test_author_label(self):
        field_label = self.news._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_header_label(self):
        field_label = self.news._meta.get_field('header').verbose_name
        self.assertEqual(field_label, 'header')

    def test_header_max_length(self):
        field_max_length = self.news._meta.get_field('header').max_length
        self.assertEqual(field_max_length, 100)

    def test_sub_header_label(self):
        field_label = self.news._meta.get_field('sub_header').verbose_name
        self.assertEqual(field_label, 'sub header')

    def test_sub_header_max_length(self):
        field_max_length = self.news._meta.get_field('sub_header').max_length
        self.assertEqual(field_max_length, 50)

    def test_image_label(self):
        field_label = self.news._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'image')

    def test_teaser_label(self):
        field_label = self.news._meta.get_field('teaser').verbose_name
        self.assertEqual(field_label, 'teaser')

    def test_teaser_max_length(self):
        field_max_length = self.news._meta.get_field('teaser').max_length
        self.assertEqual(field_max_length, 320)

    def test_full_text_label(self):
        field_label = self.news._meta.get_field('full_text').verbose_name
        self.assertEqual(field_label, 'full text')

    def test_full_text_max_length(self):
        field_max_length = self.news._meta.get_field('full_text').max_length
        self.assertEqual(field_max_length, 10000)


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='test@test.com', password='123qwe321', first_name='Anton',
                            last_name='Gorodetskiy')
        News.objects.create(author=User.objects.get(id=1), header='Header', sub_header='Sub header',
                            image=tempfile.NamedTemporaryFile(suffix=".jpg").name, teaser='Teaser',
                            full_text='Full text')
        Comment.objects.create(news=News.objects.get(id=1), author=User.objects.get(id=1), text='Comment')

    def setUp(self):
        self.news = Comment.objects.get(id=1)

    def test_news_label(self):
        field_label = self.news._meta.get_field('news').verbose_name
        self.assertEqual(field_label, 'news')

    def test_comment_label(self):
        field_label = self.news._meta.get_field('comment').verbose_name
        self.assertEqual(field_label, 'comment')

    def test_author_label(self):
        field_label = self.news._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_date_added_label(self):
        field_label = self.news._meta.get_field('date_added').verbose_name
        self.assertEqual(field_label, 'date added')

    def test_text_label(self):
        field_label = self.news._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_text_max_length(self):
        field_max_length = self.news._meta.get_field('text').max_length
        self.assertEqual(field_max_length, 10000)
