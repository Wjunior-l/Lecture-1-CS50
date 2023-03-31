from django.urls import path

from . import views

app_name='wiki'

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>', views.wiki_entry, name='wiki_entry'),
    path("search_/", views.search_, name="search_"),
    path('newpage/', views.newpage, name='newpage'),
    path('wiki/<str:title>/edit', views.editpage, name='editpage'),
    path('ramdom/', views.randompage, name='randompage')
]
