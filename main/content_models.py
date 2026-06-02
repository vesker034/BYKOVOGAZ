import hashlib

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def localized_message_hash(source_ru: str) -> str:
    raw = source_ru.replace("\u00a0", " ").strip()
    raw_norm = " ".join(raw.split())
    return hashlib.sha256(raw_norm.encode("utf-8")).hexdigest()[:16]


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        return None


class LocalizedMessage(models.Model):
    """Тексты интерфейса и страниц; ключ — короткий хэш русской версии строки."""

    key = models.CharField(_("Ключ (хэш)"), max_length=16, primary_key=True)
    ru = models.TextField(_("RU"))
    en = models.TextField(_("EN"), blank=True)

    class Meta:
        verbose_name = _("Локализованная строка")
        verbose_name_plural = _("Локализованные строки")
        ordering = ["key"]

    def __str__(self):
        excerpt = (self.ru or "").replace("\n", " ")[:50]
        return f"{self.key} — {excerpt}"


class BrandSettings(SingletonModel):
    site_name_ru = models.CharField(_("Название на сайте (RU)"), max_length=120, default="БЫКОВОГАЗ")
    site_name_en = models.CharField(_("Название на сайте (EN)"), max_length=120, default="BYKOVOGAZ")
    header_tagline_ru = models.CharField(_("Подзаголовок в шапке (RU)"), max_length=200, default="")
    header_tagline_en = models.CharField(_("Подзаголовок в шапке (EN)"), max_length=200, blank=True)

    class Meta:
        verbose_name = _("Фирменные настройки")
        verbose_name_plural = _("Фирменные настройки")


class OrganizationContacts(SingletonModel):
    address_ru = models.TextField(_("Адрес (RU)"), default="")
    address_en = models.TextField(_("Адрес (EN)"), blank=True)
    phone_display = models.CharField(_("Телефон для отображения"), max_length=80, default="")
    phone_href = models.CharField(_("Ссылка tel:"), max_length=80, default="")
    email_display = models.CharField(_("Email для отображения"), max_length=120, default="")
    email_href = models.CharField(_("Ссылка mailto:"), max_length=160, default="")
    weekday_hours_ru = models.CharField(_("Режим работы будни (RU)"), max_length=200, default="")
    weekday_hours_en = models.CharField(_("Режим работы будни (EN)"), max_length=200, blank=True)
    weekend_hours_ru = models.CharField(_("Режим выходные (RU)"), max_length=200, default="")
    weekend_hours_en = models.CharField(_("Режим выходные (EN)"), max_length=200, blank=True)
    chamber_line_ru = models.TextField(_("Строка о ТПП (RU)"), blank=True)
    chamber_line_en = models.TextField(_("Строка о ТПП (EN)"), blank=True)
    company_short_title_ru = models.CharField(_("Краткое имя организации для © (RU)"), max_length=200, default="")
    company_short_title_en = models.CharField(_("Краткое имя организации для © (EN)"), max_length=200, blank=True)
    legal_name_ru = models.TextField(_("Полное наименование (реквизиты, RU)"), default="")
    legal_name_en = models.TextField(_("Полное наименование (реквизиты, EN)"), blank=True)
    inn = models.CharField("ИНН", max_length=12, default="")
    kpp = models.CharField("КПП", max_length=12, default="")
    ogrn = models.CharField("ОГРН", max_length=20, default="")

    class Meta:
        verbose_name = _("Контакты и реквизиты")
        verbose_name_plural = _("Контакты и реквизиты")


class MarketingAsset(SingletonModel):
    license_scan = models.ImageField(_("Скан лицензии"), upload_to="site/license/", blank=True, null=True)
    home_about_image = models.ImageField(_("Изображение «О компании» на главной"), upload_to="site/home/", blank=True, null=True)

    class Meta:
        verbose_name = _("Изображения для страниц")
        verbose_name_plural = _("Изображения для страниц")


