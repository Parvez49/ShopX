# Generated by Django 4.2.8 on 2023-12-16 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='referral_code',
            field=models.IntegerField(default=266861484566, editable=False, unique=True),
        ),
    ]