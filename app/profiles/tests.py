from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from django.contrib.auth.models import User

from profiles.views import NotificationListView

from profiles.models import Profile
from mindspace.models import *
from qna.models import *

# Create your tests here.
class TestProfilesViews(TestCase):
    @classmethod
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user_1 = User.objects.create_user(username='TestUser1', password='Test')
        self.user_2 = User.objects.create_user(username='TestUser2', password='Test')
        self.profile_1 = Profile.objects.create(
            created_by=self.user_1,
            f_name='Test1',
            l_name='User1',
        )
        self.profile_2 = Profile.objects.create(
            created_by=self.user_2,
            f_name='Test2',
            l_name='User2',
        )
        self.mindspace_1 = Mindspace.objects.create(
            owner=self.profile_1,
            title='TestMindspace1',
            description='TestMindspace1'
        )

    def test_home_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.get(reverse('main_page'))
        self.assertTemplateUsed(response, 'profiles/home.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'profiles/user_login.html')

        response = self.client.post(reverse('login'), data={
            'username': 'TestUser1',
            'password': 'Test'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mindspace:mindspace_list'))

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'profiles/user_register.html')

        response = self.client.post(reverse('signup'), data={
            'first_name': 'Zahra',
            'last_name': 'Atrvash',
            'username': 'saharavsh',
            'email': 'saharavsh7192@gmail.com',
            'password1': 'SWE599-demo',
            'password2': 'SWE599-demo'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_profile_update_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.get(reverse('profiles:profile_update', kwargs={'id': self.profile_1.id}))
        self.assertTemplateUsed(response, 'profiles/profile_update.html')

        response = self.client.post(reverse('profiles:profile_update', kwargs={'id': self.profile_1.id}), data={
            'f_name': 'Test1Updated',
            'l_name': 'User1Updated',
            'company': 'TestCompany',
            'bio': 'TestBio'
        })

        self.profile_1.refresh_from_db()

        self.assertEqual(response.json()['update'], 'done')
        self.assertEqual(self.profile_1.f_name, 'Test1Updated')
        self.assertEqual(self.profile_1.l_name, 'User1Updated')
        self.assertEqual(self.profile_1.company, 'TestCompany')
        self.assertEqual(self.profile_1.bio, 'TestBio')

    def test_profile_detail_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.get(reverse('profiles:profile_detail', kwargs={'id': self.profile_1.id}))
        self.assertTemplateUsed(response, 'profiles/profile_detail.html')

    def test_notification_view(self):
        sm = ShareMindspace.objects.create(
            mindspace=self.mindspace_1,
            access_level=ShareMindspace.editor,
            shared_by=self.profile_1,
            shared_with_info='TestUser2',
            shared_with=self.profile_2
        )
        
        request = self.factory.get(reverse('profiles:profile_notifications', kwargs={'id': self.profile_2.id}))
        request.user = self.user_2
        view = NotificationListView()
        view.setup(request)
        view.object_list = view.get_queryset()
        self.assertEqual(len(view.object_list), 1)

    def tearDown(self):
        return super().tearDown()    