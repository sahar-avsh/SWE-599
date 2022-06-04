from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from django.contrib.auth.models import User

from mindspace.views import MindspaceListView, NoteListView, AjaxMindspaceSearch
from profiles.models import Profile
from mindspace.models import *

# Create your tests here.
class TestMindspaceViews(TestCase):
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
        self.mindspace_2 = Mindspace.objects.create(
            owner=self.profile_2,
            title='Test',
            description='Test'
        )

    def test_mindspace_create_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('mindspace:mindspace_create'), data={
            'title': 'Testing', 
            'description': 'Testing',
            'is_public': True
        })
        mindspace = Mindspace.objects.last()
        self.assertEqual(mindspace.title, 'Testing')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mindspace:mindspace_detail', kwargs={'id': mindspace.id}))

    def test_mindspace_update_form(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.get(reverse('mindspace:mindspace_update', kwargs={'id': self.mindspace_1.id}))
        self.assertTemplateUsed(response, 'mindspace/mindspace_update.html')

    def test_mindspace_update_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('mindspace:mindspace_update', kwargs={'id': self.mindspace_1.id}), data={
            'title': 'TestMindspaceUpdate', 
            'description': 'TestMindspaceUpdate',
            'is_public': True
        })

        self.mindspace_1.refresh_from_db()

        self.assertEqual(self.mindspace_1.title, 'TestMindspaceUpdate')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mindspace:mindspace_detail', kwargs={'id': self.mindspace_1.id}))

    def test_mindspace_delete_form(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.get(reverse('mindspace:mindspace_delete', kwargs={'id': self.mindspace_1.id}), **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertTemplateUsed(response, 'mindspace/mindspace_delete.html')

    def test_mindspace_delete_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('mindspace:mindspace_update', kwargs={'id': self.mindspace_1.id}))
        self.assertEqual(response.status_code, 200)

    def test_mindspace_share_form(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.get(reverse('mindspace:mindspace_share', kwargs={'id': self.mindspace_1.id}))
        self.assertTemplateUsed(response, 'mindspace/mindspace_share.html')

    def test_mindspace_detail_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.get(reverse('mindspace:mindspace_detail', kwargs={'id': self.mindspace_1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mindspace/mindspace_detail.html')

    def test_mindspace_list_view(self):
        request = self.factory.get(reverse('mindspace:ajax_load_mindspace_lists'), data={
            'my-mindspace-page': 1
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        request.user = self.user_1
        view = MindspaceListView()
        view.setup(request)
        view.context = view.get_context_data()
        self.assertIn('is_viewing', view.context)
        self.assertIn('page_obj', view.context)
        self.assertIn('is_paginated', view.context)
        self.assertEqual(len(view.context['page_obj'].object_list), 1)
        self.assertEqual(view.template_name, 'mindspace/mindspace_list.html')

    def test_mindspace_search_view(self):
        request = self.factory.get(reverse('mindspace:ajax_load_search_results'), data={
            'keyword_query': 'Test',
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        request.user = self.user_1
        view = AjaxMindspaceSearch()
        view.setup(request)
        view.object_list = view.get_queryset()
        view.context = view.get_context_data()

        self.assertEqual(len(view.object_list), 1)

        self.assertIn('page_obj', view.context)
        self.assertIn('is_paginated', view.context)
        self.assertIn('filter_flag', view.context)
        self.assertIn('keyword_query', view.context)
        self.assertEqual(view.template_name, 'mindspace/ajax_mindspace_results.html')

    def test_resource_create_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('mindspace:resource_create', kwargs={'ms_id': self.mindspace_1.id}), data={
            'belongs_to': self.mindspace_1,
            'title': 'TestResource', 
            'description': 'TestResource',
            'res_format': 'Quote',
            'quote': 'TestQuote'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(len(self.mindspace_1.resources.all()), 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mindspace:mindspace_detail', kwargs={'id': self.mindspace_1.id}))

    def test_resource_update_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('mindspace:resource_create', kwargs={'ms_id': self.mindspace_1.id}), data={
            'belongs_to': self.mindspace_1,
            'title': 'TestResource', 
            'description': 'TestResource',
            'res_format': 'Quote',
            'quote': 'TestQuote'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.post(reverse('mindspace:resource_update', kwargs={
            'ms_id': self.mindspace_1.id,
            'id': self.mindspace_1.resources.first().id
        }), data={
            'belongs_to': self.mindspace_1,
            'title': 'TestResourceUpdate', 
            'description': 'TestResource',
            'res_format': 'Quote',
            'quote': 'TestQuote'
        }, 
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.mindspace_1.resources.first().refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.mindspace_1.resources.first().title, 'TestResourceUpdate')

    def test_resource_delete_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('mindspace:resource_create', kwargs={'ms_id': self.mindspace_1.id}), data={
            'belongs_to': self.mindspace_1,
            'title': 'TestResource', 
            'description': 'TestResource',
            'res_format': 'Quote',
            'quote': 'TestQuote'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(len(self.mindspace_1.resources.all()), 1)

        response = self.client.post(reverse('mindspace:resource_delete', kwargs={
            'ms_id': self.mindspace_1.id,
            'id': self.mindspace_1.resources.first().id
        }))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mindspace:mindspace_detail', kwargs={'id': self.mindspace_1.id}))
        self.assertEqual(len(self.mindspace_1.resources.all()), 0)

    def test_resource_detail_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('mindspace:resource_create', kwargs={'ms_id': self.mindspace_1.id}), data={
            'belongs_to': self.mindspace_1,
            'title': 'TestResource', 
            'description': 'TestResource',
            'res_format': 'Quote',
            'quote': 'TestQuote'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.get(reverse('mindspace:resource_detail', kwargs={
            'ms_id': self.mindspace_1.id,
            'id': self.mindspace_1.resources.first().id
        }))
        self.assertEqual(response.status_code, 200)
        self.assertIn('notes', response.context)

    def test_note_create_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('mindspace:resource_create', kwargs={'ms_id': self.mindspace_1.id}), data={
            'belongs_to': self.mindspace_1,
            'title': 'TestResource', 
            'description': 'TestResource',
            'res_format': 'Quote',
            'quote': 'TestQuote'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.post(reverse('mindspace:note_create', kwargs={
            'ms_id': self.mindspace_1.id,
            'r_id': self.mindspace_1.resources.first().id
        }), data={
            'content': 'TestNote',
            'written_by': self.profile_1,
            'belongs_to': self.mindspace_1.resources.first()
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mindspace:resource_detail', kwargs={
            'ms_id': self.mindspace_1.id,
            'id': self.mindspace_1.resources.first().id
        }))
        self.assertEqual(len(self.mindspace_1.resources.first().notes.all()), 1)


    def test_note_update_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('mindspace:resource_create', kwargs={'ms_id': self.mindspace_1.id}), data={
            'belongs_to': self.mindspace_1,
            'title': 'TestResource', 
            'description': 'TestResource',
            'res_format': 'Quote',
            'quote': 'TestQuote'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.post(reverse('mindspace:note_create', kwargs={
            'ms_id': self.mindspace_1.id,
            'r_id': self.mindspace_1.resources.first().id
        }), data={
            'content': 'TestNote',
            'written_by': self.profile_1,
            'belongs_to': self.mindspace_1.resources.first()
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.post(reverse('mindspace:note_update', kwargs={
            'ms_id': self.mindspace_1.id,
            'r_id': self.mindspace_1.resources.first().id,
            'id': self.mindspace_1.resources.first().notes.first().id
        }), data={
            'content': 'TestNoteUpdated',
            'written_by': self.profile_1,
            'belongs_to': self.mindspace_1.resources.first()
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.mindspace_1.resources.first().notes.all()[0].refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mindspace:resource_detail', kwargs={
            'ms_id': self.mindspace_1.id,
            'id': self.mindspace_1.resources.first().id
        }))
        self.assertEqual(len(self.mindspace_1.resources.first().notes.all()), 1)
        self.assertEqual(self.mindspace_1.resources.first().notes.all()[0].content, 'TestNoteUpdated')

    def test_note_delete_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('mindspace:resource_create', kwargs={'ms_id': self.mindspace_1.id}), data={
            'belongs_to': self.mindspace_1,
            'title': 'TestResource', 
            'description': 'TestResource',
            'res_format': 'Quote',
            'quote': 'TestQuote'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.post(reverse('mindspace:note_create', kwargs={
            'ms_id': self.mindspace_1.id,
            'r_id': self.mindspace_1.resources.first().id
        }), data={
            'content': 'TestNote',
            'written_by': self.profile_1,
            'belongs_to': self.mindspace_1.resources.first()
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.post(reverse('mindspace:note_delete', kwargs={
            'ms_id': self.mindspace_1.id,
            'r_id': self.mindspace_1.resources.first().id,
            'id': self.mindspace_1.resources.first().notes.first().id
        }),
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mindspace:resource_detail', kwargs={
            'ms_id': self.mindspace_1.id,
            'id': self.mindspace_1.resources.first().id
        }))
        self.assertEqual(len(self.mindspace_1.resources.first().notes.all()), 0)

    def test_note_list_view(self):
        login = self.client.login(username='TestUser1', password='Test')
        response = self.client.post(reverse('mindspace:resource_create', kwargs={'ms_id': self.mindspace_1.id}), data={
            'belongs_to': self.mindspace_1,
            'title': 'TestResource', 
            'description': 'TestResource',
            'res_format': 'Quote',
            'quote': 'TestQuote'
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.post(reverse('mindspace:note_create', kwargs={
            'ms_id': self.mindspace_1.id,
            'r_id': self.mindspace_1.resources.first().id
        }), data={
            'content': 'TestNote',
            'written_by': self.profile_1,
            'belongs_to': self.mindspace_1.resources.first()
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        request = self.factory.get(reverse('mindspace:note_list', kwargs={
            'ms_id': self.mindspace_1.id,
            'r_id': self.mindspace_1.resources.first().id
        }), data={
            'resource': self.mindspace_1.resources.first().id
        },
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        request.user = self.user_1
        view = NoteListView()
        view.setup(request)
        view.object_list = view.get_queryset()
        self.assertEqual(1, len(view.object_list))

    def tearDown(self):
        return super().tearDown()