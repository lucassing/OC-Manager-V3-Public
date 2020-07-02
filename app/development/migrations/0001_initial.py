# Generated by Django 3.0.5 on 2020-07-02 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sampleapp', '0020_auto_20200617_1501'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BandSettings_Dev_Db',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume', models.DecimalField(decimal_places=1, max_digits=5, null=True)),
                ('printBothways', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='MovementSettings_Dev_Db',
            fields=[
                ('movementsettings_db_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sampleapp.MovementSettings_Db')),
            ],
            bases=('sampleapp.movementsettings_db',),
        ),
        migrations.CreateModel(
            name='PlateProperties_Dev_Db',
            fields=[
                ('plateproperties_db_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sampleapp.PlateProperties_Db')),
            ],
            bases=('sampleapp.plateproperties_db',),
        ),
        migrations.CreateModel(
            name='PressureSettings_Dev_Db',
            fields=[
                ('pressuresettings_db_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sampleapp.PressureSettings_Db')),
            ],
            bases=('sampleapp.pressuresettings_db',),
        ),
        migrations.CreateModel(
            name='Development_Db',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=120, null=True)),
                ('auth', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('developmentband_settings', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='development.BandSettings_Dev_Db')),
                ('movement_settings', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='sampleapp.MovementSettings_Db')),
                ('plate_properties', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='sampleapp.PlateProperties_Db')),
                ('pressure_settings', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='sampleapp.PressureSettings_Db')),
            ],
        ),
    ]
