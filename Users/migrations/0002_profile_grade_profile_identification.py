# Generated by Django 5.1.6 on 2025-04-22 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='grade',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='identification',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
