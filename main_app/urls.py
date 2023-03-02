from django.urls import path
from . import views

urlpatterns = [
    # using empty string, makes this our root route
    # views.home refers to a view to render a file
    # name = home is a kwarg, gives route a name (opptional)
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    #path for cats
    path('cats/', views.cats_index, name='index'),

]