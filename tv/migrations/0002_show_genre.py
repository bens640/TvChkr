# Generated by Django 3.1.3 on 2020-11-10 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tv', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='genre',
            field=models.CharField(default='none', max_length=100),
        ),
    ]
