from django.db import models

class Primary_Group(models.Model): #### Primary Group
    PRIMARY_GROUP_CHOICES = [
        ('Debit', 'Debit'),
        ('Credit', 'Credit'),
    ]
    primary_group_number = models.PositiveIntegerField(primary_key=True)  # Start from 100, 200, 300, ...
    primary_group_name = models.CharField(max_length=255)
    primary_group_type = models.CharField(
        max_length=10,
        choices=PRIMARY_GROUP_CHOICES,
    )
    def __str__(self):
        return f"{self.primary_group_name}"

    def save(self, *args, **kwargs):
        if not self.primary_group_number:
            latest_category = Primary_Group.objects.order_by('-primary_group_number').first()
            if latest_category:
                self.primary_group_number = latest_category.primary_group_number + 100
            else:
                self.primary_group_number = 100
        super(Primary_Group, self).save(*args, **kwargs)

class Group(models.Model): #### Group
    primary_group = models.ForeignKey(Primary_Group, on_delete=models.CASCADE)
    group_number = models.PositiveIntegerField()  # Start from 1 within each category
    group_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.group_name}"

    def save(self, *args, **kwargs):
        if not self.group_number:
            # Ensure subcategory_number is unique within each category
            latest_subcategory_in_category = Group.objects.filter(primary_group=self.primary_group).order_by('-group_number').first()
            if latest_subcategory_in_category:
                self.group_number = latest_subcategory_in_category.group_number + 1
            else:
                self.group_number = self.primary_group.primary_group_number+1
        super(Group, self).save(*args, **kwargs)

class Ledger(models.Model): #### Ledger
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    ledger_number = models.PositiveIntegerField()  # Start from 1 within each subcategory
    ledger_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ledger_name}"

    def save(self, *args, **kwargs):
        if not self.ledger_number:
            # Ensure account_number is unique within each subcategory
            latest_account_in_subcategory = Ledger.objects.filter(group=self.group).order_by('-ledger_number').first()
            if latest_account_in_subcategory:
                self.ledger_number = latest_account_in_subcategory.ledger_number + 1
            else:
                self.ledger_number = self.group.group_number*10+1
        super(Ledger, self).save(*args, **kwargs)
class JournalEntries(models.Model):
    s_no=models.AutoField(primary_key=True)
    voucherNo = models.IntegerField() 
    voucherCode = models.CharField(max_length=255)
    
    date = models.DateField(auto_now_add=True)
    invoice_no=models.CharField(blank=True,max_length=255)
    invoice_date=models.DateField(blank=True,null=True)
    narration = models.CharField(max_length=255,null=True, blank=True)
    primary_group = models.ForeignKey(Primary_Group, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=10, decimal_places=2)
    credit = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.voucherNo:
            # Get the maximum voucher number currently in the database
            max_voucher = JournalEntries.objects.aggregate(models.Max('voucherNo'))['voucherNo__max']
            # Set the voucher number to the maximum + 1 or 100 if there are no records yet
            self.voucherNo = max_voucher + 1 if max_voucher else 100
        self.voucherCode = "JV-"+str(self.voucherNo)
            
        super(JournalEntries, self).save(*args, **kwargs)

    def __str__(self):
        return f"Voucher No: {self.voucherNo}, Date: {self.date}, Account: {self.ledger}"
    
    
from django.db import models

# Create a model for Payment
class Payment(models.Model):
    RECEIPT_METHOD_CHOICES = (
            ('cash', 'Cash'),
            ('bank', 'Bank'),
        )

   

    date = models.DateField()
    s_no=models.AutoField(primary_key=True)
    voucherNo = models.IntegerField() 
    voucherCode = models.CharField(max_length=255)
    receipt_method = models.CharField(max_length=10, choices=RECEIPT_METHOD_CHOICES)
    
    amount_in_words = models.CharField(max_length=255)
    amount_in_numbers = models.DecimalField(max_digits=10, decimal_places=2)
    received_from = models.CharField(max_length=255)
    remarks = models.TextField(blank=True)
    narration = models.CharField(max_length=255)
    
    d_ledger = models.CharField(max_length=255)
    d_primary_group = models.CharField(max_length=255)
    d_group = models.CharField(max_length=255)
    c_ledger = models.CharField(max_length=255)
    c_primary_group = models.CharField(max_length=255)
    c_group = models.CharField(max_length=255)
    reference=models.CharField(max_length=255)
    
    reference_bill_number = models.CharField(max_length=255)
    reference_bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    debit = models.DecimalField(max_digits=10, decimal_places=2)

    # New fields
    transaction_currency = models.CharField(max_length=3, null=True, blank=True)
    clearance_date = models.DateField(null=True, blank=True)
    transaction_type = models.CharField(max_length=10, null=True, blank=True)
    

    # Receipt method (cash or bank)

    # Bank-related fields (nullable when receipt_method is 'cash')
    cheque_no = models.CharField(max_length=20, null=True, blank=True)
    bank_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.voucherNo:
            # Get the maximum voucher number currently in the database
            max_voucher = JournalEntries.objects.aggregate(models.Max('voucherNo'))['voucherNo__max']
            # Set the voucher number to the maximum + 1 or 100 if there are no records yet
            self.voucherNo = max_voucher + 1 if max_voucher else 10000
        self.voucherCode = "Pay-"+str(self.voucherNo)
            
        super(Payment, self).save(*args, **kwargs)

    def __str__(self):
        return f"Voucher No: {self.voucherNo}, Date: {self.date}, Account: {self.d_ledger}"

