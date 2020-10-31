from django.db import models


class Repository(models.Model):
    url = models.URLField()
