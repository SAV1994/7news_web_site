import tempfile
import os
from django.test import TestCase
from django.shortcuts import reverse

from ..models import User, News, Comment, Rule
from news.settings import MEDIA_ROOT


def _create_entries():
    User.objects.create(email='test3@test.com', first_name='Ivan', last_name='Ivanov')
    for _ in range(3):
        News.objects.create(author=User.objects.get(id=1), header='Header', sub_header='Sub header',
                            image=tempfile.NamedTemporaryFile(suffix=".jpg").name, teaser='Teaser',
                            full_text='Full text')
    for _ in range(3):
        Comment.objects.create(news=News.objects.get(id=3), author=User.objects.get(id=1), text='Comment')
    for _ in range(2):
        Comment.objects.create(news=News.objects.get(id=1), author=User.objects.get(id=1), text='Comment')


def _create_users():
    user_1 = User.objects.create(email='test@test.com', first_name='Ivan', last_name='Ivanov')
    user_1.set_password('123qwe321')
    user_1.save()
    user_2 = User.objects.create(email='test2@test.com', first_name='Ivan', last_name='Ivanov')
    user_2.set_password('123qwe321')
    user_2.save()


class IndexTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _create_entries()

    def test_index_url_exists_at_desired_location(self):
        resp_1 = self.client.get('/')
        resp_2 = self.client.get('/by_comments/')
        self.assertEqual(resp_1.status_code, 200)
        self.assertEqual(resp_2.status_code, 200)

    def test_index_url_accessible_by_name(self):
        resp_1 = self.client.get(reverse('main:index'))
        resp_2 = self.client.get(reverse('main:by_comments'))
        self.assertEqual(resp_1.status_code, 200)
        self.assertEqual(resp_2.status_code, 200)

    def test_index_uses_correct_template(self):
        resp_1 = self.client.get(reverse('main:index'))
        resp_2 = self.client.get(reverse('main:by_comments'))
        self.assertTemplateUsed(resp_1, 'main/index.html')
        self.assertTemplateUsed(resp_2, 'main/index.html')

    def test_index_return_correct_news(self):
        resp_1 = self.client.get(reverse('main:index'))
        news_1 = [news.pk for news in resp_1.context['news']]
        resp_2 = self.client.get(reverse('main:by_comments'))
        news_2 = [news.pk for news in resp_2.context['news']]
        self.assertEqual(news_1, [1, 2, 3])
        self.assertEqual(news_2, [3, 1, 2])

    def test_index_return_banner(self):
        resp_1 = self.client.get(reverse('main:index'))
        resp_2 = self.client.get(reverse('main:by_comments'))
        self.assertIsNotNone(resp_1.context['banner'])
        self.assertIsNotNone(resp_2.context['banner'])


class RegistrationTest(TestCase):
    def test_registration_url_exists_at_desired_location(self):
        resp = self.client.get('/registrar/')
        self.assertEqual(resp.status_code, 200)

    def test_registration_url_accessible_by_name(self):
        resp = self.client.get(reverse('main:registrar'))
        self.assertEqual(resp.status_code, 200)

    def test_registration_uses_correct_template(self):
        resp = self.client.get(reverse('main:registrar'))
        self.assertTemplateUsed(resp, 'main/registrar.html')

    def test_registration_give_rules(self):
        Rule.objects.create(rule='be polite')
        resp = self.client.get(reverse('main:registrar'))
        self.assertIsNotNone(resp.context['rules'])

    def test_registration_can_redirect_to_main_page(self):
        data = {'first_name': 'Ivan', 'last_name': 'Ivanov', 'email': 'ivanov@ivan.com', 'password': '123qwe321',
                'password_confirmation': '123qwe321', 'consent_with_rules': True}
        resp = self.client.post(path=reverse('main:registrar'), data=data)
        self.assertRedirects(resp, reverse('main:index'))

    def test_registration_can_register_and_login(self):
        data = {'first_name': 'Ivan', 'last_name': 'Ivanov', 'email': 'ivanov@ivan.com', 'password': '123qwe321',
                'password_confirmation': '123qwe321', 'consent_with_rules': True}
        resp = self.client.post(path=reverse('main:registrar'), data=data)
        user = User.objects.get(id=1)
        self.assertEqual(resp.wsgi_request.user, user)

    def test_form_invalid_confirm_password(self):
        data = {'first_name': 'Ivan', 'last_name': 'Ivanov', 'email': 'ivanov@ivan.com', 'password': '123qwe321',
                'password_confirmation': '123qwe320', 'consent_with_rules': True}
        resp = self.client.post(path=reverse('main:registrar'), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'password_confirmation', 'Password mismatch')


