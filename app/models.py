# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Person(models.Model):
    SEXES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    first_name = models.CharField(max_length=30)
    savings_amount = models.IntegerField(default=0)
    chequing_amount = models.IntegerField(default=0)
    sex = models.CharField(max_length=1, choices=SEXES)
    age = models.IntegerField()

class Account(models.Model):
    person_id = models.ForeignKey(
        Person,
        on_delete=models.CASCADE)
    savings_amount = models.IntegerField()
    chequing_amount = models.IntegerField()


