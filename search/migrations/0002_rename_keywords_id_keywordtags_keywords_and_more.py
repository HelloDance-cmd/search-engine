# Generated by Django 5.1.4 on 2025-01-02 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='keywordtags',
            old_name='keywords_id',
            new_name='keywords',
        ),
        migrations.RenameField(
            model_name='keywordtags',
            old_name='tags_id',
            new_name='tags',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='URL_id',
            new_name='URL',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='keywords_id',
            new_name='keywords',
        ),
        migrations.RenameField(
            model_name='url',
            old_name='keywords_id',
            new_name='keywords',
        ),
    ]
