# Generated by Django 4.0.7 on 2022-12-20 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manito', '0005_manitoaccount_my_balance_manitoaccount_your_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='manitoaccount',
            name='balance',
            field=models.IntegerField(default=-1),
        ),
    ]