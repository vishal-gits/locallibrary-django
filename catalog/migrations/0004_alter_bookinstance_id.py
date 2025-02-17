# Generated by Django 5.1.4 on 2024-12-10 06:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_rename_date_of_detath_author_date_of_death'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique ID for for this particular book across the whole library', primary_key=True, serialize=False),
        ),
    ]
