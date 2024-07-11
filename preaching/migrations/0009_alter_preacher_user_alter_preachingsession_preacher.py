# Generated by Django 5.0.6 on 2024-07-09 12:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preaching', '0008_alter_preachingsession_session_time_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='preacher',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='preachingsession',
            name='preacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preaching.preacher'),
        ),
    ]
