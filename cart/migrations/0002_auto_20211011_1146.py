# Generated by Django 3.2.7 on 2021-10-11 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]
