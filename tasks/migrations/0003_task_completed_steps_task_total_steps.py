# Generated by Django 5.1.4 on 2024-12-20 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed_steps',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='total_steps',
            field=models.IntegerField(default=1),
        ),
    ]
