from django.test import TestCase, Client

# Create your tests here.
class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.token = 'z0000'

    def DeviceTest(self):
        request=self.client.get(path='api/experiments/', 
                                headers={'Device-Token':self.token})
        self.assertEqual(request.status_code, 200, msg='Запрос некорректный')
        for i in range(10):
            r = self.client.get(path='api/experiments/', 
                                headers={'Device-Token':self.token})
            self.assertEqual(request.content, r.content, msg='Данные опыта изменились')

    def DistributionTest(self):
        N=[0]*3
        for i in range(600):
            token = str(i)
            request = self.client.get(path='api/experiments/', 
                                      headers={'Device-Token':token})
            self.assertEqual(request.status_code, 200, msg='Запрос некорректный')
            for a in request.context:
                if a["key"] == 'button_color':
                    print('da')
        self.assertTrue("2")

    def tearDown(self):
        print("tearDown")