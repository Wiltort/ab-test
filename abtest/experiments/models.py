from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Experiment(models.Model):
    key = models.CharField(max_lenght=250, verbose_name='Ключ')
    

class Option(models.Model):
    value = models.CharField(max_lenght=250, verbose_name='Название')


class Device(models.Model):
    Token = models.CharField(max_length=250)


class Option_of_Device(models.Model):
    device = models.ForeignKey(
        Device, 
        on_delete=models.CASCADE,
        related_name='options'
    )
    
    
    
