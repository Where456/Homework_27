from django.db import models


class Ads(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=200)
    address = models.CharField(max_length=100)


class Categories(models.Model):
    name = models.CharField(max_length=100)
