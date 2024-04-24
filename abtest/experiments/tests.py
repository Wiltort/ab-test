from django.test import TestCase, Client
import csv
import os
from django.conf import settings
from experiments.models import Experiment, Option


DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


# Create your tests here.
class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.tok = 'z0000'
        try:
            with open(
                os.path.join(DATA_ROOT, 'data.csv'),
                newline='',
                encoding='utf8'
            ) as csv_file:
                data = csv.reader(csv_file)
                for row in data:
                    k, pr, val = row
                    exp, created = Experiment.objects.get_or_create(key=k)
                    Option.objects.get_or_create(
                        value=val,
                        probability=pr,
                        experiment=exp
                    )
        except FileNotFoundError:
            raise ('Добавьте файл rings в директорию data')
                

    def test_device(self):
        res=self.client.get(
            '/api/experiments/',
            headers={'Device-Token': self.tok,},
            format='json')
        self.assertEqual(res.status_code, 200, msg='Запрос некорректный')
        for i in range(10):
            r = self.client.get(path='/api/experiments/', 
                                headers={'Device-Token': self.tok,})
            self.assertEqual(res.content, r.content, msg='Данные опыта изменились')
            

    def test_distribution(self):
        experiment_1 = {}
        experiment_2 = {}
        for i in range(1000):
            token = str(i)
            res = self.client.get(path='/api/experiments/', 
                                      headers={'Device-Token':token})
            self.assertEqual(res.status_code, 200, msg='Запрос некорректный')
            for item in res.data:
                if item["key"]=="button_color":
                    experiment_1[item["value"]] = experiment_1.get(item["value"],0)+1
                elif item["key"]=="price":
                    experiment_2[item["value"]] = experiment_2.get(item["value"],0)+1
        for v in experiment_1.values():
            self.assertLessEqual(
                abs(333-v), 
                33, 
                msg="отклонение в эксперименте №1 превышает допустимое"
                )
        for key, value in experiment_2.items():
            experiment,created = Experiment.objects.get_or_create(key='price')
            self.assertFalse(created)
            option, created = Option.objects.get_or_create(experiment=experiment, value=key)
            self.assertFalse(created)
            self.assertLessEqual(
                abs(int(option.probability)*10-value), 
                int(option.probability), 
                msg="отклонение в эксперименте №2 превышает допустимое"
                )
            