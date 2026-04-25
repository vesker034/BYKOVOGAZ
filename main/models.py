from django.db import models


class Vacancy(models.Model):
    FULL_TIME = "full_time"
    SHIFT = "shift"
    PART_TIME = "part_time"
    INTERNSHIP = "internship"

    EMPLOYMENT_TYPE_CHOICES = [
        (FULL_TIME, "Полная занятость"),
        (SHIFT, "Сменный график"),
        (PART_TIME, "Частичная занятость"),
        (INTERNSHIP, "Стажировка"),
    ]

    title = models.CharField("Название вакансии", max_length=200)
    department = models.CharField("Подразделение", max_length=160)
    location = models.CharField("Локация", max_length=160, blank=True)
    employment_type = models.CharField(
        "Формат работы",
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default=FULL_TIME,
    )
    summary = models.TextField("Краткое описание")
    requirements = models.TextField(
        "Требования",
        help_text="Укажите каждый пункт с новой строки.",
    )
    is_active = models.BooleanField("Показывать на сайте", default=True)
    display_order = models.PositiveIntegerField("Порядок", default=0)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ["display_order", "-created_at", "title"]
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.title

    @property
    def requirements_list(self):
        return [line.strip() for line in self.requirements.splitlines() if line.strip()]
