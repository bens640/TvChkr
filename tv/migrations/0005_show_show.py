# Generated by Django 3.1.3 on 2020-11-16 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tv', '0004_auto_20201114_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='show',
            field=models.IntegerField(default=456),
            preserve_default=False,
        ),
    ]