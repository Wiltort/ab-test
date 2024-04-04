import csv
import logging
import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from experiments.models import Experiment, Option

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
    filemode='w',
)

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'Load data from csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('filename', default='data.csv', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        try:
            with open(
                os.path.join(DATA_ROOT, options['filename']),
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
            raise CommandError('Добавьте файл rings в директорию data')
        logging.info('Successfully loaded all data into database')