# Generated by Django 4.0.5 on 2023-11-01 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0005_alter_schedule_day'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='day',
            new_name='days',
        ),
        migrations.AddField(
            model_name='doctor',
            name='days_available',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]
