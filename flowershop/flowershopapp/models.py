from django.db import models


class User(models.Model):
    name = models.CharField(
        'Имя пользователя',
        max_length=200,
        db_index=True
    )
    phoneNumber = models.CharField(
        'Номер телефона пользователя',
        unique=True,
        null=False,
        blank=False
    )
    def __str__(self):
        return self.full_name
