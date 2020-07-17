from django.urls import path

from . import views

app_name = 'marketplace'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('book/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('book/add/', views.add_book, name='add_book'),
    path('book/add/isbn_lookup/', views.isbn_lookup, name='isbn_lookup'),
    path('browse/', views.browse, name='browse'),
]