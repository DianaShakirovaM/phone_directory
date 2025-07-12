from django.db import models


class Employee(models.Model):
    """Модель сотрудника организации."""

    name = models.CharField('ФИО/Организация', max_length=500)
    position = models.CharField('Должность', max_length=255, blank=True, null=True)
    department = models.CharField('Подразделение', max_length=255, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=12)
    room = models.CharField('Кабинет', max_length=20, blank=True, null=True)
    email = models.EmailField('Email', blank=True, null=True)
    creared_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name
