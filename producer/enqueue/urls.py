from django.urls import path
from .views import enqueue

urlpatterns = [
    path('enqueue/', enqueue),
]