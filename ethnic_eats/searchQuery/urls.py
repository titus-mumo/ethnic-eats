from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('<str:searchTerm>/', views.SearchQuery.as_view(), name='search-query')
]

urlpatterns = format_suffix_patterns(urlpatterns)