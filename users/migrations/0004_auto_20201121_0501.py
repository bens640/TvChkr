# Generated by Django 3.1.3 on 2020-11-21 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201117_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='about',
            field=models.CharField(default='', max_length=200),
        ),
    ]
