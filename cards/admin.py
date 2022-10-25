from django.contrib import admin
from .models import Card, CardHistory


class History(admin.TabularInline):
    model = CardHistory


class CardAdmin(admin.ModelAdmin):
    inlines = [
        History,
    ]
    list_display = ('id', 'seria', 'num', 'date_of_manufacture', 'end_date', 'status')
    search_fields = ('seria', 'num')
    list_editable = ('status', )
    list_filter = ('status', 'date_of_manufacture')
    save_on_top = True


admin.site.register(Card, CardAdmin)
