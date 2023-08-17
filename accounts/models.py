from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True)  

    def __str__(self):
        return self.email  
    
    def save(self, *args, **kwargs):
        self.username = self.cpf
        super(CustomUser, self).save(*args, **kwargs)


