from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    animal_type = models.ForeignKey("Animal_Type", on_delete=models.CASCADE)