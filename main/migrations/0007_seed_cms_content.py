from django.db import migrations

from main.cms_seed import apply_seed


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_cms_content_models"),
    ]

    operations = [
        migrations.RunPython(apply_seed, migrations.RunPython.noop),
    ]
