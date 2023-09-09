from django.contrib import admin
from django import forms
from .models import Category, Subcategory, IndividualAccount,JournalEntries
import csv
from django.http import HttpResponse

# Export selected objects as CSV
def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
    writer = csv.writer(response)
    writer.writerow(['Category Name', 'Subcategory Name', 'Account Name'])
    for obj in queryset:
        writer.writerow([obj.subcategory.category.category_name,
                         obj.subcategory.subcategory_name,
                         obj.account_name])
    return response
export_as_csv.short_description = "Export selected objects as CSV"

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('category_number',)

class SubcategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        exclude = ('subcategory_number',)

class IndividualAccountAdminForm(forms.ModelForm):
    class Meta:
        model = IndividualAccount
        exclude = ('account_number',)


class JournalEntriesAdminForm(forms.ModelForm):
    class Meta:
        model = JournalEntries
        exclude = ('voucherNo','voucherCode',)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ('category_number', 'category_name')
    search_fields = ('category_number', 'category_name')

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    form = SubcategoryAdminForm
    list_display = ('get_category_number', 'get_category_name', 'get_subcategory_number', 'get_subcategory_name', 'subcategory_number', 'subcategory_name')
    search_fields = ('subcategory_number', 'subcategory_name')
    list_filter = ('category',)

    def get_category_number(self, obj):
        return obj.category.category_number
    get_category_number.short_description = 'Category Number'

    def get_category_name(self, obj):
        return obj.category.category_name
    get_category_name.short_description = 'Category Name'

    def get_subcategory_number(self, obj):
        return obj.subcategory_number
    get_subcategory_number.short_description = 'Subcategory Number'

    def get_subcategory_name(self, obj):
        return obj.subcategory_name
    get_subcategory_name.short_description = 'Subcategory Name'

@admin.register(IndividualAccount)
class IndividualAccountAdmin(admin.ModelAdmin):
    form = IndividualAccountAdminForm
    list_display = ('get_category_number', 'get_category_name', 'get_subcategory_number', 'get_subcategory_name', 'get_account_number', 'account_name')
    search_fields = ('account_name',)
    list_filter = ('subcategory__category',)
    actions = [export_as_csv]

    def get_category_number(self, obj):
        return obj.subcategory.category.category_number
    get_category_number.short_description = 'Category Number'

    def get_category_name(self, obj):
        return obj.subcategory.category.category_name
    get_category_name.short_description = 'Category Name'

    def get_subcategory_number(self, obj):
        return obj.subcategory.subcategory_number
    get_subcategory_number.short_description = 'Subcategory Number'

    def get_subcategory_name(self, obj):
        return obj.subcategory.subcategory_name
    get_subcategory_name.short_description = 'Subcategory Name'

    def get_account_number(self, obj):
        return obj.account_number
    get_account_number.short_description = 'Account Number'



@admin.register(JournalEntries)
class JournalEntriesAdmin(admin.ModelAdmin):
    form = JournalEntriesAdminForm
    list_display = ('s_no','voucherCode','voucherNo', 'date', 'narration', 'account', 'debit', 'credit')
    list_filter = ('date', 'account')
    search_fields = ('narration', 'account')