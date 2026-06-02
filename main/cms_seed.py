from __future__ import annotations

from datetime import date
from pathlib import Path

from django.conf import settings

from main.content_models import localized_message_hash as _l10_key


def _build_po_lookup() -> dict[str, str]:
    from main.po_reader import iter_po_pairs

    po_path = Path(settings.BASE_DIR) / "locale" / "en" / "LC_MESSAGES" / "django.po"
    return {mid: mstr or "" for mid, mstr in iter_po_pairs(po_path)}


def _en(po: dict[str, str], ru: str) -> str:
    return po.get(ru, "")


def apply_seed(apps, schema_editor) -> None:
    po = _build_po_lookup()

    LocalizedMessage = apps.get_model("main", "LocalizedMessage")
    for mid, mstr in po.items():
        if not mid.strip():
            continue
        LocalizedMessage.objects.update_or_create(
            key=_l10_key(mid),
            defaults={
                "ru": mid,
                "en": mstr or "",
            },
        )

    OrganizationContacts = apps.get_model("main", "OrganizationContacts")
    BrandSettings = apps.get_model("main", "BrandSettings")
    MarketingAsset = apps.get_model("main", "MarketingAsset")
    WorksPageSettings = apps.get_model("main", "WorksPageSettings")
    NewsListSettings = apps.get_model("main", "NewsListSettings")
    GalleryPageSettings = apps.get_model("main", "GalleryPageSettings")
    ContactsPageExtras = apps.get_model("main", "ContactsPageExtras")
    CareerPageSettings = apps.get_model("main", "CareerPageSettings")
    HubPageStub = apps.get_model("main", "HubPageStub")

    OrganizationContacts.objects.update_or_create(
        pk=1,
        defaults={
            "address_ru": "400050, Волгоград, ул. Маршала Рокоссовского 62, БЦ Волгоград Сити, 18 этаж",
            "address_en": _en(po, "400050, Волгоград, ул. Маршала Рокоссовского 62, БЦ Волгоград Сити, 18 этаж"),
            "phone_display": "8 (8442) 99-88-99",
            "phone_href": "tel:+78442998899",
            "email_display": "info@bykovogaz.ru",
            "email_href": "mailto:info@bykovogaz.ru",
            "weekday_hours_ru": "Понедельник - Пятница: 9:00 - 18:00",
            "weekday_hours_en": _en(po, "Понедельник - Пятница: 9:00 - 18:00"),
            "weekend_hours_ru": "Суббота - Воскресенье: Выходной",
            "weekend_hours_en": _en(po, "Суббота - Воскресенье: выходной"),
            "chamber_line_ru": "Член Союза «Волгоградская торгово-промышленная палата» с апреля 2019 года",
            "chamber_line_en": _en(
                po,
                "Член Союза «Волгоградская торгово-промышленная палата» с апреля 2019 года",
            ),
            "company_short_title_ru": "ООО «БЫКОВОГАЗ»",
            "company_short_title_en": _en(po, "ООО «БЫКОВОГАЗ»"),
            "legal_name_ru": "Полное наименование: Общество с ограниченной ответственностью «БЫКОВОГАЗ»",
            "legal_name_en": _en(po, "Полное наименование: Общество с ограниченной ответственностью «БЫКОВОГАЗ»"),
            "inn": "3439007015",
            "kpp": "340201001",
            "ogrn": "1033400954784",
        },
    )

    BrandSettings.objects.update_or_create(
        pk=1,
        defaults={
            "site_name_ru": "БЫКОВОГАЗ",
            "site_name_en": "BYKOVOGAZ",
            "header_tagline_ru": "Добыча углеводородного сырья",
            "header_tagline_en": _en(po, "Добыча углеводородного сырья"),
        },
    )

    MarketingAsset.objects.get_or_create(pk=1)

    WorksPageSettings.objects.update_or_create(
        pk=1,
        defaults={
            "page_title_ru": "Наши работы",
            "page_title_en": "Our Works",
            "hero_title_ru": "Наши работы",
            "hero_title_en": "Our Works",
            "hero_subtitle_ru": "Основные проекты и достижения компании",
            "hero_subtitle_en": "Key company projects and achievements",
            "realized_heading_ru": "Реализованные проекты",
            "realized_heading_en": "Completed Projects",
            "realized_lead_ru": (
                "За годы работы мы успешно реализовали множество проектов по разработке "
                "месторождения и созданию производственной инфраструктуры"
            ),
            "realized_lead_en": (
                "Over the years, we have successfully delivered numerous projects related to "
                "field development and production infrastructure."
            ),
            "kpi_heading_ru": "Ключевые показатели",
            "kpi_heading_en": "Key Metrics",
            "cta_title_ru": "Заинтересованы в сотрудничестве?",
            "cta_title_en": "Interested in cooperation?",
            "cta_subtitle_ru": "Свяжитесь с нами для обсуждения возможностей партнёрства",
            "cta_subtitle_en": "Contact us to discuss partnership opportunities",
        },
    )

    from main import published_constants as pub

    NewsListSettings.objects.update_or_create(
        pk=1,
        defaults={
            "page_title_ru": "Новости",
            "page_title_en": "News",
            "hero_title_ru": "Новости",
            "hero_title_en": "News",
            "hero_subtitle_ru": "Последние события и достижения компании",
            "hero_subtitle_en": "Latest company events and achievements",
            "list_page_size": pub._NEWS_LIST_PAGE_SIZE,
            "cta_title_ru": "Хотите быть в курсе всех новостей?",
            "cta_title_en": "Want to stay updated on all the news?",
            "cta_subtitle_ru": "Следите за нашими обновлениями и достижениями",
            "cta_subtitle_en": "Follow our updates and achievements",
            "cta_button_ru": "Перейти в галерею",
            "cta_button_en": "Open Gallery",
        },
    )

    GalleryPageSettings.objects.update_or_create(
        pk=1,
        defaults={
            "page_title_ru": "Галерея",
            "page_title_en": "Gallery",
            "hero_title_ru": "Галерея",
            "hero_title_en": "Gallery",
            "hero_subtitle_ru": "Фотографии нашей работы и достижений",
            "hero_subtitle_en": "Photos of our work and achievements",
            "initial_visible_count": pub._GALLERY_INITIAL_VISIBLE,
        },
    )

    ContactsPageExtras.objects.update_or_create(
        pk=1,
        defaults={
            "hero_title_ru": "Контакты",
            "hero_title_en": _en(po, "Контакты"),
            "hero_lead_ru": "Свяжитесь с нами удобным способом",
            "hero_lead_en": _en(po, "Свяжитесь с нами удобным способом"),
            "panel_eyebrow_ru": "Контактная информация",
            "panel_eyebrow_en": _en(po, "Контактная информация"),
            "panel_heading_ru": "Мы всегда на связи",
            "panel_heading_en": _en(po, "Мы всегда на связи"),
            "panel_lead_ru": (
                "Для общих вопросов, сотрудничества и деловой переписки используйте "
                "удобный для вас канал связи."
            ),
            "panel_lead_en": _en(
                po,
                (
                    "Для общих вопросов, сотрудничества и деловой переписки используйте "
                    "удобный для вас канал связи."
                ),
            ),
        },
    )

    CareerPageSettings.objects.update_or_create(
        pk=1,
        defaults={
            "hero_title_ru": "Карьера",
            "hero_title_en": _en(po, "Карьера"),
            "hero_lead_ru": "Присоединяйтесь к нашей команде",
            "hero_lead_en": _en(po, "Присоединяйтесь к нашей команде"),
        },
    )

    HubPageStub.objects.update_or_create(
        code="about",
        defaults={
            "heading_ru": pub._PAGE_TITLES["about"]["ru"],
            "heading_en": pub._PAGE_TITLES["about"]["en"],
        },
    )
    HubPageStub.objects.update_or_create(
        code="press",
        defaults={
            "heading_ru": pub._PAGE_TITLES["press"]["ru"],
            "heading_en": pub._PAGE_TITLES["press"]["en"],
        },
    )

    HomeStatTile = apps.get_model("main", "HomeStatTile")
    HomeStatTile.objects.all().delete()
    tiles = [
        ("2002", "Год основания"),
        ("250", "Млн м<sup>3</sup>/год газа"),
        ("40", "Тыс. тонн/год конденсата"),
        ("140", "Сотрудников"),
    ]
    for order, (val, lbl_ru) in enumerate(tiles):
        use_html = "<sup>" in lbl_ru
        lbl_en = _en(po, lbl_ru) if not use_html else _en(po, "Млн м<sup>3</sup>/год газа")
        HomeStatTile.objects.create(
            value_text=val,
            label_ru=lbl_ru,
            label_en=lbl_en,
            use_html_labels=use_html,
            sort_order=order,
        )

    HomeServiceCard = apps.get_model("main", "HomeServiceCard")
    HomeServiceCard.objects.all().delete()
    cards = [
        (
            "factory",
            "Разработка недр",
            _en(po, "Разработка недр"),
            "Геологоразведка и разработка углеводородных месторождений.",
            _en(po, "Геологоразведка и разработка углеводородных месторождений."),
        ),
        (
            "flame",
            "Добыча газа",
            _en(po, "Добыча газа"),
            "Промышленная добыча природного газа до 250 млн м<sup>3</sup>/год.",
            _en(po, "Промышленная добыча природного газа до 250 млн м<sup>3</sup>/год."),
        ),
        (
            "pressure",
            "Добыча конденсата",
            _en(po, "Добыча конденсата"),
            "Производство газового конденсата до 40 тыс. тонн/год.",
            _en(po, "Производство газового конденсата до 40 тыс. тонн/год."),
        ),
        (
            "drill",
            "Буровые услуги",
            _en(po, "Буровые услуги"),
            "Бурение скважин на нефть и газ, обустройство месторождений.",
            _en(po, "Бурение скважин на нефть и газ, обустройство месторождений."),
        ),
    ]
    for order, row in enumerate(cards):
        HomeServiceCard.objects.create(
            icon=row[0],
            title_ru=row[1],
            title_en=row[2],
            body_ru=row[3],
            body_en=row[4],
            sort_order=order,
        )

    TeamValue = apps.get_model("main", "TeamValue")
    TeamValue.objects.all().delete()
    team_rows = [
        (
            "Профессионализм",
            "Высококвалифицированные специалисты с многолетним опытом.",
        ),
        (
            "Ответственность",
            "Гарантируем выполнение всех обязательств перед клиентами.",
        ),
        (
            "Инновации",
            "Внедряем современные технологии для улучшения качества услуг.",
        ),
    ]
    for order, (t_ru, b_ru) in enumerate(team_rows):
        TeamValue.objects.create(
            title_ru=t_ru,
            title_en=_en(po, t_ru),
            body_ru=b_ru,
            body_en=_en(po, b_ru),
            sort_order=order,
        )

    AboutExploreCard = apps.get_model("main", "AboutExploreCard")
    AboutExploreCard.objects.all().delete()
    explore_rows = [
        ("О месторождении", "История и характеристика Южно-Кисловского месторождения.", "main:about_field"),
        ("Лицензия", "Лицензия на разведку и добычу углеводородного сырья.", "main:about_license"),
        ("Виртуальный тур", "Совершите виртуальную экскурсию по нашему офису.", "main:about_tour"),
    ]
    for order, (title_ru, txt_ru, urln) in enumerate(explore_rows):
        AboutExploreCard.objects.create(
            title_ru=title_ru,
            title_en=_en(po, title_ru),
            text_ru=txt_ru,
            text_en=_en(po, txt_ru),
            url_name=urln,
            sort_order=order,
        )

    FieldSiteBullet = apps.get_model("main", "FieldSiteBullet")
    FieldSiteBullet.objects.all().delete()
    geo_items = [
        "Быковский район Волгоградской области",
        "30 км к юго-востоку от р. п. Быково",
        "Левый берег Волги",
    ]
    for order, ru in enumerate(geo_items):
        FieldSiteBullet.objects.create(
            group_slug="geo",
            body_ru=ru,
            body_en=_en(po, ru),
            supports_html=False,
            sort_order=order,
        )
    geol_plain = [
        "Продуктивные песчаные пласты нижнего мела",
        "Газоконденсатная залежь",
    ]
    order = 0
    for ru in geol_plain:
        FieldSiteBullet.objects.create(
            group_slug="geology",
            body_ru=ru,
            body_en=_en(po, ru),
            supports_html=False,
            sort_order=order,
        )
        order += 1
    lic_area_ru = "Площадь лицензированного участка 36 км<sup>2</sup>"
    FieldSiteBullet.objects.create(
        group_slug="geology",
        body_ru=lic_area_ru,
        body_en=_en(po, lic_area_ru),
        supports_html=True,
        sort_order=order,
    )

    Zone = apps.get_model("main", "VirtualTourOfficeZone")
    VB = apps.get_model("main", "VirtualTourBullet")
    Zone.objects.all().delete()
    server = Zone.objects.create(
        slug="server",
        css_modifier="server",
        title_ru="Серверная",
        title_en=_en(po, "Серверная"),
        intro_ru=(
            "Техническое сердце компании: здесь размещено оборудование для поддержки "
            "корпоративной инфраструктуры и хранения данных."
        ),
        intro_en=_en(
            po,
            "Техническое сердце компании: здесь размещено оборудование для поддержки "
            "корпоративной инфраструктуры и хранения данных.",
        ),
        sort_order=0,
    )

    srv_bullets = ["Поддержка IT-систем", "Система наблюдения", "Защита данных"]
    for sid, tb in enumerate(srv_bullets):
        VB.objects.create(zone=server, text_ru=tb, text_en=_en(po, tb), sort_order=sid)

    workspace = Zone.objects.create(
        slug="workspace",
        css_modifier="workspace",
        title_ru="Офисное пространство",
        title_en=_en(po, "Офисное пространство"),
        intro_ru=(
            "Современное рабочее пространство с комфортными условиями для продуктивной работы "
            "и взаимодействия между отделами."
        ),
        intro_en=_en(
            po,
            "Современное рабочее пространство с комфортными условиями для продуктивной работы "
            "и взаимодействия между отделами.",
        ),
    )
    work_bullets = ["Эргономичные рабочие места", "Естественное освещение", "Современная техника"]
    for sid, tb in enumerate(work_bullets):
        VB.objects.create(zone=workspace, text_ru=tb, text_en=_en(po, tb), sort_order=sid)

    meeting = Zone.objects.create(
        slug="meeting",
        css_modifier="meeting",
        title_ru="Комната совещаний",
        title_en=_en(po, "Комната совещаний"),
        intro_ru=(
            "Пространство для проведения совещаний, презентаций и переговоров, оснащенное "
            "необходимым мультимедийным оборудованием."
        ),
        intro_en=_en(
            po,
            "Пространство для проведения совещаний, презентаций и переговоров, оснащенное "
            "необходимым мультимедийным оборудованием.",
        ),
    )
    meet_bullets = ["Мультимедийное оборудование", "Видеоконференцсвязь", "Комфортная мебель"]
    for sid, tb in enumerate(meet_bullets):
        VB.objects.create(zone=meeting, text_ru=tb, text_en=_en(po, tb), sort_order=sid)

    WorkTimelineProject = apps.get_model("main", "WorkTimelineProject")
    WorkAchievement = apps.get_model("main", "WorkTimelineAchievement")
    WorkTimelineProject.objects.all().delete()
    for wi, chunk in enumerate(pub._WORKS_TIMELINE):
        title_en = chunk["project_title"]["en"] if isinstance(chunk["project_title"], dict) else chunk["project_title"]
        title_ru = chunk["project_title"]["ru"] if isinstance(chunk["project_title"], dict) else chunk["project_title"]
        desc_en = chunk["description"]["en"] if isinstance(chunk["description"], dict) else chunk["description"]
        desc_ru = chunk["description"]["ru"] if isinstance(chunk["description"], dict) else chunk["description"]
        show_home = wi < 2
        proj = WorkTimelineProject.objects.create(
            blue_left=chunk["blue_left"],
            blue_height_px=chunk["blue_height_px"],
            period=chunk["period"],
            status_ru=chunk["status"]["ru"],
            status_en=chunk["status"]["en"],
            title_ru=title_ru,
            title_en=title_en,
            description_ru=desc_ru,
            description_en=desc_en,
            sort_order=wi,
            show_on_homepage=show_home,
            home_sort_order=wi,
        )
        for ai, ach in enumerate(chunk["achievements"]):
            WorkAchievement.objects.create(
                project=proj,
                text_ru=ach["ru"],
                text_en=ach["en"],
                sort_order=ai,
            )

    WorkPageKpi = apps.get_model("main", "WorkPageKpi")
    WorkPageKpi.objects.all().delete()
    for ki, km in enumerate(pub._WORKS_KPIS):
        if "label_html" in km:
            lh = km["label_html"]
            WorkPageKpi.objects.create(
                value=km["value"],
                label_ru="",
                label_en="",
                label_html_ru=lh["ru"],
                label_html_en=lh["en"],
                sort_order=ki,
            )
        else:
            lb = km["label"]
            WorkPageKpi.objects.create(
                value=km["value"],
                label_ru=lb["ru"],
                label_en=lb["en"],
                label_html_ru="",
                label_html_en="",
                sort_order=ki,
            )

    GC = apps.get_model("main", "GalleryCategory")
    GI = apps.get_model("main", "GalleryItem")
    GC.objects.all().delete()
    GI.objects.all().delete()
    for ci, cat in enumerate(pub._GALLERY_CATEGORY_OPTIONS):
        GC.objects.create(
            slug=cat["id"],
            label_ru=cat["label"]["ru"],
            label_en=cat["label"]["en"],
            sort_order=ci,
            is_all_option=cat["id"] == "all",
        )
    slug_to_cat = {c.slug: c for c in GC.objects.all()}
    for ix, triple in enumerate(pub._GALLERY_ITEMS_RAW):
        src, cap, slug = triple
        GI.objects.create(
            category=slug_to_cat[slug],
            static_path=src,
            caption_ru=cap["ru"],
            caption_en=cap["en"],
            sort_order=ix,
            is_active=True,
        )

    PressArticle = apps.get_model("main", "PressNewsArticle")
    PressArticle.objects.all().delete()

    ex_intro12 = (
        "Компания успешно ввела в промышленную эксплуатацию разведочную скважину №12 "
        "Южно-Кисловского газоконденсатного месторождения."
    )
    ex_tpp = (
        "ООО «БЫКОВОГАЗ» стало членом Союза «Волгоградская торгово-промышленная палата», "
        "укрепив свои позиции в деловом сообществе региона."
    )
    ex_launch = (
        "Получено разрешение на ввод установки комплексной подготовки газа в промышленную "
        "эксплуатацию. Начался этап промышленной разработки месторождения."
    )
    ex_seismic = (
        "Компанией успешно завершены сейсморазведочные работы МОГТ-3D на площади 63 км² "
        "для уточнения геологического строения месторождения."
    )
    ex_reserves = (
        "Запасы углеводородного сырья Южно-Кисловского месторождения поставлены на государственный баланс ГКЗ РФ."
    )
    ex_home_ukpg = (
        "Успешно завершено строительство установки комплексной подготовки газа "
        "с проектной мощностью 250 млн м<sup>3</sup>/год по газу и 40 тыс. т/год по конденсату."
    )

    supplemental = [
        {
            "published_at": date(2019, 12, 15),
            "display_date_ru": "15 декабря 2019",
            "display_date_en": "December 15, 2019",
            "category_ru": "Производство",
            "category_en": "Production",
            "title_ru": "Введение в эксплуатацию разведочной скважины №12",
            "title_en": _en(po, "Введение в эксплуатацию разведочной скважины №12"),
            "excerpt_ru": ex_intro12,
            "excerpt_en": _en(po, ex_intro12),
            "gallery_style": "production",
            "home_order": 0,
        },
        {
            "published_at": date(2019, 4, 15),
            "display_date_ru": "15 апреля 2019",
            "display_date_en": "April 15, 2019",
            "category_ru": "Корпоративные новости",
            "category_en": "Corporate News",
            "title_ru": "БЫКОВОГАЗ вступил в Торгово-промышленную палату",
            "title_en": _en(po, "БЫКОВОГАЗ вступил в Торгово-промышленную палату"),
            "excerpt_ru": ex_tpp,
            "excerpt_en": _en(po, ex_tpp),
            "gallery_style": "corporate",
            "home_order": 1,
        },
        {
            "published_at": date(2017, 12, 20),
            "display_date_ru": "20 декабря 2017",
            "display_date_en": "December 20, 2017",
            "category_ru": "Производство",
            "category_en": "Production",
            "title_ru": "Запуск УКПГ в промышленную эксплуатацию",
            "title_en": _en(po, "Запуск УКПГ в промышленную эксплуатацию"),
            "excerpt_ru": ex_launch,
            "excerpt_en": _en(po, ex_launch),
            "gallery_style": "industry",
            "home_order": 2,
        },
        {
            "published_at": date(2014, 9, 10),
            "display_date_ru": "10 сентября 2014",
            "display_date_en": "September 10, 2014",
            "category_ru": "Геологоразведка",
            "category_en": _en(po, "Геологоразведка") or "Exploration",
            "title_ru": "Завершение сейсморазведочных работ МОГТ-3D",
            "title_en": _en(po, "Завершение сейсморазведочных работ МОГТ-3D"),
            "excerpt_ru": ex_seismic,
            "excerpt_en": _en(po, ex_seismic),
            "gallery_style": "survey",
            "home_order": 4,
        },
        {
            "published_at": date(2006, 12, 1),
            "display_date_ru": "1 декабря 2006",
            "display_date_en": "December 1, 2006",
            "category_ru": "Корпоративные новости",
            "category_en": "Corporate News",
            "title_ru": "Утверждение запасов месторождения ГКЗ РФ",
            "title_en": _en(po, "Утверждение запасов месторождения ГКЗ РФ"),
            "excerpt_ru": ex_reserves,
            "excerpt_en": _en(po, ex_reserves),
            "gallery_style": "archive",
            "home_order": 5,
        },
    ]

    for row in supplemental:
        PressArticle.objects.create(
            published_at=row["published_at"],
            display_date_ru=row["display_date_ru"],
            display_date_en=row["display_date_en"] or row["display_date_ru"],
            category_ru=row["category_ru"],
            category_en=row["category_en"],
            title_ru=row["title_ru"],
            title_en=row["title_en"],
            excerpt_ru=row["excerpt_ru"],
            excerpt_en=row["excerpt_en"] or row["excerpt_ru"],
            detail_url="",
            gallery_style=row["gallery_style"],
            is_published=True,
            show_on_homepage=True,
            home_sort_order=row["home_order"],
            hero_image=None,
        )

    for row in pub._NEWS_ARTICLES_RAW:
        iso = row["iso_date"]
        title_ru = row["title"]["ru"]
        is_home_highlight = iso == "2017-06-30" and title_ru.startswith("Завершение строительства УКПГ")
        excerpt_ru = ex_home_ukpg if is_home_highlight else row["excerpt"]["ru"]
        excerpt_en = _en(po, ex_home_ukpg) if is_home_highlight else row["excerpt"]["en"]
        PressArticle.objects.create(
            published_at=date.fromisoformat(iso),
            display_date_ru=row["date_display"]["ru"],
            display_date_en=row["date_display"]["en"],
            category_ru=row["category"]["ru"],
            category_en=row["category"]["en"],
            title_ru=title_ru,
            title_en=row["title"]["en"],
            excerpt_ru=excerpt_ru,
            excerpt_en=excerpt_en,
            detail_url=(row["detail_url"] if row["detail_url"] != "#" else ""),
            hero_image=None,
            gallery_style="plant" if is_home_highlight else "",
            is_published=True,
            show_on_homepage=is_home_highlight,
            home_sort_order=3 if is_home_highlight else 0,
        )
