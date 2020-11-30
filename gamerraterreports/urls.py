from django.urls import path
from .views import topgames_list

urlpatterns = [
    path('reports/topgames', topgames_list),
]