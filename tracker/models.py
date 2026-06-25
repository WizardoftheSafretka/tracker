from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from config import settings


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name="Пользователь",
        help_text="Введите пользователя"
    )
    place = models.CharField(max_length=255, verbose_name="Место", help_text="Введите место")
    time = models.TimeField(verbose_name="Время", help_text="Введите время")
    action = models.CharField(max_length=255, verbose_name="Действие", help_text="Введите действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Признак полезной привычки",
                                      help_text="Укажите признок полезной привычки")
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_to',
        verbose_name="Связанная привычка",
        help_text="Введите связанную привычку"
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность",
        help_text="Введите периодичность",
        validators=[MinValueValidator(1), MaxValueValidator(7)]
    )
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вознаграждение",
                              help_text="Введите вознаграждение")
    execution_time = models.PositiveIntegerField(verbose_name="Время на выполнение",
                                                 help_text="Введите время на выполнение")
    is_public = models.BooleanField(verbose_name="Признак публичности", default=False,
                                    help_text="Укажите признок публичности")

    def __str__(self):
        return f"{self.user} - {self.action}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
