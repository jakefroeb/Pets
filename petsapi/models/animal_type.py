from django.db import models

class Animal_Type(models.Model):
    name = models.CharField(max_length=50)
    actions = models.models.ManyToManyField("Action", related_name="animal_types")