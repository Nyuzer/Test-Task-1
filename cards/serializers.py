from .models import Card
from rest_framework import serializers


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ('id', 'seria', 'num', 'date_of_manufacture', 'end_date', 'use_date', 'amount', 'status',)
