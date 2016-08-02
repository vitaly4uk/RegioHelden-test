from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from rhusers.forms import UserUpdateForm
from rhusers.models import IBANProfile


class RHTestCase(TestCase):

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser('admin_user', 'admin@regiohelden.com', 'qwerty100')
        self.admin_user.profile

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertTrue('users' in response.context)

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'<a href="/login/">' in response.content)

        self.assertTrue(self.client.login(username='admin_user', password='qwerty100'))
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'<a href="/create/">' in response.content)

    def test_create_redirect(self):
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/create/')

        self.assertTrue(self.client.login(username='admin_user', password='qwerty100'))
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_create_user_form(self):
        form = UserUpdateForm({}, user=self.admin_user)
        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {
            'bban': ['This field is required.'],
            'check_digits': ['This field is required.'],
            'country_code': ['This field is required.'],
            'username': ['This field is required.']})

        form = UserUpdateForm({'bban': '23e23e-32e32', 'check_digits': '123', 'country_code': 'fg', 'username': '1qaz'},
                              user=self.admin_user)
        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {
            'bban': ['Enter a valid value.'],
            'check_digits': ['Ensure this value is less than or equal to 99.'],
            'country_code': ['Incorrect country code']})

        form = UserUpdateForm({'bban': '12qw23we', 'check_digits': '23', 'country_code': 'ua', 'username': 'user'},
                              user=self.admin_user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(form.instance.profile.created_by, self.admin_user)

    def test_profile_autocreate(self):
        user1 = get_user_model().objects.create_user('user1', 'user1@regiohelden.com', 'qwerty100')
        self.assertEqual(IBANProfile.objects.filter(user=user1).count(), 1)
        user2 = get_user_model().objects.create_user('user2', 'user2@regiohelden.com', 'qwerty100')
        self.assertEqual(IBANProfile.objects.filter(user=user2).count(), 1)

    def test_update_user_form(self):
        user1 = get_user_model().objects.create_user('user1', 'user1@regiohelden.com', 'qwerty100')
        form = UserUpdateForm({'bban': '12qw23we', 'check_digits': '23', 'country_code': 'ua', 'username': 'user'},
                              user=self.admin_user, instance=user1)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(form.instance, user1)
        self.assertEqual(form.instance.profile.bban, '12qw23we')
        self.assertEqual(form.instance.profile.created_by, self.admin_user)

    def test_edit_user(self):
        user1 = get_user_model().objects.create_user('user1', 'user1@regiohelden.com', 'qwerty100')
        user1.profile.created_by = self.admin_user
        user1.profile.save()
        user2 = get_user_model().objects.create_user('user2', 'user2@regiohelden.com', 'qwerty100')
        user2.profile.created_by = user1
        user2.profile.save()

        self.assertTrue(self.client.login(username='admin_user', password='qwerty100'))
        response = self.client.get('/{0}/edit/'.format(user1.pk))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/{0}/edit/'.format(user2.pk))
        self.assertEqual(response.status_code, 404)