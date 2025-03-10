from django.db import models

# Create your models here.

class Tags(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=255, null=False, unique=True)


class Keywords(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=255, null=False, unique=True)
    tags = models.ManyToManyField(Tags)


class URL(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    url = models.CharField(max_length=200, null=False)
    official_name = models.CharField(max_length=255, null=True)
    keywords = models.ForeignKey(Keywords, on_delete=models.CASCADE)


class Text(models.Model):
    URL = models.ForeignKey(URL, primary_key=True, auto_created=True, on_delete=models.DO_NOTHING)
    keywords = models.ForeignKey(Keywords, on_delete=models.CASCADE)
    text = models.TextField()
    title = models.CharField(max_length=255)
