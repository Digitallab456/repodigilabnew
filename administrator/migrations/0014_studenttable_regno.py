# Generated by Django 5.1.4 on 2025-02-08 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0013_delete_answertable'),
    ]

    operations = [
        migrations.AddField(
            model_name='studenttable',
            name='regno',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
