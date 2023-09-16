from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True, primary_key=True)

    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True, blank=True, default='')  
    city = models.CharField(max_length=50, blank=True, default='')
    state = models.CharField(max_length=50, blank=True, default='')
    country = models.CharField(max_length=50, blank=True, default='')
    zipcode = models.CharField(max_length=50, blank=True, default='')
    birth_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    profile_picture = models.ImageField(upload_to='user/profile/%Y/%m/%d/', null=True, blank=True)

    categories = models.ManyToManyField(Category, related_name='user_categories', blank=True)



    def __str__(self):
        return self.email  
    
    def save(self, *args, **kwargs):
        if self.cpf:
            self.username = self.cpf
        super(CustomUser, self).save(*args, **kwargs)

        if self.profile_picture:
            img = Image.open(self.profile_picture.path)

            min_dim = min(img.width, img.height)
            left = (img.width - min_dim) // 2
            top = (img.height - min_dim) // 2
            right = (img.width + min_dim) // 2
            bottom = (img.height + min_dim) // 2

            img = img.crop((left, top, right, bottom))

            new_size = (200, 200) 
            img = img.resize(new_size, Image.LANCZOS)

            img.save(self.profile_picture.path)


class Review(models.Model):
    review_id = models.UUIDField(auto_created=True, primary_key=True, unique=True)
    review_body = models.TextField(max_length=200)
    review_value = models.ValueRange(1,5)
    created_at = models.DateTimeField(auto_now=True)

    reviewed_user = models.ForeignKey(CustomUser, related_name='reviwed_user', on_delete=models.CASCADE)
    author_user = models.ForeignKey(CustomUser, related_name='author_user', on_delete=models.CASCADE)

    # TODO Criar chave estrangeira do projeto
    # TODO Faz sentido manter um id pra review ou utilizar reviewed_user + author_user + project_id + inteiro iterativo?

    def __str__(self):
        return self.review_id