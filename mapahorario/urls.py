from django.urls import path
from . import views


urlpatterns = [

    path('', views.mapahorario, name ="mapahorario"),
    path("update/<int:pk>/<str:column>/", views.update_schedule, name="update_schedule"),

]

