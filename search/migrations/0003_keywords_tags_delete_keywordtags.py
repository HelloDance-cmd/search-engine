# Generated by Django 5.1.4 on 2025-01-02 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_rename_keywords_id_keywordtags_keywords_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='keywords',
            name='tags',
            field=models.ManyToManyField(to='search.tags'),
        ),
        migrations.DeleteModel(
            name='KeywordTags',
        ),
    ]
