# Generated by Django 2.2.1 on 2019-05-28 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_task_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='result',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
