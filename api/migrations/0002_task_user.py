from django.conf import settings
from django.db import migrations, models


def clear_tasks(apps, schema_editor):
    apps.get_model("api", "Task").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(clear_tasks, migrations.RunPython.noop),
        migrations.AddField(
            model_name="task",
            name="user",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name="tasks",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
