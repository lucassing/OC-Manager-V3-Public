# Generated by Django 2.1.15 on 2020-01-28 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connection', '0005_auto_20200127_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection_db',
            name='connected',
            field=models.BooleanField(default=False),
        ),
    ]
