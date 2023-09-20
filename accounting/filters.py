import django_filters
from .models import JournalEntries
class JournalEntryFilter(django_filters.FilterSet):
    class Meta:
        model=JournalEntries
        fields=[
            'voucherCode',
            'date',
            'primary_group',
            'group',
            'ledger'
            
            
        ]
        