from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils.translation import get_language

from .models import Vacancy


def _language_code():
    language = (get_language() or "ru").lower()
    return "en" if language.startswith("en") else "ru"


def _localize(value, language):
    if isinstance(value, dict):
        if "ru" in value or "en" in value:
            return value.get(language) or value.get("ru") or value.get("en")
        return {key: _localize(item, language) for key, item in value.items()}
    if isinstance(value, list):
        return [_localize(item, language) for item in value]
    return value


_PAGE_TITLES = {
    "about": {"ru": "О нас", "en": "About"},
    "press": {"ru": "Пресс-центр", "en": "Press Center"},
}

_WORKS_TIMELINE = [
    {
        "blue_left": True,
        "blue_height_px": 155.96,
        "period": "2015-2017",
        "project_title": {"ru": "Строительство УКПГ", "en": "Gas Treatment Unit Construction"},
        "status": {"ru": "Завершено", "en": "Completed"},
        "description": {
            "ru": (
                "Успешное строительство установки комплексной подготовки газа (УКПГ) "
                "с проектной мощностью по очищенному газу 250 млн м³/год и по газовому конденсату 40 тыс. т/год."
            ),
            "en": (
                "Successful construction of a gas treatment unit with a design capacity of "
                "250 million m3/year of treated gas and 40 thousand tonnes/year of gas condensate."
            ),
        },
        "achievements": [
            {
                "ru": "Получено разрешение на ввод в промышленную эксплуатацию в 4 квартале 2017 г.",
                "en": "Commissioning approval was received in Q4 2017.",
            },
            {
                "ru": "Проектная мощность достигнута.",
                "en": "The design production capacity was achieved.",
            },
            {
                "ru": "Все работы выполнены в срок.",
                "en": "All work was completed on schedule.",
            },
        ],
    },
    {
        "blue_left": False,
        "blue_height_px": 155.96,
        "period": "2016-2018",
        "project_title": {"ru": "Обустройство месторождения", "en": "Field Development Infrastructure"},
        "status": {"ru": "Завершено", "en": "Completed"},
        "description": {
            "ru": (
                "Комплексные работы на Южно-Кисловском газоконденсатном месторождении, включая создание "
                "необходимой инфраструктуры, подготовку промысловых объектов и инженерных коммуникаций."
            ),
            "en": (
                "Comprehensive works at the Yuzhno-Kislovskoe gas-condensate field, including "
                "infrastructure development, site preparation, and engineering utilities."
            ),
        },
        "achievements": [
            {"ru": "Создана необходимая инфраструктура.", "en": "The required infrastructure was created."},
            {"ru": "Проложены трубопроводы и инженерные сети.", "en": "Pipelines and utility networks were installed."},
            {"ru": "Обеспечена промышленная безопасность.", "en": "Industrial safety requirements were ensured."},
        ],
    },
    {
        "blue_left": True,
        "blue_height_px": 187.96,
        "period": "2012-2014",
        "project_title": {"ru": "Сейсморазведочные работы МОГТ-3D", "en": "3D Seismic Survey Program"},
        "status": {"ru": "Завершено", "en": "Completed"},
        "description": {
            "ru": (
                "Проведение сейсморазведочных работ МОГТ-3D для уточнения геологического строения месторождения "
                "и оценки запасов углеводородного сырья."
            ),
            "en": (
                "3D seismic exploration work performed to refine the geological structure of the field "
                "and reassess hydrocarbon reserves."
            ),
        },
        "achievements": [
            {"ru": "Обработана площадь 63 км².", "en": "An area of 63 km2 was processed."},
            {"ru": "Получена детальная модель месторождения.", "en": "A detailed field model was created."},
            {"ru": "Уточнены запасы углеводородного сырья.", "en": "Hydrocarbon reserves were refined."},
        ],
    },
    {
        "blue_left": False,
        "blue_height_px": 187.96,
        "period": "2008-2011",
        "project_title": {"ru": "Расконсервация и освоение скважин", "en": "Well Reactivation and Appraisal"},
        "status": {"ru": "Завершено", "en": "Completed"},
        "description": {
            "ru": (
                "Работы по расконсервации и изучению дебита скважин в целях подготовки "
                "к опытно-промышленной эксплуатации."
            ),
            "en": (
                "Well reactivation and productivity assessment completed to prepare the field "
                "for pilot industrial operation."
            ),
        },
        "achievements": [
            {"ru": "Выполнена расконсервация скважин.", "en": "Wells were brought back into operation."},
            {"ru": "Изучены дебитные возможности.", "en": "Flow rate capabilities were evaluated."},
            {"ru": "Месторождение подготовлено к вводу в эксплуатацию.", "en": "The field was prepared for commissioning."},
        ],
    },
    {
        "blue_left": True,
        "blue_height_px": 219.97,
        "period": "2019-2020",
        "project_title": {
            "ru": "Геолого-разведочные работы в северной части месторождения",
            "en": "Exploration Works in the Northern Part of the Field",
        },
        "status": {"ru": "Завершено", "en": "Completed"},
        "description": {
            "ru": (
                "Проведение геолого-разведочных работ в северной части месторождения с целью увеличения "
                "ресурсной базы и оценки перспектив дальнейшей разработки."
            ),
            "en": (
                "Exploration works in the northern part of the field aimed at increasing the resource base "
                "and evaluating further development potential."
            ),
        },
        "achievements": [
            {"ru": "Планируемое увеличение ресурсной базы.", "en": "The resource base expansion was prepared."},
            {"ru": "Оценка новых перспективных участков.", "en": "New prospective zones were assessed."},
            {"ru": "Подготовка к бурению новых скважин.", "en": "Preparations were made for drilling new wells."},
        ],
    },
    {
        "blue_left": False,
        "blue_height_px": 219.97,
        "period": "2019",
        "project_title": {
            "ru": "Ввод в эксплуатацию разведочной скважины №12",
            "en": "Commissioning of Exploration Well No. 12",
        },
        "status": {"ru": "Завершено", "en": "Completed"},
        "description": {
            "ru": (
                "Планируемый ввод в промышленную эксплуатацию разведочной скважины №11 "
                "Южно-Кисловского газоконденсатного месторождения."
            ),
            "en": (
                "Planned commissioning of exploration well No. 11 at the Yuzhno-Kislovskoe "
                "gas-condensate field."
            ),
        },
        "achievements": [
            {"ru": "Завершение бурения скважины.", "en": "Well drilling was completed."},
            {"ru": "Подготовка к промышленной эксплуатации.", "en": "The site was prepared for industrial operation."},
            {"ru": "Расширение производственных мощностей.", "en": "Production capacity was expanded."},
        ],
    },
]

