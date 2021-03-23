# Generated by Django 3.1.6 on 2021-03-23 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20210323_1737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='date',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='price',
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