class WorkTimelineProject(models.Model):
    blue_left = models.BooleanField(_("Синяя колонка слева"), default=True)
    blue_height_px = models.DecimalField(_("Высота синей колонки, px"), max_digits=6, decimal_places=2, default="155.96")
    period = models.CharField(_("Период"), max_length=64)
    status_ru = models.CharField(_("Статус (RU)"), max_length=120)
    status_en = models.CharField(_("Статус (EN)"), max_length=120, blank=True)
    title_ru = models.CharField(_("Название проекта (RU)"), max_length=260)
    title_en = models.CharField(_("Название проекта (EN)"), max_length=260, blank=True)
    description_ru = models.TextField(_("Описание (RU)"))
    description_en = models.TextField(_("Описание (EN)"), blank=True)
    sort_order = models.PositiveIntegerField(_("Порядок на странице «Работы»"), default=0)
    show_on_homepage = models.BooleanField(_("Показывать на главной"), default=False)
    home_sort_order = models.PositiveIntegerField(_("Порядок на главной"), default=0)

    class Meta:
        verbose_name = _("Этап / проект (таймлайн)")
        verbose_name_plural = _("Таймлайн работ")
        ordering = ["sort_order", "pk"]

    def __str__(self):
        return f"{self.period} — {self.title_ru}"


class WorkTimelineAchievement(models.Model):
    project = models.ForeignKey(
        WorkTimelineProject,
        verbose_name=_("Проект"),
        related_name="achievements",
        on_delete=models.CASCADE,
    )
    text_ru = models.CharField(_("Пункт (RU)"), max_length=350)
    text_en = models.CharField(_("Пункт (EN)"), max_length=350, blank=True)
    sort_order = models.PositiveIntegerField(_("Порядок"), default=0)

    class Meta:
        verbose_name = _("Достижение проекта")
        verbose_name_plural = _("Достижения проектов")
        ordering = ["project", "sort_order", "pk"]

    def __str__(self):
        return self.text_ru[:40]


class WorkPageKpi(models.Model):
    value = models.CharField(_("Значение"), max_length=40)
    label_ru = models.CharField(_("Подпись (RU)"), max_length=200, blank=True)
    label_en = models.CharField(_("Подпись (EN)"), max_length=200, blank=True)
    label_html_ru = models.CharField(_("Подпись HTML (RU)"), max_length=320, blank=True)
    label_html_en = models.CharField(_("Подпись HTML (EN)"), max_length=320, blank=True)
    sort_order = models.PositiveIntegerField(_("Порядок"), default=0)

    class Meta:
        verbose_name = _("KPI блока работ")
        verbose_name_plural = _("KPI блока работ")
        ordering = ["sort_order", "pk"]

    def clean(self):
        ru_plain = bool((self.label_ru or "").strip())
        ru_html = bool((self.label_html_ru or "").strip())
        if not ru_plain and not ru_html:
            raise ValidationError(_("Укажите подпись (RU) или HTML-подпись (RU)."))


class PressNewsArticle(models.Model):
    published_at = models.DateField(_("Дата публикации"))
    display_date_ru = models.CharField(_("Дата в виде текста (RU)"), max_length=120, blank=True)
    display_date_en = models.CharField(_("Дата в виде текста (EN)"), max_length=120, blank=True)
    category_ru = models.CharField(_("Рубрика (RU)"), max_length=120)
    category_en = models.CharField(_("Рубрика (EN)"), max_length=120, blank=True)
    title_ru = models.CharField(_("Заголовок (RU)"), max_length=300)
    title_en = models.CharField(_("Заголовок (EN)"), max_length=300, blank=True)
    excerpt_ru = models.TextField(_("Анонс (RU)"))
    excerpt_en = models.TextField(_("Анонс (EN)"), blank=True)
    detail_url = models.URLField(_("Ссылка на подробнее"), blank=True)
    hero_image = models.ImageField(_("Изображение карточки"), upload_to="press/news/", blank=True, null=True)
    gallery_style = models.CharField(
        _("Стиль блока медиа на главной"),
        max_length=32,
        blank=True,
        help_text=_("Классы: production, corporate, industry, plant, survey, archive — для карточки на главной."),
    )
    is_published = models.BooleanField(_("Опубликовано"), default=True)
    show_on_homepage = models.BooleanField(_("Показать блок на главной"), default=False)
    home_sort_order = models.PositiveIntegerField(_("Порядок на главной"), default=0)

    class Meta:
        verbose_name = _("Новость")
        verbose_name_plural = _("Новости")
        ordering = ["-published_at", "pk"]

    def __str__(self):
        return self.title_ru


