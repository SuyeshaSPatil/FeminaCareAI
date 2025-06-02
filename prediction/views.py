# prediction/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BreastCancerPredictionForm
from .utils import make_prediction # Your prediction function
from .models import PredictionResult

@login_required
def prediction_form_view(request):
    prediction_result = None
    form = BreastCancerPredictionForm()

    if request.method == 'POST':
        form = BreastCancerPredictionForm(request.POST)
        if form.is_valid():
            input_data = form.cleaned_data # This is a dict
            try:
                label, probability = make_prediction(input_data)
                prediction_result = {
                    'label': label,
                    'probability': f"{probability*100:.2f}% for Malignant" # Or format as needed
                }
                # Save the prediction result
                PredictionResult.objects.create(
                    user=request.user,
                    prediction_label=label,
                    probability_score=probability,
                    input_features_json=input_data,
                    model_version="v1.0" # Or get from model metadata
                )
                messages.success(request, f"Prediction successful: {label}")
            except Exception as e:
                messages.error(request, f"Error making prediction: {e}")
                # Log the error e
                prediction_result = {'error': str(e)}
        else:
             messages.error(request, "Please correct the form errors.")


    context = {
        'form': form,
        'prediction_result': prediction_result,
        'page_title': 'Breast Cancer Prediction'
    }
    return render(request, 'prediction/prediction_form.html', context)