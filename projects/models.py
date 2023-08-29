from django.db import models
from PIL import Image
from django.contrib.auth import get_user_model

class Project(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project_id = models.IntegerField(blank=True)
    name = models.CharField(max_length=255)
    cover_photo = models.ImageField(upload_to='project/cover/%Y/%m/%d/')
    description = models.TextField(max_length=600, blank=True)
    status = models.BooleanField(default=True)
    composite_pk = models.CharField(max_length=255, unique=True, primary_key=True)
    members = models.ManyToManyField(get_user_model(), related_name='projects', blank=True)

    def save(self, *args, **kwargs):
        cpf = self.owner.cpf.replace('-', '')
        cpf = cpf.replace('.', '')
        self.composite_pk = f"{cpf}-{self.project_id}"
        super().save(*args, **kwargs)

        if self.cover_photo:
            img = Image.open(self.cover_photo.path)
            target_width = 1600 
            target_height = 900  
            
            img.thumbnail((target_width, target_height))
            img.save(self.cover_photo.path, quality=85)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    post_id = models.IntegerField()
    autor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = models.TextField(max_length=600, blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    composite_pk = models.CharField(max_length=255, unique=True, primary_key=True)

    def save(self, *args, **kwargs):
        project = self.project.composite_pk
        autor = self.autor.cpf.replace('-', '')
        autor = autor.replace('.', '')
        self.composite_pk = f"{project}-{autor}-{self.post_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text
    
class Comment(models.Model):
    comment_id = models.IntegerField()
    autor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=600, blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    composite_pk = models.CharField(max_length=255, unique=True, primary_key=True)

    def save(self, *args, **kwargs):
        post = self.post.composite_pk
        autor = self.autor.cpf.replace('-', '')
        autor = autor.replace('.', '')
        self.composite_pk = f"{post}-{autor}-{self.comment_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text

