from django.db import models
from django.db.models import F
from django.db.models.functions import Concat


class Repository(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()

    def append(self):
        new_id = self.id
        self.string_id = str(new_id) + '/commits'
        super(Repository, self).save()

    class Meta:
        verbose_name = "Репозиторий"
        verbose_name_plural = "Репозитории"

    def __str__(self):
        return self.title


class Commits(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Коммиты'
        verbose_name_plural = "Коммиты"

    def __str__(self):
        return self.title
