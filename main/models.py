from django.db import models
from django.utils.translation import get_language, gettext_lazy as _


class Vacancy(models.Model):
    FULL_TIME = "full_time"
    SHIFT = "shift"
    PART_TIME = "part_time"
    INTERNSHIP = "internship"

    EMPLOYMENT_TYPE_CHOICES = [
        (FULL_TIME, _("Полная занятость")),
        (SHIFT, _("Сменный график")),
        (PART_TIME, _("Частичная занятость")),
        (INTERNSHIP, _("Стажировка")),
    ]

    title = models.CharField(_("Название вакансии (RU)"), max_length=200)
    title_en = models.CharField(_("Название вакансии (EN)"), max_length=200, blank=True)
    department = models.CharField(_("Подразделение (RU)"), max_length=160)
    department_en = models.CharField(_("Подразделение (EN)"), max_length=160, blank=True)
    location = models.CharField(_("Локация (RU)"), max_length=160, blank=True)
    location_en = models.CharField(_("Локация (EN)"), max_length=160, blank=True)
    employment_type = models.CharField(
        _("Формат работы"),
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default=FULL_TIME,
    )
    summary = models.TextField(_("Краткое описание (RU)"))
    summary_en = models.TextField(_("Краткое описание (EN)"), blank=True)
    requirements = models.TextField(
        _("Требования (RU)"),
        help_text=_("Укажите каждый пункт с новой строки."),
    )
    requirements_en = models.TextField(
        _("Требования (EN)"),
        blank=True,
        help_text=_("Укажите каждый пункт с новой строки."),
    )
    is_active = models.BooleanField(_("Показывать на сайте"), default=True)
    display_order = models.PositiveIntegerField(_("Порядок"), default=0)
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    class Meta:
        ordering = ["display_order", "-created_at", "title"]
        verbose_name = _("Вакансия")
        verbose_name_plural = _("Вакансии")

    def __str__(self):
        return self.title

    def _is_english(self):
        language = (get_language() or "ru").lower()
        return language.startswith("en")

    def _localized_value(self, ru_value, en_value):
        if self._is_english() and en_value:
            return en_value
        return ru_value

    @property
    def localized_title(self):
        return self._localized_value(self.title, self.title_en)

    @property
    def localized_department(self):
        return self._localized_value(self.department, self.department_en)

    @property
    def localized_location(self):
        return self._localized_value(self.location, self.location_en)

    @property
    def localized_summary(self):
        return self._localized_value(self.summary, self.summary_en)

    @property
    def localized_requirements(self):
        return self._localized_value(self.requirements, self.requirements_en)

    @property
    def requirements_list(self):
        return [line.strip() for line in self.requirements.splitlines() if line.strip()]

    @property
    def localized_requirements_list(self):
        return [line.strip() for line in self.localized_requirements.splitlines() if line.strip()]
