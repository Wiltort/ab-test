from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from .serializers import ExperimentSerializer
from .models import Experiment, Device, Option_of_Device
from rest_framework.response import Response
from random import random, seed


class ExperimentViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Option_of_Device.objects.all()
    serializer_class = ExperimentSerializer

    def get_queryset(self):
        if 'Device-Token' not in self.request.headers:
            return None
        token = self.request.headers['Device-Token']
        device, created = Device.objects.get_or_create(Token=token)
        if created:
            experiments = Experiment.objects.all()
            for exp in experiments:
                seed()
                x = random()
                s = 0
                for opt in exp.options.all():
                    s += opt.probability
                    if x * 100 <= s or s >= 100:
                        Option_of_Device.objects.create(
                            device=device,
                            experiment=exp,
                            option=opt
                        )
                        break
        queryset = Option_of_Device.objects.filter(device=device)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if 'Device-Token' not in request.headers:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


def index(request):
    devices = Device.objects.all().count()
    experiments = Experiment.objects.all()
    statistic_data = {}
    options = Option_of_Device.objects.all()
    for exp in experiments:
        statistic_data[exp.key] = {}
    for opt in options:
        statistic_data[opt.experiment.key][opt.option.value] = (
            statistic_data[opt.experiment.key].get(opt.option.value, 0) + 1
        )
    return render(
        request,
        "index.html",
        {
            "devices": devices,
            "experiments": experiments,
            "statistic_data": statistic_data
        }
    )
