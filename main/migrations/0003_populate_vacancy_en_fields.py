from django.db import migrations


VACANCY_TRANSLATIONS = {
    "Инженер-технолог": {
        "title_en": "Process Engineer",
        "department_en": "Production and Technical Department",
        "location_en": "Volgograd, Bykovsky District",
        "summary_en": (
            "Control of gas and gas condensate processing operations, participation in supporting "
            "production processes, and analysis of equipment performance."
        ),
        "requirements_en": "\n".join(
            [
                "Higher technical education",
                "At least 1 year of relevant experience",
                "Knowledge of oil and gas industry process operations",
                "Ability to work with technical documentation",
                "Responsibility and attention to detail",
            ]
        ),
    },
    "Оператор технологических установок": {
        "title_en": "Process Equipment Operator",
        "department_en": "Production Unit",
        "location_en": "Bykovsky District, Volgograd Region",
        "summary_en": (
            "Operation of process equipment, monitoring of unit performance parameters, and support "
            "for a stable production process."
        ),
        "requirements_en": "\n".join(
            [
                "Secondary vocational or higher technical education",
                "Production experience will be an advantage",
                "Knowledge of industrial safety rules",
                "Readiness to work in production conditions",
                "Discipline and reliability",
            ]
        ),
    },
    "Инженер по охране труда и промышленной безопасности": {
        "title_en": "Occupational Health and Industrial Safety Engineer",
        "department_en": "Occupational Health and Industrial Safety Service",
        "location_en": "Volgograd",
        "summary_en": (
            "Organization and control of occupational, industrial, and fire safety activities, "
            "including briefings and inspection support."
        ),
        "requirements_en": "\n".join(
            [
                "Higher education",
                "Experience in occupational health or industrial safety",
                "Knowledge of the regulatory framework of the Russian Federation",
                "Skills in preparing instructions and local regulations",
                "Attention to detail and a systematic approach",
            ]
        ),
    },
    "Электромеханик": {
        "title_en": "Electromechanic",
        "department_en": "Equipment Maintenance Service",
        "location_en": "Bykovsky District, Volgograd Region",
        "summary_en": (
            "Maintenance and repair of electrical and mechanical equipment, as well as monitoring "
            "the operability of production systems."
        ),
        "requirements_en": "\n".join(
            [
                "Secondary vocational or higher technical education",
                "Experience in equipment maintenance",
                "Ability to read electrical diagrams",
                "Fault diagnostics skills",
                "Responsibility and accuracy",
            ]
        ),
    },
}


def populate_vacancy_english_fields(apps, schema_editor):
    Vacancy = apps.get_model("main", "Vacancy")

    for title_ru, translated_values in VACANCY_TRANSLATIONS.items():
        try:
            vacancy = Vacancy.objects.get(title=title_ru)
        except Vacancy.DoesNotExist:
            continue

        updated = False
        for field_name, field_value in translated_values.items():
            if not getattr(vacancy, field_name):
                setattr(vacancy, field_name, field_value)
                updated = True

        if updated:
            vacancy.save(
                update_fields=[
                    "title_en",
                    "department_en",
                    "location_en",
                    "summary_en",
                    "requirements_en",
                ]
            )


def clear_vacancy_english_fields(apps, schema_editor):
    Vacancy = apps.get_model("main", "Vacancy")
    titles = list(VACANCY_TRANSLATIONS.keys())
    Vacancy.objects.filter(title__in=titles).update(
        title_en="",
        department_en="",
        location_en="",
        summary_en="",
        requirements_en="",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_vacancy_department_en_vacancy_location_en_and_more"),
    ]

    operations = [
        migrations.RunPython(populate_vacancy_english_fields, clear_vacancy_english_fields),
    ]
