# Generated by Django 3.1.6 on 2021-03-23 19:38

from django.db import migrations, models
import giftSomeone.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210323_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=giftSomeone.helpers.PathAndRenameFile('categories')),
        ),
    ]