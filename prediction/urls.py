# prediction/urls.py
from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    path('assess/', views.prediction_form_view, name='predict_form'),
    # Add more URLs for viewing past predictions, etc.
]