from django.db import models


class Repository(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    url = models.URLField()

    # def append(self):
    #     new_id = self.id
    #     self.string_id = str(new_id) + '/commits'
    #     super(Repository, self).save()

    class Meta:
        verbose_name = "Репозиторий"
        verbose_name_plural = "Репозитории"

    def __str__(self):
        return self.title


class Commits(models.Model):
    title = models.CharField(max_length=255, db_index=True, null=True)
    message = models.TextField(db_index=True, null=True)
    timestamp = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Коммиты'
        verbose_name_plural = "Коммиты"

    def __str__(self):
        return self.title
