from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True, primary_key=True)

    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True)  
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)
    birth_date = models.DateField(auto_now=False, auto_now_add=False)

    profile_picture = models.ImageField(upload_to='user/profile/%Y/%m/%d/')

    categories = models.ManyToManyField(Category, related_name='user_categories')



    def __str__(self):
        return self.email  
    
    def save(self, *args, **kwargs):
        self.username = self.cpf
        super(CustomUser, self).save(*args, **kwargs)

