# Generated by Django 4.0.5 on 2023-10-20 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0004_doctor_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='image',
            field=models.ImageField(default='static/images/ai.jpg', upload_to='Web App\\static\\images\\doctor_images'),
        ),
    ]