class NewsListSettings(SingletonModel):
    page_title_ru = models.CharField(max_length=120)
    page_title_en = models.CharField(max_length=120, blank=True)
    hero_title_ru = models.CharField(max_length=160)
    hero_title_en = models.CharField(max_length=160, blank=True)
    hero_subtitle_ru = models.CharField(max_length=320)
    hero_subtitle_en = models.CharField(max_length=320, blank=True)
    list_page_size = models.PositiveSmallIntegerField(default=6)
    cta_title_ru = models.CharField(max_length=200)
    cta_title_en = models.CharField(max_length=200, blank=True)
    cta_subtitle_ru = models.CharField(max_length=260)
    cta_subtitle_en = models.CharField(max_length=260, blank=True)
    cta_button_ru = models.CharField(max_length=120)
    cta_button_en = models.CharField(max_length=120, blank=True)

    class Meta:
        verbose_name = _("Настройки списка новостей")
        verbose_name_plural = _("Настройки списка новостей")


class WorksPageSettings(SingletonModel):
    page_title_ru = models.CharField(max_length=120)
    page_title_en = models.CharField(max_length=120, blank=True)
    hero_title_ru = models.CharField(max_length=160)
    hero_title_en = models.CharField(max_length=160, blank=True)
    hero_subtitle_ru = models.CharField(max_length=320)
    hero_subtitle_en = models.CharField(max_length=320, blank=True)
    realized_heading_ru = models.CharField(max_length=160)
    realized_heading_en = models.CharField(max_length=160, blank=True)
    realized_lead_ru = models.CharField(max_length=400)
    realized_lead_en = models.CharField(max_length=400, blank=True)
    kpi_heading_ru = models.CharField(max_length=160)
    kpi_heading_en = models.CharField(max_length=160, blank=True)
    cta_title_ru = models.CharField(max_length=200)
    cta_title_en = models.CharField(max_length=200, blank=True)
    cta_subtitle_ru = models.CharField(max_length=260)
    cta_subtitle_en = models.CharField(max_length=260, blank=True)

    class Meta:
        verbose_name = _("Настройки страницы «Работы»")
        verbose_name_plural = _("Настройки страницы «Работы»")


class GalleryCategory(models.Model):
    slug = models.SlugField(_("Код фильтра"), max_length=32, unique=True)
    label_ru = models.CharField(_("Подпись (RU)"), max_length=160)
    label_en = models.CharField(_("Подпись (EN)"), max_length=160, blank=True)
    sort_order = models.PositiveIntegerField(_("Порядок"), default=0)
    is_all_option = models.BooleanField(_("Специальный пункт «Все»"), default=False)

    class Meta:
        verbose_name = _("Категория галереи")
        verbose_name_plural = _("Категории галереи")
        ordering = ["sort_order", "slug"]

    def __str__(self):
        return f"{self.slug}"


