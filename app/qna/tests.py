from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from django.contrib.auth.models import User

from qna.views import QuestionDashboardView, QuestionListView, QuestionSearchView
from profiles.models import Profile
from mindspace.models import *
from qna.models import *

# Create your tests here.
class TestQnAViews(TestCase):
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
        self.resource_1 = Resource.objects.create(
            owner=self.profile_1,
            title='TestResource',
            description='TestResource1',
            belongs_to=self.mindspace_1,
            res_format='Quote',
            quote='TestQuote1'
        )
        self.mindspace_2 = Mindspace.objects.create(
            owner=self.profile_2,
            title='TestMindspace2',
            description='TestMindspace2'
        )
        self.resource_2 = Resource.objects.create(
            owner=self.profile_2,
            title='TestResource2',
            description='TestResource1',
            belongs_to=self.mindspace_2,
            res_format='Quote',
            quote='TestQuote2'
        )

    def test_question_create_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('qna:question_create'), data={
            'owner': self.profile_1,
            'title': 'TestQuestion',
            'body': 'TestQuestion'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        question = Question.objects.last()
        self.assertEqual(question.title, 'TestQuestion')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['nextURL'], reverse('qna:question_detail', kwargs={'id': question.id}))

    def test_load_resources_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.get(reverse('qna:ajax_load_resources'), data={
            'mindspace': self.mindspace_1,
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTemplateUsed(response, 'qna/resource_dropdown_list_options.html')
        self.assertEqual(response.status_code, 200)

    def test_question_update_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('qna:question_create'), data={
            'owner': self.profile_1,
            'title': 'TestQuestion',
            'body': 'TestQuestion'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        question = Question.objects.last()

        response = self.client.post(reverse('qna:question_update', kwargs={'id': question.id}), data={
            'title': 'TestQuestionUpdated',
            'body': 'TestQuestion'
        })

        question.refresh_from_db()
        
        self.assertEqual(question.title, 'TestQuestionUpdated')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('qna:question_detail', kwargs={'id': question.id}))

    def test_question_delete_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('qna:question_create'), data={
            'owner': self.profile_1,
            'title': 'TestQuestion',
            'body': 'TestQuestion'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        question = Question.objects.last()

        response = self.client.post(reverse('qna:question_delete', kwargs={'id': question.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('qna:question_list'))

    def test_question_detail_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('qna:question_create'), data={
            'owner': self.profile_1,
            'title': 'TestQuestion',
            'body': 'TestQuestion'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        question = Question.objects.last()

        response = self.client.get(reverse('qna:question_detail', kwargs={'id': question.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qna/question_detail.html')

    def test_question_dashboard_view(self):
        request = self.factory.get(reverse('qna:question_list'))
        request.user = self.user_1
        view = QuestionDashboardView()
        view.setup(request)
        view.context = view.get_context_data()
        self.assertIn('form_create', view.context)
        self.assertIn('form_search', view.context)
        self.assertEqual(view.template_name, 'qna/question_dashboard.html')

    def test_question_list_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('qna:question_create'), data={
            'owner': self.profile_1,
            'title': 'TestQuestion',
            'body': 'TestQuestion'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        request = self.factory.get(reverse('qna:ajax_load_question_lists'), data={
            'my-questions-page': 1
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        request.user = self.user_1
        view = QuestionListView()
        view.setup(request)
        view.context = view.get_context_data()
        self.assertIn('is_viewing', view.context)
        self.assertIn('page_obj', view.context)
        self.assertIn('is_paginated', view.context)
        self.assertEqual(len(view.context['page_obj'].object_list), 1)
        self.assertEqual(view.template_name, 'qna/question_list.html')

    def test_question_search_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('qna:question_create'), data={
            'owner': self.profile_1,
            'title': 'TestQuestion',
            'body': 'TestQuestion'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.post(reverse('qna:question_create'), data={
            'owner': self.profile_1,
            'title': 'Question',
            'body': 'Question'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        request = self.factory.get(reverse('qna:question_search'), data={
            'keyword': 'Test'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user_1
        view = QuestionSearchView()
        view.setup(request)
        view.object_list = view.get_queryset()
        self.assertEqual(len(view.object_list), 1)

    def test_answer_create_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('qna:question_create'), data={
            'owner': self.profile_1,
            'title': 'TestQuestion',
            'body': 'TestQuestion'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        question = Question.objects.last()

        response = self.client.post(reverse('qna:answer_create', kwargs={'q_id': question.id}), data={
            'owner': self.profile_1,
            'question': question,
            'reply': 'TestAnswer',
        })

        answer = question.answers.all()[0]
        self.assertEqual(answer.reply, 'TestAnswer')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('qna:question_detail', kwargs={'id': question.id}))

    def test_answer_update_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('qna:question_create'), data={
            'owner': self.profile_1,
            'title': 'TestQuestion',
            'body': 'TestQuestion'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        question = Question.objects.last()

        response = self.client.post(reverse('qna:answer_create', kwargs={'q_id': question.id}), data={
            'owner': self.profile_1,
            'question': question,
            'reply': 'TestAnswer',
        })

        answer = question.answers.all()[0]

        response = self.client.post(reverse('qna:answer_update', kwargs={'q_id': question.id, 'id': answer.id}), data={
            'owner': self.profile_1,
            'question': question,
            'reply': 'TestAnswerUpdated',
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        answer.refresh_from_db()

        self.assertEqual(answer.reply, 'TestAnswerUpdated')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('qna:question_detail', kwargs={'id': question.id}))

    def test_answer_delete_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('qna:question_create'), data={
            'owner': self.profile_1,
            'title': 'TestQuestion',
            'body': 'TestQuestion'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        question = Question.objects.last()

        response = self.client.post(reverse('qna:answer_create', kwargs={'q_id': question.id}), data={
            'owner': self.profile_1,
            'question': question,
            'reply': 'TestAnswer',
        })

        answer = question.answers.all()[0]

        response = self.client.post(reverse('qna:answer_delete', kwargs={
            'q_id': question.id,
            'id': answer.id
        }))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('qna:question_detail', kwargs={'id': question.id}))

    def test_answer_vote_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('qna:question_create'), data={
            'owner': self.profile_1,
            'title': 'TestQuestion',
            'body': 'TestQuestion'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        question = Question.objects.last()

        response = self.client.post(reverse('qna:answer_create', kwargs={'q_id': question.id}), data={
            'owner': self.profile_1,
            'question': question,
            'reply': 'TestAnswer',
        })

        answer = question.answers.all()[0]

        response = self.client.post(reverse('qna:answer_vote'), data={
            'vote_type': 'U',
            'answer_id': answer.id
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['nature'], 'create')
        self.assertEqual(response.json()['vote'], 'U')