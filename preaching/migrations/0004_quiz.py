# Generated by Django 5.0.6 on 2024-07-08 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preaching', '0003_rename_audio_file_gospelsong_file_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('option1', models.CharField(max_length=255)),
                ('option2', models.CharField(max_length=255)),
                ('option3', models.CharField(max_length=255)),
                ('option4', models.CharField(max_length=255)),
                ('correct_option', models.CharField(max_length=255)),
            ],
        ),
    ]
