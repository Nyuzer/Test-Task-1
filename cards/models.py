from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db import models
from datetime import date


class CardHistory(models.Model):
    card = models.ForeignKey('Card', on_delete=models.CASCADE, related_name='history')
    description = models.CharField(max_length=100, verbose_name='Description')

    def __str__(self):
        return f'{self.card} {self.description}'


class Card(models.Model):
    seria = models.CharField(max_length=12, verbose_name='Seria')
    num = models.PositiveIntegerField(verbose_name='Card number')
    date_of_manufacture = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Date of manufacture')
    end_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name='End date of activity')
    use_date = models.DateField(auto_now=True, auto_now_add=False, verbose_name='Date of use')
    amount = models.DecimalField(max_digits=100, decimal_places=2, verbose_name='Amount')
    VALID = 'Valid'
    NVALID = 'Not valid'
    STATUS_CHOICES = [
        (VALID, 'Valid'),
        (NVALID, 'Not valid'),
    ]
    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default=VALID,
        verbose_name='Status'
    )

    def __str__(self):
        return self.seria

    def check_status(self):
        if date.today() > self.end_date:
            self.status = self.NVALID
        else:
            self.status = self.VALID

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'
        ordering = ['-date_of_manufacture']

