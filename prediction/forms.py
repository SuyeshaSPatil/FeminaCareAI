# prediction/forms.py
from django import forms

class BreastCancerPredictionForm(forms.Form):
    # Define fields based on your model's input features
    # Example, names should match your trained model's feature names
    radius_mean = forms.FloatField(label="Mean Radius", required=True)
    texture_mean = forms.FloatField(label="Mean Texture", required=True)
    perimeter_mean = forms.FloatField(label="Mean Perimeter", required=True)
    area_mean = forms.FloatField(label="Mean Area", required=True)
    smoothness_mean = forms.FloatField(label="Mean Smoothness", required=True)
    # ... add all other features your model expects
    # You might want to add help_text for each field