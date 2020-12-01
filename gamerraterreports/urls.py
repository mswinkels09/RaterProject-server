from django.urls import path
from .views import topgames_list, bottomgames_list, gamespercategory_list, morethan5players_list, mostreviewedgame_list

urlpatterns = [
    path('reports/topgames', topgames_list),
    path('reports/bottomgames', bottomgames_list),
    path('reports/gamespercategory', gamespercategory_list),
    path('reports/morethan5players', morethan5players_list),
    path('reports/mostreviews', mostreviewedgame_list),
]