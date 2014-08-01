from django.db import models


class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(max_length=200)
    list = models.ForeignKey(List)
