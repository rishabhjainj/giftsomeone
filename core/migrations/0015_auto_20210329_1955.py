# Generated by Django 3.1.6 on 2021-03-29 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20210329_1947'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='billing',
            new_name='billing_address',
        ),
    ]
