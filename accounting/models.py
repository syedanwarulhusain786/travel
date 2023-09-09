from django.db import models

class Category(models.Model):
    category_number = models.PositiveIntegerField(primary_key=True)  # Start from 100, 200, 300, ...
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category_name}"

    def save(self, *args, **kwargs):
        if not self.category_number:
            latest_category = Category.objects.order_by('-category_number').first()
            if latest_category:
                self.category_number = latest_category.category_number + 100
            else:
                self.category_number = 100
        super(Category, self).save(*args, **kwargs)

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_number = models.PositiveIntegerField()  # Start from 1 within each category
    subcategory_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.subcategory_name}"

    def save(self, *args, **kwargs):
        if not self.subcategory_number:
            # Ensure subcategory_number is unique within each category
            latest_subcategory_in_category = Subcategory.objects.filter(category=self.category).order_by('-subcategory_number').first()
            if latest_subcategory_in_category:
                self.subcategory_number = latest_subcategory_in_category.subcategory_number + 1
            else:
                self.subcategory_number = self.category.category_number+1
        super(Subcategory, self).save(*args, **kwargs)

class IndividualAccount(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    account_number = models.PositiveIntegerField()  # Start from 1 within each subcategory
    account_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.account_name}"

    def save(self, *args, **kwargs):
        if not self.account_number:
            # Ensure account_number is unique within each subcategory
            latest_account_in_subcategory = IndividualAccount.objects.filter(subcategory=self.subcategory).order_by('-account_number').first()
            if latest_account_in_subcategory:
                self.account_number = latest_account_in_subcategory.account_number + 1
            else:
                self.account_number = self.subcategory.subcategory_number*10+1
        super(IndividualAccount, self).save(*args, **kwargs)
class JournalEntries(models.Model):
    s_no=models.AutoField(primary_key=True)
    voucherNo = models.IntegerField() 
    voucherCode = models.CharField(max_length=255)
    
    date = models.DateField(auto_now_add=True)
    narration = models.CharField(max_length=255,null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    account = models.ForeignKey(IndividualAccount, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=10, decimal_places=2)
    credit = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.voucherNo:
            # Get the maximum voucher number currently in the database
            max_voucher = JournalEntries.objects.aggregate(models.Max('voucherNo'))['voucherNo__max']
            # Set the voucher number to the maximum + 1 or 100 if there are no records yet
            self.voucherNo = max_voucher + 1 if max_voucher else 100
        self.voucherCode = "VN-"+str(self.voucherNo)
            
        super(JournalEntries, self).save(*args, **kwargs)

    def __str__(self):
        return f"Voucher No: {self.voucherNo}, Date: {self.date}, Account: {self.account}"