from django.urls import path
from .views import CardListView, CardDetailView, CardDeleteView, CardUpdateView, SearchCardsView, CardApiListView


urlpatterns = [
    path('', CardListView.as_view(), name='card_list'),
    path('<int:pk>/', CardDetailView.as_view(), name='card_detail'),
    path('<int:pk>/delete/', CardDeleteView.as_view(), name='card_delete'),
    path('<int:pk>/update/', CardUpdateView.as_view(), name='card_update'),
    path('search/', SearchCardsView.as_view(), name='search_card'),
    path('api/', CardApiListView.as_view())
]
