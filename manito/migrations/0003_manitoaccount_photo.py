# Generated by Django 4.0.7 on 2022-12-20 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manito', '0002_manitoaccount_about_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='manitoaccount',
            name='photo',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
