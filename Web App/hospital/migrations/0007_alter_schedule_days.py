# Generated by Django 4.0.5 on 2023-11-01 20:08

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_rename_day_schedule_days_doctor_days_available_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='days',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=500),
        ),
    ]