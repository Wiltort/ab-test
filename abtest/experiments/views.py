from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, mixins, status
from .serializers import ExperimentSerializer
from .models import Experiment, Device, Option_of_Device, Option
from rest_framework.response import Response
from random import random


class RubricViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Option_of_Device.objects.all()
    serializer_class = ExperimentSerializer
    
    def get_queryset(self):
        token = self.request.headers('Device-Token')
        if not token: 
            return None
        device, created = Device.objects.get_or_create(Token=token)
        if created:
            experiments = Experiment.objects.all()
            for exp in experiments:
                x = random()
                s = 0
                for opt in exp.options.all():
                    s += opt.probability
                    if x*100 <= s or s >= 100:
                        Option_of_Device.objects.create(
                            device=device, 
                            experiment=exp, 
                            option=opt
                        )
                        break
        queryset = Option_of_Device.objects.filter(device=device)
        return queryset
