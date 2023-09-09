# Generated by Django 4.2.4 on 2023-09-05 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journalentries',
            name='id',
        ),
        migrations.AddField(
            model_name='journalentries',
            name='voucherCode',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='journalentries',
            name='s_no',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]