# Generated by Django 3.1.6 on 2021-03-23 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210323_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