# Create a model for Receipt
class Receipt(models.Model):
    RECEIPT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('bank', 'Bank'),
    )

   

    date = models.DateField()
    s_no=models.AutoField(primary_key=True)
    voucherNo = models.IntegerField() 
    voucherCode = models.CharField(max_length=255)
    receipt_method = models.CharField(max_length=10, choices=RECEIPT_METHOD_CHOICES)
    
    amount_in_words = models.CharField(max_length=255)
    amount_in_numbers = models.DecimalField(max_digits=10, decimal_places=2)
    received_from = models.CharField(max_length=255)
    remarks = models.TextField(blank=True)
    narration = models.CharField(max_length=255)
    
    d_ledger = models.CharField(max_length=255)
    d_primary_group = models.CharField(max_length=255)
    d_group = models.CharField(max_length=255)
    c_ledger = models.CharField(max_length=255)
    c_primary_group = models.CharField(max_length=255)
    c_group = models.CharField(max_length=255)
    reference=models.CharField(max_length=255)
    
    reference_bill_number = models.CharField(max_length=255)
    reference_bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    debit = models.DecimalField(max_digits=10, decimal_places=2)

    # New fields
    transaction_currency = models.CharField(max_length=3, null=True, blank=True)
    clearance_date = models.DateField(null=True, blank=True)
    transaction_type = models.CharField(max_length=10, null=True, blank=True)
    

    # Receipt method (cash or bank)

    # Bank-related fields (nullable when receipt_method is 'cash')
    cheque_no = models.CharField(max_length=20, null=True, blank=True)
    bank_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.voucherNo:
            # Get the maximum voucher number currently in the database
            max_voucher = JournalEntries.objects.aggregate(models.Max('voucherNo'))['voucherNo__max']
            # Set the voucher number to the maximum + 1 or 100 if there are no records yet
            self.voucherNo = max_voucher + 1 if max_voucher else 10000
        self.voucherCode = "Recieve-"+str(self.voucherNo)
            
        super(Receipt, self).save(*args, **kwargs)

    def __str__(self):
        return f"Voucher No: {self.voucherNo}, Date: {self.date}, Account: {self.d_ledger}"
class SalesReceipt(models.Model):
    date = models.DateField()
    s_no = models.AutoField(primary_key=True)
    voucherNo = models.IntegerField()
    voucherCode = models.CharField(max_length=255)
    
    deb_primary_group = models.ForeignKey(Primary_Group, on_delete=models.CASCADE, related_name='debit_primary_group_salesreceipts')
    deb_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='debit_group_salesreceipts')
    deb_ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE, related_name='debit_ledger_salesreceipts')
    cred_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='credit_group_salesreceipts')
    cred_ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE, related_name='credit_ledger_salesreceipts')
    cred_primary_group = models.ForeignKey(Primary_Group, on_delete=models.CASCADE, related_name='credit_primary_group_salesreceipts')
    decsription=models.CharField(max_length=400)
    qty = models.IntegerField()
    untPrice = models.DecimalField(max_digits=10, decimal_places=2)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    taxed = models.DecimalField(max_digits=10, decimal_places=2)
    
    final = models.DecimalField(max_digits=10, decimal_places=2)
    

    def save(self, *args, **kwargs):
        if not self.voucherNo:
            max_voucher = SalesReceipt.objects.aggregate(models.Max('voucherNo'))['voucherNo__max']
            self.voucherNo = max_voucher + 1 if max_voucher else 10000
        self.voucherCode = "Sales-" + str(self.voucherNo)
        super(SalesReceipt, self).save(*args, **kwargs)

    def __str__(self):
        return f"Voucher No: {self.voucherNo}, Date: {self.date}, Account: {self.deb_ledger}"

class PurchaseReceipt(models.Model):
    date = models.DateField()
    s_no = models.AutoField(primary_key=True)
    voucherNo = models.IntegerField()
    voucherCode = models.CharField(max_length=255)

    deb_primary_group = models.ForeignKey(Primary_Group, on_delete=models.CASCADE, related_name='debit_primary_group_purchasereceipts')
    deb_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='debit_group_purchasereceipts')
    deb_ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE, related_name='debit_ledger_purchasereceipts')
    cred_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='credit_group_purchasereceipts')
    cred_ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE, related_name='credit_ledger_purchasereceipts')
    cred_primary_group = models.ForeignKey(Primary_Group, on_delete=models.CASCADE, related_name='credit_primary_group_purchasereceipts')
    description = models.CharField(max_length=400)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # New field
    bill_no = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.voucherNo:
            max_voucher = PurchaseReceipt.objects.aggregate(models.Max('voucherNo'))['voucherNo__max']
            self.voucherNo = max_voucher + 1 if max_voucher else 10000
        self.voucherCode = "Purchase-" + str(self.voucherNo)
        super(PurchaseReceipt, self).save(*args, **kwargs)

    def __str__(self):
        return f"Voucher No: {self.voucherNo}, Date: {self.date}, Account: {self.deb_ledger}"