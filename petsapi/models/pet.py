from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from datetime import timedelta

class Pet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    animal_type = models.ForeignKey("Animal_Type", on_delete=models.CASCADE)
    actions = models.ManyToManyField("Action", through='Pet_Action')

    @property
    def happiness(self):
        minutes = timedelta(hours=1, minutes= 40)
        pet_acts = self.pet_action_set.filter(action_date__gte= datetime.now() - minutes)
        happiness = 0 
        for pet_act in pet_acts:
            happiness += 5
        return happiness
    
    @property
    def image_url(self):
        if self.happiness >= 50:
            return "http://localhost:8000/media/dog_images/happy-dog.jpeg"
        else:
            return "http://localhost:8000/media/dog_images/sad-dog.jpeg"