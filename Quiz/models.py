from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self) -> str:
        return "%s - %s - %s" % (self.id, self.username, self.email)

    class Meta:
        db_table = 'users'