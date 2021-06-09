from django.db import models

class Pet_Action(models.Model):
    pet = models.ForeignKey("Pet", on_delete=models.CASCADE)
    action = models.ForeignKey("Action", on_delete=models.CASCADE)
    action_date = models.DateTimeField(auto_now_add=True)