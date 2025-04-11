from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, null=False)

class Website(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=800)
    description = models.TextField()
    content = models.TextField(max_length=2000)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)


class User(models.Model):
    visited_website = models.ManyToManyField(Website)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    avatar = models.SlugField(max_length=255)
