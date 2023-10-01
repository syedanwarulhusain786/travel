# Generated by Django 4.2.4 on 2023-09-30 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_number', models.PositiveIntegerField()),
                ('group_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ledger_number', models.PositiveIntegerField()),
                ('ledger_name', models.CharField(max_length=255)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.group')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('date', models.DateField()),
                ('s_no', models.AutoField(primary_key=True, serialize=False)),
                ('voucherNo', models.IntegerField()),
                ('voucherCode', models.CharField(max_length=255)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('bank', 'Bank')], max_length=10)),
                ('amount_in_words', models.CharField(max_length=255)),
                ('amount_in_numbers', models.DecimalField(decimal_places=2, max_digits=10)),
                ('received_from', models.CharField(max_length=255)),
                ('remarks', models.TextField(blank=True)),
                ('narration', models.CharField(max_length=255)),
                ('ledger', models.CharField(max_length=255)),
                ('primary_group', models.CharField(max_length=255)),
                ('group', models.CharField(max_length=255)),
                ('reference_bill_number', models.CharField(max_length=255)),
                ('reference_bill_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('credit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_currency', models.CharField(max_length=3)),
                ('clearance_date', models.DateField(blank=True, null=True)),
                ('transaction_type', models.CharField(blank=True, max_length=10, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('cheque_no', models.CharField(blank=True, max_length=20, null=True)),
                ('bank_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Primary_Group',
            fields=[
                ('primary_group_number', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('primary_group_name', models.CharField(max_length=255)),
                ('primary_group_type', models.CharField(choices=[('Debit', 'Debit'), ('Credit', 'Credit')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('date', models.DateField()),
                ('s_no', models.AutoField(primary_key=True, serialize=False)),
                ('voucherNo', models.IntegerField()),
                ('voucherCode', models.CharField(max_length=255)),
                ('receipt_method', models.CharField(choices=[('cash', 'Cash'), ('bank', 'Bank')], max_length=10)),
                ('amount_in_words', models.CharField(max_length=255)),
                ('amount_in_numbers', models.DecimalField(decimal_places=2, max_digits=10)),
                ('received_from', models.CharField(max_length=255)),
                ('remarks', models.TextField(blank=True)),
                ('narration', models.CharField(max_length=255)),
                ('ledger', models.CharField(max_length=255)),
                ('primary_group', models.CharField(max_length=255)),
                ('group', models.CharField(max_length=255)),
                ('reference_bill_number', models.CharField(max_length=255)),
                ('reference_bill_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('debit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_currency', models.CharField(max_length=3)),
                ('clearance_date', models.DateField(blank=True, null=True)),
                ('transaction_type', models.CharField(blank=True, max_length=10, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('cheque_no', models.CharField(blank=True, max_length=20, null=True)),
                ('bank_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SalesReceipt',
            fields=[
                ('date', models.DateField()),
                ('s_no', models.AutoField(primary_key=True, serialize=False)),
                ('voucherNo', models.IntegerField()),
                ('voucherCode', models.CharField(max_length=255)),
                ('decsription', models.CharField(max_length=400)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cred_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_group_salesreceipts', to='accounting.group')),
                ('cred_ledger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_ledger_salesreceipts', to='accounting.ledger')),
                ('cred_primary_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_primary_group_salesreceipts', to='accounting.primary_group')),
                ('deb_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debit_group_salesreceipts', to='accounting.group')),
                ('deb_ledger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debit_ledger_salesreceipts', to='accounting.ledger')),
                ('deb_primary_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debit_primary_group_salesreceipts', to='accounting.primary_group')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseReceipt',
            fields=[
                ('date', models.DateField()),
                ('s_no', models.AutoField(primary_key=True, serialize=False)),
                ('voucherNo', models.IntegerField()),
                ('voucherCode', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=400)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bill_no', models.CharField(max_length=255)),
                ('cred_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_group_purchasereceipts', to='accounting.group')),
                ('cred_ledger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_ledger_purchasereceipts', to='accounting.ledger')),
                ('cred_primary_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_primary_group_purchasereceipts', to='accounting.primary_group')),
                ('deb_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debit_group_purchasereceipts', to='accounting.group')),
                ('deb_ledger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debit_ledger_purchasereceipts', to='accounting.ledger')),
                ('deb_primary_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debit_primary_group_purchasereceipts', to='accounting.primary_group')),
            ],
        ),
        migrations.CreateModel(
            name='JournalEntries',
            fields=[
                ('s_no', models.AutoField(primary_key=True, serialize=False)),
                ('voucherNo', models.IntegerField()),
                ('voucherCode', models.CharField(max_length=255)),
                ('date', models.DateField(auto_now_add=True)),
                ('invoice_no', models.CharField(blank=True, max_length=255)),
                ('invoice_date', models.DateField(blank=True, null=True)),
                ('narration', models.CharField(blank=True, max_length=255, null=True)),
                ('debit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('credit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.group')),
                ('ledger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.ledger')),
                ('primary_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.primary_group')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='primary_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.primary_group'),
        ),
    ]
