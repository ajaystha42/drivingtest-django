from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self) -> str:
        return "%s - %s" % (self.user_id, self.name)

    class Meta:
        db_table = 'users'