class GalleryItem(models.Model):
    category = models.ForeignKey(GalleryCategory, verbose_name=_("Категория"), related_name="items", on_delete=models.PROTECT)
    image = models.ImageField(_("Изображение"), upload_to="press/gallery/", blank=True, null=True)
    static_path = models.CharField(
        _("Путь под static"),
        max_length=200,
        blank=True,
        help_text=_('Например: img/news/news-01.png (если нет загружаемого файла).'),
    )
    caption_ru = models.CharField(_("Подпись (RU)"), max_length=220)
    caption_en = models.CharField(_("Подпись (EN)"), max_length=220, blank=True)
    sort_order = models.PositiveIntegerField(_("Порядок"), default=0)
    is_active = models.BooleanField(_("На сайте"), default=True)

    class Meta:
        verbose_name = _("Элемент галереи")
        verbose_name_plural = _("Элементы галереи")
        ordering = ["sort_order", "pk"]

    def clean(self):
        if not self.image and not (self.static_path or "").strip():
            raise ValidationError(_("Укажите файл изображения или путь под static."))

    def resolved_src(self):
        """Возвращает относительный URL media или строку-путь под static."""

        if self.image:
            return self.image.url
        return self.static_path.strip()


class GalleryPageSettings(SingletonModel):
    page_title_ru = models.CharField(max_length=120)
    page_title_en = models.CharField(max_length=120, blank=True)
    hero_title_ru = models.CharField(max_length=160)
    hero_title_en = models.CharField(max_length=160, blank=True)
    hero_subtitle_ru = models.CharField(max_length=260)
    hero_subtitle_en = models.CharField(max_length=260, blank=True)
    initial_visible_count = models.PositiveSmallIntegerField(_("Количество снимков до «Загрузить ещё»"), default=8)

    class Meta:
        verbose_name = _("Настройки галереи")
        verbose_name_plural = _("Настройки галереи")


class HomeStatTile(models.Model):
    value_text = models.CharField(_("Значение"), max_length=40)
    label_ru = models.CharField(_("Подпись (RU)"), max_length=200)
    label_en = models.CharField(_("Подпись (EN)"), max_length=200, blank=True)
    use_html_labels = models.BooleanField(_("Подпись с HTML-тегами"), default=False)
    sort_order = models.PositiveIntegerField(_("Порядок"), default=0)

    class Meta:
        verbose_name = _("Показатель на главной (цифры)")
        verbose_name_plural = _("Показатели на главной (цифры)")
        ordering = ["sort_order", "pk"]


class HomeServiceCard(models.Model):
    ICON_FACTORY = "factory"
    ICON_FLAME = "flame"
    ICON_PRESSURE = "pressure"
    ICON_DRILL = "drill"

    ICON_CHOICES = [
        (ICON_FACTORY, _("Подземная разработка / завод")),
        (ICON_FLAME, _("Пламя / газ")),
        (ICON_PRESSURE, _("Давление / конденсат")),
        (ICON_DRILL, _("Бурение")),
    ]

    icon = models.CharField(_("Иконка"), max_length=20, choices=ICON_CHOICES)
    title_ru = models.CharField(max_length=160)
    title_en = models.CharField(max_length=160, blank=True)
    body_ru = models.TextField()
    body_en = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(_("Порядок"), default=0)

    class Meta:
        verbose_name = _("Карточка «Направления» на главной")
        verbose_name_plural = _("Карточки «Направления» на главной")
        ordering = ["sort_order", "pk"]


class TeamValue(models.Model):
    title_ru = models.CharField(max_length=140)
    title_en = models.CharField(max_length=140, blank=True)
    body_ru = models.TextField()
    body_en = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(_("Порядок"), default=0)

    class Meta:
        verbose_name = _("Ценность команды")
        verbose_name_plural = _("Ценности команды")
        ordering = ["sort_order", "pk"]


class HubPageStub(models.Model):
    """Заготовки простых узлов («О нас» / «Пресс-центр» без контента на hub-странице)."""

    code = models.SlugField(primary_key=True, max_length=32)
    heading_ru = models.CharField(max_length=140)
    heading_en = models.CharField(max_length=140, blank=True)

    class Meta:
        verbose_name = _("Страница-заготовка")
        verbose_name_plural = _("Страницы-заготовки")


