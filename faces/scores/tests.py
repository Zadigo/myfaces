import json

from django.urls import reverse
from rest_framework.test import APITestCase
from scores.models import UserDetail
from scores.utils import session_creator


class TestFacesApi(APITestCase):
    fixtures = ['user_details']

    @classmethod
    def setUpTestData(cls):
        cls.fake_session = 'sess_123'
        cls.session_id = session_creator()
        cls.user_detail = UserDetail.objects.create(**{
            'session': cls.session_id,
            'country': 'France',
            'date_of_birth': '2000-1-1',
            # 'zodiac_sign': 'Libra',
            'ethnicity': 'Black',
            'gender': 'Man'
        })

    def test_list_faces(self):
        path = reverse('scores_api:list_all_faces')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_list_random_faces(self):
        path = reverse('scores_api:list_random_faces')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_list_emotions(self):
        path = reverse('scores_api:list_emotions')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertIn('count', response.json())
        self.assertIn('positive', response.json())
        self.assertIn('negative', response.json())

    def test_submit_scores(self):
        path = reverse('scores_api:submit_scores')
        data = json.dumps({
            'session': self.user_detail.session,
            'scores': []
        })
        response = self.client.post(
            path,
            content_type='application/json',
            data=data
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('count', response.json())

    def test_new_session(self):
        path = reverse('scores_api:new_session')
        response = self.client.post(path, data={
            'country': 'France',
            'date_of_birth': '2000-1-1'
        })
        self.assertIn('session', response.json())
