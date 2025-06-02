# prediction/utils.py
import joblib
import pandas as pd
import os
from django.conf import settings

# Define paths to your saved model and scaler
MODEL_DIR = os.path.join(settings.BASE_DIR, 'ml_models')
MODEL_PATH = os.path.join(MODEL_DIR, 'breast_cancer_model.pkl') # Your trained model
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl') # Your trained scaler, if used

# Ensure the ml_models directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

# --- Placeholder for model and scaler creation ---
# You need to run this part once (e.g., in a separate script or Django management command)
# after training your model and scaler to create the .pkl files.
def _create_placeholder_model_and_scaler():
    from sklearn.svm import SVC
    from sklearn.preprocessing import StandardScaler
    import numpy as np

    if not os.path.exists(MODEL_PATH):
        print(f"Creating placeholder model at {MODEL_PATH}")
        # Create a dummy model for demonstration
        # Replace this with loading your actual trained model
        X_dummy = np.random.rand(10, 5) # 5 features
        y_dummy = (np.random.rand(10) > 0.5).astype(int)
        model = SVC(probability=True)
        model.fit(X_dummy, y_dummy)
        joblib.dump(model, MODEL_PATH)

    if not os.path.exists(SCALER_PATH):
        print(f"Creating placeholder scaler at {SCALER_PATH}")
        # Create a dummy scaler
        scaler = StandardScaler()
        scaler.fit(np.random.rand(10, 5)) # Fit with dummy data
        joblib.dump(scaler, SCALER_PATH)

# Call this function to ensure placeholders exist if actual files are missing
# In a real app, you'd have these files prepared.
_create_placeholder_model_and_scaler()
# --- End of placeholder creation ---


# Load the model and scaler once when the module is imported
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH) # Load scaler if you used one
    print("ML Model and Scaler loaded successfully.")
except FileNotFoundError:
    model = None
    scaler = None
    print(f"Error: Model or scaler file not found. Please ensure '{MODEL_PATH}' and '{SCALER_PATH}' exist.")
except Exception as e:
    model = None
    scaler = None
    print(f"Error loading ML model or scaler: {e}")


def make_prediction(input_data: dict):
    """
    Makes a prediction using the loaded model.
    input_data: A dictionary where keys are feature names and values are their values.
    """
    if model is None or scaler is None: # Adjust if you don't use a scaler
        raise Exception("ML Model or Scaler not loaded. Cannot make predictions.")

    try:
        # Convert input_data dict to DataFrame in the correct feature order
        # This order MUST match the order of features the model was trained on.
        # Example feature order (ADAPT THIS TO YOUR MODEL):
        feature_order = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean']
        
        # Create a DataFrame with a single row
        df = pd.DataFrame([input_data], columns=feature_order)

        # Ensure all expected columns are present, fill with NaN if not (or handle error)
        for col in feature_order:
            if col not in df.columns:
                # df[col] = pd.NA # Or some default, or raise error
                raise ValueError(f"Missing feature in input: {col}")
        
        # Fill any NaNs if your model can't handle them (e.g., with mean from training data - stored in scaler)
        # For simplicity, we assume data is complete here. Proper handling is crucial.
        # df.fillna(scaler.mean_, inplace=True) # Example if scaler stores means

        # Scale the features (if your model was trained on scaled data)
        scaled_features = scaler.transform(df) # `scaler` should be your trained StandardScaler

        # Make prediction
        prediction_raw = model.predict(scaled_features) # Output: [0] or [1]
        prediction_proba = model.predict_proba(scaled_features) # Output: [[prob_class_0, prob_class_1]]

        predicted_label_int = prediction_raw[0]
        
        # Map integer prediction to human-readable label
        # ADAPT THIS MAPPING: 0 for Benign, 1 for Malignant (common for Scikit-learn datasets)
        label_map = {0: 'Benign', 1: 'Malignant'}
        predicted_label_str = label_map.get(predicted_label_int, "Unknown")

        # Get the probability of the predicted class
        # If predicted_label_int is 1 (Malignant), probability is proba[0][1]
        # If predicted_label_int is 0 (Benign), probability is proba[0][0]
        # More generally, prob_for_predicted_class = prediction_proba[0][predicted_label_int]
        # Or, if you always want probability of 'Malignant' (class 1):
        prob_malignant = prediction_proba[0][1] # Assuming class 1 is Malignant

        return predicted_label_str, prob_malignant

    except Exception as e:
        print(f"Error during prediction: {e}")
        # Log the error properly
        raise # Re-raise the exception to be caught by the view