_WORKS_KPIS = [
    {"value": "6+", "label": {"ru": "Крупных проектов", "en": "Major projects"}},
    {"value": "250", "label_html": {"ru": "Млн м<sup>3</sup>/год мощность", "en": "Million m<sup>3</sup>/year capacity"}},
    {"value": "63", "label_html": {"ru": "км<sup>2</sup> площадь 3D", "en": "km<sup>2</sup> of 3D survey area"}},
    {"value": "2017", "label": {"ru": "Ввод УКПГ", "en": "Gas treatment launch"}},
]

_NEWS_LIST_PAGE_SIZE = 6

_NEWS_ARTICLES_RAW = [
    {
        "iso_date": "2017-06-30",
        "date_display": {"ru": "30 июня 2017", "en": "June 30, 2017"},
        "category": {"ru": "Производство", "en": "Production"},
        "title": {"ru": "Завершение строительства УКПГ", "en": "Gas Treatment Unit Construction Completed"},
        "excerpt": {
            "ru": (
                "Введён в эксплуатацию комплекс подготовки газа: достигнута проектная мощность по очищенному газу "
                "и конденсату, обеспечена готовность технологических линий к промышленной нагрузке."
            ),
            "en": (
                "The gas treatment complex was commissioned: the design capacity for treated gas and condensate "
                "was achieved, and the process lines were prepared for industrial load."
            ),
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2019-12-15",
        "date_display": {"ru": "15 декабря 2019", "en": "December 15, 2019"},
        "category": {"ru": "Корпоративные новости", "en": "Corporate News"},
        "title": {"ru": "Подписание соглашения о сотрудничестве с вузами региона", "en": "Cooperation Agreement Signed with Regional Universities"},
        "excerpt": {
            "ru": "Закреплены направления подготовки кадров, практики для студентов и совместные научно-исследовательские работы.",
            "en": "Key areas for staff training, student internships, and joint research work were formalized.",
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2018-09-03",
        "date_display": {"ru": "3 сентября 2018", "en": "September 3, 2018"},
        "category": {"ru": "Геологоразведка", "en": "Exploration"},
        "title": {"ru": "Завершение съёмки 3D на ключевом участке месторождения", "en": "3D Survey Completed on a Key Section of the Field"},
        "excerpt": {
            "ru": "Обработаны полевые материалы; обновлена геологическая модель для уточнения запасов и проектирования скважин.",
            "en": "Field data was processed and the geological model was updated for reserve refinement and well planning.",
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2026-03-18",
        "date_display": {"ru": "18 марта 2026", "en": "March 18, 2026"},
        "category": {"ru": "Производство", "en": "Production"},
        "title": {"ru": "Итоги производственного совещания за I квартал", "en": "Q1 Production Meeting Results"},
        "excerpt": {
            "ru": "Обсуждены показатели добычи, график ТОР и меры по снижению простоев оборудования на объектах подготовки газа.",
            "en": "Production indicators, maintenance schedules, and measures to reduce downtime at gas treatment facilities were reviewed.",
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2026-02-27",
        "date_display": {"ru": "27 февраля 2026", "en": "February 27, 2026"},
        "category": {"ru": "Корпоративные новости", "en": "Corporate News"},
        "title": {"ru": "Обновление регламента допуска на опасные объекты", "en": "Updated Access Regulations for Hazardous Facilities"},
        "excerpt": {
            "ru": "Вступают в силу уточнённые процедуры инструктажа и контроля персонала подрядных организаций на площадке.",
            "en": "Revised briefing and contractor personnel control procedures at hazardous sites have come into effect.",
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2026-02-05",
        "date_display": {"ru": "5 февраля 2026", "en": "February 5, 2026"},
        "category": {"ru": "Геологоразведка", "en": "Exploration"},
        "title": {"ru": "Участие в региональной ярмарке вакансий", "en": "Participation in the Regional Career Fair"},
        "excerpt": {
            "ru": "Компания представила программы стажировок и открытые позиции для инженерно-технических специальностей.",
            "en": "The company presented internship programs and current openings for engineering and technical specialists.",
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2026-01-20",
        "date_display": {"ru": "20 января 2026", "en": "January 20, 2026"},
        "category": {"ru": "Производство", "en": "Production"},
        "title": {"ru": "План мероприятий по охране труда на год", "en": "Annual Occupational Safety Action Plan"},
        "excerpt": {
            "ru": "Утверждены сроки учебных сборов, проверок средств индивидуальной защиты и внешних аудитов подрядчиков.",
            "en": "Training sessions, PPE inspections, and external contractor audits were approved for the year.",
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2016-11-22",
        "date_display": {"ru": "22 ноября 2016", "en": "November 22, 2016"},
        "category": {"ru": "Корпоративные новости", "en": "Corporate News"},
        "title": {"ru": "Награда отрасли за реализацию проекта модернизации", "en": "Industry Award for Modernization Project"},
        "excerpt": {
            "ru": "Отмечены результаты внедрения системы мониторинга технологических параметров и снижения энергозатрат.",
            "en": "The project was recognized for implementing process monitoring systems and reducing energy consumption.",
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2020-04-10",
        "date_display": {"ru": "10 апреля 2020", "en": "April 10, 2020"},
        "category": {"ru": "Геологоразведка", "en": "Exploration"},
        "title": {"ru": "Интерпретация данных ГИС по разведочным скважинам", "en": "Well Logging Data Interpretation for Exploration Wells"},
        "excerpt": {
            "ru": "Подготовлен отчёт для включения в материалы государственной экспертизы запасов углеводородного сырья.",
            "en": "A report was prepared for inclusion in the state expertise package on hydrocarbon reserves.",
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2025-11-10",
        "date_display": {"ru": "10 ноября 2025", "en": "November 10, 2025"},
        "category": {"ru": "Производство", "en": "Production"},
        "title": {"ru": "Внешний аудит системы промышленной безопасности", "en": "External Audit of the Industrial Safety System"},
        "excerpt": {
            "ru": "Завершена проверка документации, режимов эксплуатации оборудования и готовности к плановым испытаниям защитных систем.",
            "en": "Documentation, operating modes, and readiness for scheduled safety system tests were audited.",
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2025-09-01",
        "date_display": {"ru": "1 сентября 2025", "en": "September 1, 2025"},
        "category": {"ru": "Корпоративные новости", "en": "Corporate News"},
        "title": {"ru": "Расширение программы поддержки семей сотрудников", "en": "Expanded Employee Family Support Program"},
        "excerpt": {
            "ru": "Добавлены направления по оздоровлению детей, скидкам на спорт и участию в корпоративных мероприятиях региона.",
            "en": "New benefits include children's wellness support, sports discounts, and participation in regional corporate events.",
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2025-08-15",
        "date_display": {"ru": "15 августа 2025", "en": "August 15, 2025"},
        "category": {"ru": "Геологоразведка", "en": "Exploration"},
        "title": {"ru": "Старт разведочной скважины на лицензионном участке", "en": "Exploration Well Started on the Licensed Block"},
        "excerpt": {
            "ru": "Проект прошёл внутреннюю приёмку; бурение ведётся с соблюдением экологических норм и графика цикличности.",
            "en": "The project passed internal acceptance, and drilling is proceeding in line with environmental standards and the approved schedule.",
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2025-06-20",
        "date_display": {"ru": "20 июня 2025", "en": "June 20, 2025"},
        "category": {"ru": "Производство", "en": "Production"},
        "title": {"ru": "Модернизация узла компрессорной подготовки газа", "en": "Modernization of the Gas Compression Preparation Unit"},
        "excerpt": {
            "ru": "Установлено новое оборудование контроля вибрации и температуры подшипников; повышена надёжность работы агрегатов.",
            "en": "New vibration and bearing temperature monitoring equipment was installed, improving unit reliability.",
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2025-07-05",
        "date_display": {"ru": "5 июля 2025", "en": "July 5, 2025"},
        "category": {"ru": "Корпоративные новости", "en": "Corporate News"},
        "title": {"ru": "Итоги экологического мониторинга за I полугодие", "en": "Environmental Monitoring Results for H1"},
        "excerpt": {
            "ru": "Показатели сброса и выбросов в пределах установленных лимитов; отчётность перед контролирующими органами сдана в срок.",
            "en": "Discharge and emission figures remained within limits, and all reports were submitted on time to regulators.",
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2024-12-12",
        "date_display": {"ru": "12 декабря 2024", "en": "December 12, 2024"},
        "category": {"ru": "Геологоразведка", "en": "Exploration"},
        "title": {"ru": "Материалы по запасам переданы на государственную экспертизу", "en": "Reserve Materials Submitted for State Review"},
        "excerpt": {
            "ru": "Сформирован пакет геологических моделей и таблиц расчёта; готовность к рассмотрению подтверждена независимым аудитом.",
            "en": "A package of geological models and calculation tables was prepared and verified by an independent audit.",
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2024-10-30",
        "date_display": {"ru": "30 октября 2024", "en": "October 30, 2024"},
        "category": {"ru": "Производство", "en": "Production"},
        "title": {"ru": "Ввод объекта вспомогательной инфраструктуры безопасности", "en": "Commissioning of Auxiliary Safety Infrastructure"},
        "excerpt": {
            "ru": "Обеспечены резервные маршруты эвакуации и связи; проведены учения с привлечением подрядных организаций.",
            "en": "Backup evacuation and communication routes were introduced, and drills with contractors were conducted.",
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2024-05-18",
        "date_display": {"ru": "18 мая 2024", "en": "May 18, 2024"},
        "category": {"ru": "Корпоративные новости", "en": "Corporate News"},
        "title": {"ru": "День открытых дверей для школьников региона", "en": "Open Day for Local School Students"},
        "excerpt": {
            "ru": "Экскурсии по учебным стендам и встречи с инженерами: знакомство с профессиями нефтегазовой отрасли и требованиями ТБ.",
            "en": "Students toured training stands and met engineers to learn about oil and gas careers and safety requirements.",
        },
        "detail_url": "#",
    },
    {
        "iso_date": "2024-03-22",
        "date_display": {"ru": "22 марта 2024", "en": "March 22, 2024"},
        "category": {"ru": "Геологоразведка", "en": "Exploration"},
        "title": {"ru": "Архивация сейсмических материалов прошлых сезонов", "en": "Archiving Seismic Materials from Previous Seasons"},
        "excerpt": {
            "ru": "Данные структурированы для повторной обработки; обновлён каталог носителей и доступ для проектных команд.",
            "en": "The data was organized for reprocessing, and the media catalog and project team access were updated.",
        },
        "detail_url": "#",
    },
]

_GALLERY_CATEGORY_OPTIONS = [
    {"id": "all", "label": {"ru": "Все", "en": "All"}},
    {"id": "production", "label": {"ru": "Производство", "en": "Production"}},
    {"id": "infrastructure", "label": {"ru": "Инфраструктура", "en": "Infrastructure"}},
    {"id": "drilling", "label": {"ru": "Бурение", "en": "Drilling"}},
    {"id": "team", "label": {"ru": "Команда", "en": "Team"}},
    {"id": "office", "label": {"ru": "Офис", "en": "Office"}},
]

_GALLERY_INITIAL_VISIBLE = 8

_GALLERY_ITEMS_RAW = [
    ("img/news/news-01.png", {"ru": "Промышленный комплекс", "en": "Industrial complex"}, "production"),
    ("img/news/news-02.png", {"ru": "Трубопроводное оборудование", "en": "Pipeline equipment"}, "infrastructure"),
    ("img/news/news-03.png", {"ru": "Узел подготовки", "en": "Processing unit"}, "production"),
    ("img/news/news-04.png", {"ru": "Буровая установка", "en": "Drilling rig"}, "drilling"),
    ("img/news/news-05.png", {"ru": "Специалист на объекте", "en": "Field specialist"}, "team"),
    ("img/news/news-06.png", {"ru": "Офисное здание", "en": "Office building"}, "office"),
    ("img/home-about.jpg", {"ru": "Месторождение", "en": "Field site"}, "drilling"),
    ("img/home-hero.jpg", {"ru": "Производственная площадка", "en": "Production site"}, "production"),
    ("img/news/news-02.png", {"ru": "Инженерные коммуникации", "en": "Engineering utilities"}, "infrastructure"),
    ("img/news/news-04.png", {"ru": "Работы на кусте", "en": "Operations at the well pad"}, "drilling"),
    ("img/news/news-05.png", {"ru": "Команда проекта", "en": "Project team"}, "team"),
    ("img/news/news-06.png", {"ru": "Переговорная", "en": "Meeting room"}, "office"),
    ("img/news/news-01.png", {"ru": "Цех подготовки", "en": "Preparation workshop"}, "production"),
    ("img/news/news-03.png", {"ru": "Контрольно-измерительные приборы", "en": "Instrumentation"}, "infrastructure"),
    ("img/news/news-04.png", {"ru": "Разведка участка", "en": "Site exploration"}, "drilling"),
    ("img/home-hero.jpg", {"ru": "Инфраструктура объекта", "en": "Facility infrastructure"}, "infrastructure"),
]
_gallery_test_dup = list(_GALLERY_ITEMS_RAW)
_GALLERY_ITEMS_RAW = _GALLERY_ITEMS_RAW + _gallery_test_dup


def home(request):
    return render(request, "pages/home.html")


def about(request):
    language = _language_code()
    return render(request, "pages/empty.html", {"page_title": _PAGE_TITLES["about"][language]})


def works(request):
    language = _language_code()
    timeline = [_localize(item, language) for item in _WORKS_TIMELINE]
    kpis = [_localize(item, language) for item in _WORKS_KPIS]
    context = {
        "page_title": {"ru": "Наши работы", "en": "Our Works"}[language],
        "hero_title": {"ru": "Наши работы", "en": "Our Works"}[language],
        "hero_subtitle": {
            "ru": "Основные проекты и достижения компании",
            "en": "Key company projects and achievements",
        }[language],
        "realized_title": {"ru": "Реализованные проекты", "en": "Completed Projects"}[language],
        "realized_lead": {
            "ru": "За годы работы мы успешно реализовали множество проектов по разработке месторождения и созданию производственной инфраструктуры",
            "en": "Over the years, we have successfully delivered numerous projects related to field development and production infrastructure.",
        }[language],
        "timeline": timeline,
        "kpi_section_title": {"ru": "Ключевые показатели", "en": "Key Metrics"}[language],
        "kpis": kpis,
        "cta_title": {"ru": "Заинтересованы в сотрудничестве?", "en": "Interested in cooperation?"}[language],
        "cta_subtitle": {
            "ru": "Свяжитесь с нами для обсуждения возможностей партнёрства",
            "en": "Contact us to discuss partnership opportunities",
        }[language],
    }
    return render(request, "pages/works.html", context)


def press(request):
    language = _language_code()
    return render(request, "pages/empty.html", {"page_title": _PAGE_TITLES["press"][language]})


def career(request):
    vacancies = Vacancy.objects.filter(is_active=True)
    return render(request, "pages/career.html", {"vacancies": vacancies})


def contacts(request):
    return render(request, "pages/contacts.html")


def about_company(request):
    return render(request, "pages/about_company.html")


def about_field(request):
    return render(request, "pages/about_field.html")


def about_team(request):
    return render(request, "pages/about_team.html")


def about_license(request):
    return render(request, "pages/about_license.html")


def about_tour(request):
    return render(request, "pages/about_tour.html")


def press_news(request):
    language = _language_code()
    localized_articles = [
        {**_localize(row, language), "image": f"img/news/news-{(index % 6) + 1:02d}.png"}
        for index, row in enumerate(_NEWS_ARTICLES_RAW)
    ]
    paginator = Paginator(localized_articles, _NEWS_LIST_PAGE_SIZE)
    news_page = paginator.get_page(request.GET.get("page") or 1)
    context = {
        "page_title": {"ru": "Новости", "en": "News"}[language],
        "hero_title": {"ru": "Новости", "en": "News"}[language],
        "hero_subtitle": {
            "ru": "Последние события и достижения компании",
            "en": "Latest company events and achievements",
        }[language],
        "news_page": news_page,
        "news_cta_title": {
            "ru": "Хотите быть в курсе всех новостей?",
            "en": "Want to stay updated on all the news?",
        }[language],
        "news_cta_subtitle": {
            "ru": "Следите за нашими обновлениями и достижениями",
            "en": "Follow our updates and achievements",
        }[language],
        "news_cta_button": {"ru": "Перейти в галерею", "en": "Open Gallery"}[language],
    }
    return render(request, "pages/news.html", context)


def press_gallery(request):
    language = _language_code()
    categories = [_localize(item, language) for item in _GALLERY_CATEGORY_OPTIONS]
    gallery_items = [
        {"src": src, "alt": _localize(alt, language), "category": category}
        for src, alt, category in _GALLERY_ITEMS_RAW
    ]
    category = (request.GET.get("category") or "all").strip()
    valid_ids = {item["id"] for item in categories}
    if category not in valid_ids:
        category = "all"
    filtered = gallery_items if category == "all" else [row for row in gallery_items if row["category"] == category]
    context = {
        "page_title": {"ru": "Галерея", "en": "Gallery"}[language],
        "hero_title": {"ru": "Галерея", "en": "Gallery"}[language],
        "hero_subtitle": {
            "ru": "Фотографии нашей работы и достижений",
            "en": "Photos of our work and achievements",
        }[language],
        "gallery_items": filtered,
        "gallery_categories": categories,
        "gallery_category_active": category,
        "gallery_initial_visible": _GALLERY_INITIAL_VISIBLE,
    }
    return render(request, "pages/gallery.html", context)
