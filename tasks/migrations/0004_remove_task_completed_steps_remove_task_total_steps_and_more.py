# Generated by Django 5.1.4 on 2024-12-20 12:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_task_completed_steps_task_total_steps'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='completed_steps',
        ),
        migrations.RemoveField(
            model_name='task',
            name='total_steps',
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_completed', models.BooleanField(default=False)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='tasks.task')),
            ],
        ),
    ]