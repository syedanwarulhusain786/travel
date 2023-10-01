from django.contrib import admin
from django import forms
import csv
from django.http import HttpResponse
from .models import Primary_Group, Group, Ledger, JournalEntries,SalesReceipt,PurchaseReceipt,Receipt,Payment
class SalesReceiptAdmin(admin.ModelAdmin):
    list_display = ('date', 's_no', 'voucherNo', 'voucherCode','deb_primary_group', 'deb_group','deb_ledger','cred_primary_group', 'cred_group','cred_ledger', 'decsription', 'amount', 'total')

admin.site.register(SalesReceipt, SalesReceiptAdmin)


admin.site.register(PurchaseReceipt)


admin.site.register(Receipt)


admin.site.register(Payment)
# Export selected objects as CSV
def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
    writer = csv.writer(response)
    writer.writerow(['Primary Group Name', 'Group Name', 'Ledger Name'])
    for obj in queryset:
        writer.writerow([obj.group.primary_group.primary_group_name,
                         obj.group.group_name,
                         obj.ledger_name])
    return response

export_as_csv.short_description = "Export selected objects as CSV"

class PrimaryGroupAdminForm(forms.ModelForm):
    class Meta:
        model = Primary_Group
        exclude = ('primary_group_number',)

class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ('group_number',)

class LedgerAdminForm(forms.ModelForm):
    class Meta:
        model = Ledger
        exclude = ('ledger_number',)

class JournalEntriesAdminForm(forms.ModelForm):
    class Meta:
        model = JournalEntries
        exclude = ('voucherNo', 'voucherCode',)

@admin.register(Primary_Group)
class PrimaryGroupAdmin(admin.ModelAdmin):
    form = PrimaryGroupAdminForm
    list_display = ('primary_group_number', 'primary_group_name', 'primary_group_type')
    search_fields = ('primary_group_number', 'primary_group_name')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    list_display = ('get_primary_group_number', 'get_primary_group_name', 'get_group_number', 'group_name')
    search_fields = ('group_name',)
    list_filter = ('primary_group',)

    def get_primary_group_number(self, obj):
        return obj.primary_group.primary_group_number
    get_primary_group_number.short_description = 'Primary Group Number'

    def get_primary_group_name(self, obj):
        return obj.primary_group.primary_group_name
    get_primary_group_name.short_description = 'Primary Group Name'

    def get_group_number(self, obj):
        return obj.group_number
    get_group_number.short_description = 'Group Number'

@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    form = LedgerAdminForm
    list_display = ('get_primary_group_number', 'get_primary_group_name', 'get_group_number', 'get_group_name', 'get_ledger_number', 'ledger_name')
    search_fields = ('ledger_name',)
    list_filter = ('group__primary_group', 'group',)
    actions = [export_as_csv]

    def get_primary_group_number(self, obj):
        return obj.group.primary_group.primary_group_number
    get_primary_group_number.short_description = 'Primary Group Number'

    def get_primary_group_name(self, obj):
        return obj.group.primary_group.primary_group_name
    get_primary_group_name.short_description = 'Primary Group Name'

    def get_group_number(self, obj):
        return obj.group.group_number
    get_group_number.short_description = 'Group Number'

    def get_group_name(self, obj):
        return obj.group.group_name
    get_group_name.short_description = 'Group Name'

    def get_ledger_number(self, obj):
        return obj.ledger_number
    get_ledger_number.short_description = 'Ledger Number'

@admin.register(JournalEntries)
class JournalEntriesAdmin(admin.ModelAdmin):
    form = JournalEntriesAdminForm
    list_display = ('s_no', 'voucherCode', 'voucherNo', 'date', 'narration', 'ledger', 'debit', 'credit')
    list_filter = ('date', 'ledger')
    search_fields = ('narration', 'ledger')
