from django.forms import ModelForm
from .models import Card, CardHistory


class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = ['seria', 'num', 'end_date', 'amount', 'status', ]


class HistoryForm(ModelForm):
    class Meta:
        model = CardHistory
        fields = ['description', ]