class AboutExploreCard(models.Model):
    title_ru = models.CharField(max_length=160)
    title_en = models.CharField(max_length=160, blank=True)
    text_ru = models.TextField()
    text_en = models.TextField(blank=True)
    url_name = models.CharField(
        _("Имя маршрута Django"),
        max_length=64,
        help_text=_("Например: main:about_field"),
    )
    sort_order = models.PositiveIntegerField(_("Порядок"), default=0)

    class Meta:
        verbose_name = _("Карточка блока «Узнайте больше»")
        verbose_name_plural = _("Карточки блока «Узнайте больше»")
        ordering = ["sort_order", "pk"]

    def build_url(self):
        return reverse(self.url_name)


class ContactsPageExtras(SingletonModel):
    hero_title_ru = models.CharField(max_length=140)
    hero_title_en = models.CharField(max_length=140, blank=True)
    hero_lead_ru = models.CharField(max_length=220)
    hero_lead_en = models.CharField(max_length=220, blank=True)
    panel_eyebrow_ru = models.CharField(max_length=120)
    panel_eyebrow_en = models.CharField(max_length=120, blank=True)
    panel_heading_ru = models.CharField(max_length=140)
    panel_heading_en = models.CharField(max_length=140, blank=True)
    panel_lead_ru = models.CharField(max_length=300)
    panel_lead_en = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = _("Тексты страницы «Контакты»")
        verbose_name_plural = _("Тексты страницы «Контакты»")


class CareerPageSettings(SingletonModel):
    hero_title_ru = models.CharField(max_length=140)
    hero_title_en = models.CharField(max_length=140, blank=True)
    hero_lead_ru = models.CharField(max_length=220)
    hero_lead_en = models.CharField(max_length=220, blank=True)

    class Meta:
        verbose_name = _("Настройки страницы карьеры")
        verbose_name_plural = _("Настройки страницы карьеры")


class VirtualTourOfficeZone(models.Model):
    slug = models.SlugField(unique=True)
    css_modifier = models.SlugField(
        _("CSS-модификатор блока медиа"),
        max_length=32,
        help_text=_("server / workspace / meeting и т. п."),
    )
    title_ru = models.CharField(max_length=160)
    title_en = models.CharField(max_length=160, blank=True)
    intro_ru = models.TextField()
    intro_en = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(_("Порядок"), default=0)

    class Meta:
        verbose_name = _("Зона виртуального тура")
        verbose_name_plural = _("Зоны виртуального тура")
        ordering = ["sort_order", "pk"]


class VirtualTourBullet(models.Model):
    zone = models.ForeignKey(VirtualTourOfficeZone, verbose_name=_("Зона"), related_name="bullets", on_delete=models.CASCADE)
    text_ru = models.CharField(max_length=240)
    text_en = models.CharField(max_length=240, blank=True)
    sort_order = models.PositiveIntegerField(_("Порядок"), default=0)

    class Meta:
        verbose_name = _("Пункт списка (тур)")
        verbose_name_plural = _("Пункты списка (тур)")
        ordering = ["zone", "sort_order", "pk"]


class FieldSiteBullet(models.Model):
    """Строки списков на странице «О месторождении» (география, факты)."""

    group_slug = models.SlugField(max_length=32)
    body_ru = models.CharField(max_length=260)
    body_en = models.CharField(max_length=260, blank=True)
    supports_html = models.BooleanField(_("HTML в тексте пункта"), default=False)
    sort_order = models.PositiveIntegerField(_("Порядок"), default=0)

    class Meta:
        verbose_name = _("Пункт блока месторождения")
        verbose_name_plural = _("Пункты блоков месторождения")
        ordering = ["group_slug", "sort_order", "pk"]
