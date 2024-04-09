from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, APIClient

# Create your tests here.
class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.token = 'z0000'
        self.factory = APIRequestFactory()

    def test_device(self):
        res=self.client.get(path='/api/experiments/', 
                                headers={'Device-Token': self.token,})
        self.assertEqual(res.status_code, 200, msg='Запрос некорректный')
        print(self.token)
        for i in range(10):
            r = self.client.get(path='/api/experiments/', 
                                headers={'Device-Token': self.token,})
            self.assertEqual(res.content, r.content, msg='Данные опыта изменились')
            print(res.request)

    def test_distribution(self):
        N=[0]*3
        for i in range(600):
            token = str(i)
            request = self.client.get(path='/api/experiments/', 
                                      headers={'Device-Token':token})
            self.assertEqual(request.status_code, 200, msg='Запрос некорректный')
            

    def tearDown(self):
        print("tearDown")