# Generated by Django 5.1.6 on 2025-02-27 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0005_rename_subtask_subtask_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='progress',
            field=models.CharField(choices=[('todo', 'To Do'), ('in progress', 'In Progress'), ('await feedback', 'Await Feedback'), ('done', 'Done')], default='todo', max_length=20),
        ),
    ]
