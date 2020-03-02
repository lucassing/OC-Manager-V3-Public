# Generated by Django 3.0.3 on 2020-02-25 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GcodeFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=100)),
                ('uploader', models.CharField(max_length=100)),
                ('gcode', models.FileField(upload_to='gcode/files')),
            ],
        ),
    ]