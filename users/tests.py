from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.factories import UserExtendedFactory
from utils.test_admin import get_admin_list_view_url, get_admin_change_view_url, TestAdmin


class UsersAdminTest(TestAdmin):
    """Тест приложения Users для админки"""
    def setUp(self) -> None:
        super().setUp()

    def test_change_view_loads_normally_for_users_add(self):
        """Проверка доступа на страницу просмотра/редактирования экземпляра модели в админке"""

        # логинимся под суперпользователем
        self.client.login(email=self.super_user.email, password=self.password)

        response = self.client.get(get_admin_change_view_url(self.super_user))
        self.assertEqual(response.status_code, 200)

    def test_list_view_loads_normally_for_users_add(self):
        """Проверка доступа на страницу списка экземпляров модели в админке"""

        # логинимся под суперпользователем
        self.client.login(email=self.super_user.email, password=self.password)

        response = self.client.get(get_admin_list_view_url(self.super_user))
        self.assertEqual(response.status_code, 200)


class TokenObtainPairViewTestCase(APITestCase):

    def setUp(self):
        self.password = 'StrongPassword123'
        self.user = UserExtendedFactory(
            username='test_user',
            email='test@example.com',
            password=self.password
        )
        self.url = reverse('token_obtain_pair')

    def test_login_success(self):
        """ Вход с корректными данными """
        response = self.client.post(self.url, {'email': self.user.email, 'password': self.password}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], self.user.email,)

    def test_login_invalid_password(self):
        """ Вход с неверным паролем """
        response = self.client.post(self.url, {'email': self.user.email, 'password': 'wrong-password'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)

    def test_login_unknown_email(self):
        """ Вход с несуществующим пользователем """
        response = self.client.post(
            self.url, {'email': 'unknown@example.com', 'password': self.password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_without_password(self):
        """ Вход без пароля """
        response = self.client.post(self.url, {'email': self.user.email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_without_email(self):
        """ Вход без email """
        response = self.client.post(self.url, {'password': self.password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutViewTestCase(APITestCase):

    def setUp(self):
        self.password = 'StrongPassword123'

        self.user = UserExtendedFactory(
            username='test_user',
            email='test@example.com',
            password=self.password
        )

        token_response = self.client.post(
            reverse('token_obtain_pair'),
            {'email': self.user.email, 'password': self.password},
            format='json'
        )

        self.access = token_response.data['access']
        self.refresh = token_response.data['refresh']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')

    def test_logout_success(self):
        response = self.client.post(reverse('logout'), {'refresh': self.refresh}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Successfully logged out.')

    def test_logout_without_refresh_token(self):
        response = self.client.post(reverse('logout'), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_invalid_refresh_token(self):
        response = self.client.post(reverse('logout'),  {'refresh': 'invalid-token'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
