# Generated by Django 3.2 on 2021-05-24 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Table', '0013_alter_restaurant_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='request',
            field=models.CharField(default='-', max_length=200),
        ),
    ]