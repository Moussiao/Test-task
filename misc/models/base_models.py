from django.db import models


class TimeBaseModel(models.Model):
    """Базовая модель, которая содержит в себе поля с датой создания и датой обновления записи"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
