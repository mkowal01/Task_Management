# Generated by Django 5.1.4 on 2025-01-08 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_remove_task_completed_steps_remove_task_total_steps_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
