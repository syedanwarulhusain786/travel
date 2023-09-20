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