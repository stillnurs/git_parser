from django.db import models


class Repository(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    url = models.URLField()

    class Meta:
        verbose_name = "Репозиторий"
        verbose_name_plural = "Репозитории"

    def __str__(self):
        return str(self.title)


class Commits(models.Model):
    title = models.CharField(max_length=255, db_index=True, null=True)
    message = models.TextField(db_index=True, null=True)
    timestamp = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'коммиты'
        verbose_name_plural = "коммиты"

    def __str__(self):
        return str(self.title)
