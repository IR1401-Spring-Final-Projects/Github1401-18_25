from django.urls import path

from search_engine import views

urlpatterns = [

    path(
        'mir',
        views.SearchEngine.as_view(),
        name='search'
    )
]
