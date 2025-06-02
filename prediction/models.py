# prediction/models.py
from django.db import models
from users.models import CustomUser
# from health_records.models import PatientDataRecord # If prediction is linked to a specific record

class PredictionResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='predictions')
    # patient_data_record = models.OneToOneField(PatientDataRecord, on_delete=models.CASCADE, null=True, blank=True)
    prediction_label = models.CharField(max_length=50) # e.g., 'Benign', 'Malignant', 'Low Risk', 'High Risk'
    probability_score = models.FloatField(null=True, blank=True)
    # Input features at the time of prediction can be stored as JSON or linked to PatientDataRecord
    input_features_json = models.JSONField(null=True, blank=True)
    prediction_date = models.DateTimeField(auto_now_add=True)
    model_version = models.CharField(max_length=50, blank=True, null=True) # To track which model version made the prediction

    def __str__(self):
        return f"Prediction for {self.user.username} on {self.prediction_date.strftime('%Y-%m-%d')}: {self.prediction_label}"