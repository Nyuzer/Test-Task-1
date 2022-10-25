from django.views import View
from django.views.generic import DetailView, DeleteView, ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from datetime import date
from django.db.models import Q

from rest_framework import generics
from .serializers import CardSerializer

from .forms import CardForm, HistoryForm
from .models import Card, CardHistory


def check(model):
    objects = model.objects.all()
    for obj in objects:
        obj.check_status()
        obj.save()
    return objects


class CardListView(View):
    model = Card
    template = 'cards/cards_list.html'

    def get(self, request):
        cards = check(self.model)
        ctx = {'cards': cards}
        return render(request, self.template, ctx)


class CardDetailView(View):
    model = Card
    template = 'cards/card_detail.html'
    message = 'Something goes wrong'

    def get(self, request, pk):
        card = get_object_or_404(self.model, pk=pk)
        form = HistoryForm()
        ctx = {'card': card, 'form': form}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        card = get_object_or_404(self.model, pk=pk)
        form = HistoryForm(request.POST)
        if form.is_valid():
            history_add = form.save(commit=False)
            history_add.card = card
            history_add.save()
            return redirect(reverse_lazy('card_detail', kwargs={'pk': card.id}))
        return render(request, self.template, {'card': card, 'form': form, 'message': self.message})


class CardDeleteView(DeleteView):
    model = Card
    template_name = 'cards/card_delete.html'
    success_url = reverse_lazy('card_list')
    context_object_name = 'card'


class CardUpdateView(View):
    model = Card
    template = 'cards/card_update.html'
    message_error = 'Something goes wrong.'
    message_error_status = "You should change card 'end date' and then 'status'"

    # Check that the end_date is correct for status
    @staticmethod
    def form_valid(form):
        card = form.save(commit=False)
        if date.today() > card.end_date and card.status == 'Valid':
            return False
        card.save()
        return True

    def get(self, request, pk):
        card = get_object_or_404(self.model, pk=pk)
        form = CardForm(instance=card)
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        card = get_object_or_404(self.model, pk=pk)
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            if self.form_valid(form):
                return redirect(reverse_lazy('card_detail', kwargs={'pk': card.pk}))
            return render(request, self.template, {'form': form, 'message': self.message_error_status})
        else:
            return render(request, self.template, {'form': form, 'message': self.message_error})


class SearchCardsView(ListView):
    template_name = 'cards/search_card.html'
    model = Card
    context_object_name = 'cards_list'

    def get_queryset(self):
        query = self.request.GET.get('searched')
        return self.model.objects.filter(
            Q(seria__icontains=query) | Q(num__icontains=query) |
            Q(end_date__icontains=query) | Q(status__icontains=query)
        )


class CardApiListView(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
