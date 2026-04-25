from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Vacancy",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Название вакансии")),
                ("department", models.CharField(max_length=160, verbose_name="Подразделение")),
                ("location", models.CharField(blank=True, max_length=160, verbose_name="Локация")),
                (
                    "employment_type",
                    models.CharField(
                        choices=[
                            ("full_time", "Полная занятость"),
                            ("shift", "Сменный график"),
                            ("part_time", "Частичная занятость"),
                            ("internship", "Стажировка"),
                        ],
                        default="full_time",
                        max_length=20,
                        verbose_name="Формат работы",
                    ),
                ),
                ("summary", models.TextField(verbose_name="Краткое описание")),
                (
                    "requirements",
                    models.TextField(
                        help_text="Укажите каждый пункт с новой строки.",
                        verbose_name="Требования",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Показывать на сайте")),
                ("display_order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
            ],
            options={
                "verbose_name": "Вакансия",
                "verbose_name_plural": "Вакансии",
                "ordering": ["display_order", "-created_at", "title"],
            },
        ),
    ]
