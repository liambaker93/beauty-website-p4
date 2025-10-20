from django.db import models

# Create your models here.


class InformationRequest(models.Model):
    """
    Generates a form for the user to send to the site owner
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"Info request from {self.name}"
