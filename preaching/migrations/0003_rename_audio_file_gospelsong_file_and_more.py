# Generated by Django 5.0.6 on 2024-07-08 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preaching', '0002_gospelsong'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gospelsong',
            old_name='audio_file',
            new_name='file',
        ),
        migrations.AddField(
            model_name='gospelsong',
            name='media_type',
            field=models.CharField(choices=[('audio', 'Audio'), ('video', 'Video')], default='audio', max_length=5),
        ),
        migrations.AlterField(
            model_name='gospelsong',
            name='artist',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='gospelsong',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
