# Generated by Django 4.0.7 on 2022-12-20 12:12

from django.db import migrations, models
import json.decoder
import json.encoder


class Migration(migrations.Migration):

    dependencies = [
        ('manito', '0004_alter_manitoaccount_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='manitoaccount',
            name='my_balance',
            field=models.JSONField(decoder=json.decoder.JSONDecoder, default=list, encoder=json.encoder.JSONEncoder),
        ),
        migrations.AddField(
            model_name='manitoaccount',
            name='your_balance',
            field=models.JSONField(decoder=json.decoder.JSONDecoder, default=list, encoder=json.encoder.JSONEncoder),
        ),
    ]
