from django.contrib.auth.models import User
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


class Role(models.Model):
    """Справочник ролей (связь с пользователями через user_roles)."""

    name = models.CharField(_("Название"), max_length=120, unique=True)

    class Meta:
        verbose_name = _("Роль")
        verbose_name_plural = _("Роли")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
        related_name="role_links",
    )
    role = models.ForeignKey(Role, verbose_name=_("Роль"), on_delete=models.CASCADE, related_name="user_links")

    class Meta:
        verbose_name = _("Роль пользователя")
        verbose_name_plural = _("Роли пользователей")
        constraints = [
            models.UniqueConstraint(fields=["user", "role"], name="main_userrole_user_role_uniq"),
        ]

    def __str__(self) -> str:
        return f"{self.user.username} — {self.role.name}"


class Department(models.Model):
    """Подразделение (родительское для членов команды)."""

    name = models.CharField(_("Название"), max_length=200)

    class Meta:
        verbose_name = _("Подразделение")
        verbose_name_plural = _("Подразделения")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class SocialLink(models.Model):
    """Типы социальных ссылок (справочник)."""

    name = models.CharField(_("Название"), max_length=120)
    base_url = models.URLField(_("Базовый URL"), max_length=500, blank=True)

    class Meta:
        verbose_name = _("Соц. канал")
        verbose_name_plural = _("Соц. каналы")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class TeamMember(models.Model):
    department = models.ForeignKey(
        Department,
        verbose_name=_("Подразделение"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
    )
    first_name = models.CharField(_("Имя"), max_length=80)
    last_name = models.CharField(_("Фамилия"), max_length=80)
    position = models.CharField(_("Должность"), max_length=200)
    photo = models.ImageField(_("Фото"), upload_to="team/photos/", blank=True)
    bio = models.TextField(_("Биография"), blank=True)
    created_at = models.DateTimeField(_("Дата создания записи"), auto_now_add=True)

    class Meta:
        verbose_name = _("Член команды")
        verbose_name_plural = _("Команда")
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"


class MemberSocialLink(models.Model):
    member = models.ForeignKey(TeamMember, verbose_name=_("Сотрудник"), on_delete=models.CASCADE, related_name="socials")
    social = models.ForeignKey(SocialLink, verbose_name=_("Канал"), on_delete=models.CASCADE)
    url_or_value = models.CharField(_("URL или значение"), max_length=500)

    class Meta:
        verbose_name = _("Соц. профиль сотрудника")
        verbose_name_plural = _("Соц. профили сотрудников")
        constraints = [
            models.UniqueConstraint(fields=["member", "social"], name="main_membersocial_member_social_uniq"),
        ]

    def resolved_url(self) -> str:
        raw = (self.url_or_value or "").strip()
        if not raw or raw.startswith(("#", "javascript:")):
            return ""
        low = raw.lower()
        if low.startswith(("http://", "https://", "//", "mailto:", "tel:")):
            return raw
        base = (self.social.base_url or "").strip().rstrip("/")
        if base:
            return f"{base}/{raw.lstrip('/')}"
        return raw

    def __str__(self) -> str:
        return f"{self.member} ({self.social.name})"


class CandidateStatus(models.Model):
    """Статус заявки кандидата."""

    name = models.CharField(_("Название"), max_length=120, unique=True)

    class Meta:
        verbose_name = _("Статус кандидата")
        verbose_name_plural = _("Статусы кандидатов")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class CandidateProfile(models.Model):
    status = models.ForeignKey(
        CandidateStatus,
        verbose_name=_("Статус"),
        on_delete=models.PROTECT,
        related_name="candidates",
    )
    full_name = models.CharField(_("ФИО"), max_length=240)
    phone = models.CharField(_("Телефон"), max_length=40)
    email = models.EmailField(_("Электронная почта"))
    desired_position = models.CharField(_("Желаемая должность"), max_length=200)
    message = models.TextField(_("Сообщение / о себе"))
    created_at = models.DateTimeField(_("Дата подачи"), auto_now_add=True)

    class Meta:
        verbose_name = _("Заявка кандидата")
        verbose_name_plural = _("Заявки кандидатов")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.full_name


class CandidateAttachment(models.Model):
    candidate = models.ForeignKey(
        CandidateProfile,
        verbose_name=_("Кандидат"),
        on_delete=models.CASCADE,
        related_name="attachments",
    )
    file = models.FileField(_("Файл"), upload_to="candidates/attachments/")
    uploaded_at = models.DateTimeField(_("Дата загрузки"), auto_now_add=True)

    class Meta:
        verbose_name = _("Вложение кандидата")
        verbose_name_plural = _("Вложения кандидата")
        ordering = ["-uploaded_at"]

    def __str__(self) -> str:
        return self.file.name if self.file else str(self.pk)


class ContactMessage(models.Model):
    """Сообщение из формы обратной связи (единое поле контакта: телефон или email по плану БД)."""

    name = models.CharField(_("Имя / подпись"), max_length=200)
    phone_email = models.CharField(_("Телефон или email"), max_length=200)
    subject = models.CharField(_("Тема"), max_length=240, blank=True)
    message = models.TextField(_("Текст"))
    created_at = models.DateTimeField(_("Дата получения"), auto_now_add=True)
    processed_by = models.ForeignKey(
        User,
        verbose_name=_("Обработал"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="processed_contact_messages",
    )

    class Meta:
        verbose_name = _("Обращение")
        verbose_name_plural = _("Обращения")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.created_at:%Y-%m-%d})"


class ContactMessageAttachment(models.Model):
    message = models.ForeignKey(
        ContactMessage,
        verbose_name=_("Обращение"),
        on_delete=models.CASCADE,
        related_name="attachments",
    )
    file = models.FileField(_("Файл"), upload_to="contacts/attachments/")
    uploaded_at = models.DateTimeField(_("Дата загрузки"), auto_now_add=True)

    class Meta:
        verbose_name = _("Вложение обращения")
        verbose_name_plural = _("Вложения обращений")
        ordering = ["-uploaded_at"]

    def __str__(self) -> str:
        return self.file.name if self.file else str(self.pk)


from .content_models import *  # noqa: E402,F401,F403
