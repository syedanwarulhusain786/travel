# Generated by Django 4.2.4 on 2023-09-05 23:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0005_alter_journalentries_voucherno'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journalentries',
            name='comments',
        ),
    ]
