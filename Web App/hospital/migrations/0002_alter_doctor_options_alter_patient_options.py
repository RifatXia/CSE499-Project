# Generated by Django 4.0.5 on 2023-10-31 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctor',
            options={'verbose_name_plural': 'Doctors'},
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={'verbose_name_plural': 'Patients'},
        ),
    ]