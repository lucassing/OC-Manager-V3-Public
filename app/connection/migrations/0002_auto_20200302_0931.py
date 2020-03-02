# Generated by Django 3.0.3 on 2020-03-02 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('connection', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connection_db',
            name='auth',
        ),
        migrations.AddField(
            model_name='connection_db',
            name='auth_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]