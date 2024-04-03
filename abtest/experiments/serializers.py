from rest_framework import serializers
from .models import (
    Experiment,
    Option,
    Option_of_Device,
    Device
    )


class ExperimentSerializer(serializers.ModelSerializer):
    key = serializers.ReadOnlyField(source = 'experiment.key')
    value = serializers.ReadOnlyField(source = 'option.value')

    class Meta:
        model = Option_of_Device
        fields = ('id', 'key', 'value')