class EditUserTest(TestCase):
    def setUp(self):
        _create_users()
        self.data = {'first_name': 'Maxim', 'last_name': 'Pupkin', 'email': 'test3@test.com', 'password': '123qwe321',
                     'password_confirmation': '123qwe321', 'consent_with_rules': True}

    def test_edit_user_not_authorized_user_cannot_access(self):
        resp = self.client.get('/user/1/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=%2Fuser%2F1/')

    def test_edit_user_url_exists_at_desired_location(self):
        self.client.login(email='test@test.com', password='123qwe321')
        resp_1 = self.client.get('/user/1/')
        resp_2 = self.client.get('/user/1/by_comm/')
        self.assertEqual(resp_1.status_code, 200)
        self.assertEqual(resp_2.status_code, 200)

    def test_edit_user_url_accessible_by_name(self):
        self.client.login(email='test@test.com', password='123qwe321')
        resp_1 = self.client.get(reverse('main:personal', kwargs={'pk': 1}))
        resp_2 = self.client.get(reverse('main:personal_by_comm', kwargs={'pk': 1}))
        self.assertEqual(resp_1.status_code, 200)
        self.assertEqual(resp_2.status_code, 200)

    def test_edit_user_uses_correct_template(self):
        self.client.login(email='test@test.com', password='123qwe321')
        resp = self.client.get(reverse('main:personal', kwargs={'pk': 1}))
        self.assertTemplateUsed(resp, 'main/personal.html')

    def test_edit_user_authorized_user_cannot_access_to_someone_elses_data(self):
        self.client.login(email='test2@test.com', password='123qwe321')
        resp = self.client.get(reverse('main:personal', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 404)

    def test_edit_user_can_make_changes_to_data(self):
        self.client.login(email='test@test.com', password='123qwe321')
        self.client.post('/user/1/', self.data)
        user = User.objects.get(id=1)
        self.assertEqual(user.first_name, 'Maxim')
        self.assertEqual(user.last_name, 'Pupkin')
        self.assertEqual(user.email, 'test3@test.com')

    def test_edit_user_not_authorized_user_cannot_make_changes_to_data(self):
        resp = self.client.post('/user/1/', self.data)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=%2Fuser%2F1/')

    def test_edit_user_authorized_user_cannot_make_changes_to_someone_elses_data(self):
        self.client.login(email='test2@test.com', password='123qwe321')
        resp = self.client.post('/user/1/', self.data)
        self.assertEqual(resp.status_code, 404)

    def test_edit_user_return_correct_news(self):
        _create_entries()
        self.client.login(email='test@test.com', password='123qwe321')
        resp_1 = self.client.get('/user/1/')
        resp_2 = self.client.get('/user/1/by_comm/')
        news_1 = [news.pk for news in resp_1.context['news']]
        news_2 = [news.pk for news in resp_2.context['news']]
        self.assertEqual(news_1, [1, 2, 3])
        self.assertEqual(news_2, [3, 1, 2])

    def test_edit_user_user_remains_logged_in_after_made_changes_to_data(self):
        self.client.login(email='test@test.com', password='123qwe321')
        resp = self.client.post('/user/1/', self.data)
        user = User.objects.get(id=1)
        self.assertEqual(user.first_name, 'Maxim')
        self.assertEqual(resp.wsgi_request.user, user)


class AddNewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='test@test.com', first_name='Ivan', last_name='Ivanov')
        user.set_password('123qwe321')
        user.save()

    def test_add_news_not_authorized_user_cannot_access(self):
        resp = self.client.get('/news/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=%2Fnews%2F')

    def test_add_news_url_exists_at_desired_location(self):
        self.client.login(email='test@test.com', password='123qwe321')
        resp = self.client.get('/news/')
        self.assertEqual(resp.status_code, 200)

    def test_add_news_url_accessible_by_name(self):
        self.client.login(email='test@test.com', password='123qwe321')
        resp = self.client.get(reverse('main:add_news'))
        self.assertEqual(resp.status_code, 200)

    def test_add_news_uses_correct_template(self):
        self.client.login(email='test@test.com', password='123qwe321')
        resp = self.client.get(reverse('main:add_news'))
        self.assertTemplateUsed(resp, 'main/news.html')

    def test_add_news_can_add_news(self):
        with open('main/tests/test_img/test.png', 'rb') as file:
            data = {'author': 1, 'header': 'Header', 'sub_header': 'Sub header', 'image': file, 'teaser': 'Teaser',
                    'full_text': 'Full text'}
            self.client.login(email='test@test.com', password='123qwe321')
            resp = self.client.post('/news/', data)
            os.remove(os.path.join(MEDIA_ROOT, 'test.png'))
            self.assertIsNotNone(News.objects.get(id=1))
            self.assertRedirects(resp, reverse('main:index'))


class DeleteNewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _create_users()
        News.objects.create(author=User.objects.get(id=1), header='Header', sub_header='Sub header',
                            image=tempfile.NamedTemporaryFile(suffix=".jpg").name, teaser='Teaser',
                            full_text='Full text')

    def test_delete_news_not_authorized_user_cannot_access(self):
        resp = self.client.get('/delete_news/1/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=%2Fdelete_news%2F1/')

    def test_delete_news_url_exists_at_desired_location(self):
        self.client.login(email='test@test.com', password='123qwe321')
        resp = self.client.get('/delete_news/1/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('main:personal', kwargs={'pk': 1}))

    def test_delete_news_url_accessible_by_name(self):
        self.client.login(email='test@test.com', password='123qwe321')
        resp = self.client.get(reverse('main:delete_news', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('main:personal', kwargs={'pk': 1}))

    def test_delete_news_authorized_user_cannot_delete_someone_elses_entry(self):
        self.client.login(email='test2@test.com', password='123qwe321')
        resp = self.client.get('/delete_news/1/')
        self.assertEqual(resp.status_code, 404)


class EditNewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _create_users()
        News.objects.create(author=User.objects.get(id=1), header='Header', sub_header='Sub header',
                            image=tempfile.NamedTemporaryFile(suffix=".jpg").name, teaser='Teaser',
                            full_text='Full text')

    def test_edit_news_not_authorized_user_cannot_access(self):
        resp = self.client.get('/news/1/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=%2Fnews%2F1/')

    def test_edit_news_url_exists_at_desired_location(self):
        self.client.login(email='test@test.com', password='123qwe321')
        resp = self.client.get('/news/1/')
        self.assertEqual(resp.status_code, 200)

    def test_edit_news_url_accessible_by_name(self):
        self.client.login(email='test@test.com', password='123qwe321')
        resp = self.client.get(reverse('main:edit_news', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)

    def test_edit_news_uses_correct_template(self):
        self.client.login(email='test@test.com', password='123qwe321')
        resp = self.client.get('/news/1/')
        self.assertTemplateUsed(resp, 'main/news.html')

    def test_edit_news_authorized_user_c_cannot_access(self):
        self.client.login(email='test2@test.com', password='123qwe321')
        resp = self.client.get('/news/1/')
        self.assertEqual(resp.status_code, 404)

    def test_edit_news_can_edit_entry(self):
        with open('main/tests/test_img/test.png', 'rb') as file:
            data = {'author': 1, 'header': 'New Header', 'sub_header': 'New Sub header', 'image': file,
                    'teaser': 'New Teaser', 'full_text': 'New Full text'}
            self.client.login(email='test@test.com', password='123qwe321')
            resp = self.client.post('/news/1/', data)
            news = News.objects.get(id=1)
            os.remove(os.path.join(MEDIA_ROOT, 'test.png'))
            self.assertEqual(news.header, 'New Header')
            self.assertEqual(news.sub_header, 'New Sub header')
            self.assertEqual(news.teaser, 'New Teaser')
            self.assertEqual(news.full_text, 'New Full text')
            self.assertRedirects(resp, reverse('main:add_news'))

    def test_edit_news_authorized_user_cannot_edit_someone_elses_entry(self):
        with open('main/tests/test_img/test.png', 'rb') as file:
            data = {'author': 1, 'header': 'New Header', 'sub_header': 'New Sub header', 'image': file,
                    'teaser': 'New Teaser', 'full_text': 'New Full text'}
            self.client.login(email='test2@test.com', password='123qwe321')
            resp = self.client.post('/news/1/', data)
            self.assertEqual(resp.status_code, 404)

    def test_edit_news_not_authorized_user_cannot_edit_entry(self):
        with open('main/tests/test_img/test.png', 'rb') as file:
            data = {'author': 1, 'header': 'New Header', 'sub_header': 'New Sub header', 'image': file,
                    'teaser': 'New Teaser', 'full_text': 'New Full text'}
            resp = self.client.post('/news/1/', data)
            self.assertRedirects(resp, '/login/?next=%2Fnews%2F1/')


class DetailTest(TestCase):
    def setUp(self):
        User.objects.create(email='test@test.com', first_name='Ivan', last_name='Ivanov')
        News.objects.create(author=User.objects.get(id=1), header='Header', sub_header='Sub header',
                            image=tempfile.NamedTemporaryFile(suffix=".jpg").name, teaser='Teaser',
                            full_text='Full text')
        for _ in range(2):
            Comment.objects.create(news=News.objects.get(id=1), author=User.objects.get(id=1), text='Comment')
        for _ in range(2):
            Comment.objects.create(news=News.objects.get(id=1), comment=2, author=User.objects.get(id=1),
                                   text='Comment')
        for _ in range(2):
            Comment.objects.create(news=News.objects.get(id=1), comment=4, author=User.objects.get(id=1),
                                   text='Comment')
        self.data = {'news': 1, 'comment': 0, 'author': 'Anonymous', 'text': 'Some Text'}

    def test_detail_url_exists_at_desired_location(self):
        resp = self.client.get('/detail/1/')
        self.assertEqual(resp.status_code, 200)

    def test_detail_url_accessible_by_name(self):
        resp = self.client.get(reverse('main:detail', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)

    def test_detail_uses_correct_template(self):
        resp = self.client.get('/detail/1/')
        self.assertTemplateUsed(resp, 'main/detail.html')

    def test_detail_return_correct_data(self):
        resp = self.client.get('/detail/1/')
        news = News.objects.get(id=1)
        comments = [{'value': Comment.objects.get(id=1), 'comms_lvl2': []},
                    {'value': Comment.objects.get(id=2), 'comms_lvl2':
                        [{'value': Comment.objects.get(id=3), 'comms_lvl3': []},
                         {'value': Comment.objects.get(id=4), 'comms_lvl3': [Comment.objects.get(id=5),
                                                                             Comment.objects.get(id=6)]}]}]
        self.assertEqual(resp.context['news'], news)
        self.assertEqual(resp.context['comments'], comments)

    def test_detail_not_authorized_user_can_add_comment(self):
        self.client.post('/detail/1/', self.data)
        number_of_comments = News.objects.get(id=1).comment_set.count()
        self.assertEqual(number_of_comments, 7)

    def test_detail_authorized_user_can_add_comment(self):
        self.client.post('/detail/1/', self.data)
        number_of_comments = News.objects.get(id=1).comment_set.count()
        self.assertEqual(number_of_comments, 7)


class LoginTest(TestCase):
    def test_login_url_exists_at_desired_location(self):
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)

    def test_login_url_accessible_by_name(self):
        resp = self.client.get(reverse('main:login'))
        self.assertEqual(resp.status_code, 200)

    def test_login_uses_correct_template(self):
        resp = self.client.get('/login/')
        self.assertTemplateUsed(resp, 'registration/login.html')

    def test_login_can_login(self):
        user = User.objects.create(email='test@test.com', first_name='Ivan', last_name='Ivanov')
        user.set_password('123qwe321')
        user.save()
        data = {'username': 'test@test.com', 'password': '123qwe321'}
        resp = self.client.post('/login/', data)
        user = User.objects.get(id=1)
        self.assertEqual(resp.wsgi_request.user, user)
