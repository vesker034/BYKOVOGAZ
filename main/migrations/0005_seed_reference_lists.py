from django.db import migrations


def forwards(apps, schema_editor):
    CandidateStatus = apps.get_model("main", "CandidateStatus")
    Role = apps.get_model("main", "Role")
    for label in ("Новая", "В рассмотрении", "Отклонена"):
        CandidateStatus.objects.get_or_create(name=label)
    for label in ("admin", "moderator"):
        Role.objects.get_or_create(name=label)


def backwards(apps, schema_editor):
    CandidateStatus = apps.get_model("main", "CandidateStatus")
    Role = apps.get_model("main", "Role")
    CandidateStatus.objects.filter(name__in=["Новая", "В рассмотрении", "Отклонена"]).delete()
    Role.objects.filter(name__in=["admin", "moderator"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_schema_plan_db"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
