# Generated by Django 4.2.4 on 2023-09-19 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0003_journalentries_invoice_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentries',
            name='invoice_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='journalentries',
            name='invoice_no',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]