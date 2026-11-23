import pickle
import warnings
import pandas as pd
import sklearn.compose._column_transformer as ct

# Suppress sklearn unpickle warnings & add compatibility patch for sklearn version mismatch
warnings.filterwarnings("ignore")
class _RemainderColsList(list):
    pass
ct._RemainderColsList = _RemainderColsList

# import the ml model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

# MLFlow / Model Version (support both for backwards compatibility)
MODEL_VERSION = '1.0.0'
model_version = MODEL_VERSION

# Get class labels from model (important for matching probabilities to class names)
class_labels = model.classes_.tolist()

def predict_output(user_input: dict):

    df = pd.DataFrame([user_input])

    # Predict the class
    predicted_class = model.predict(df)[0]

    # Get probabilities for all classes
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)
    
    # Create mapping: {class_name: probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(float(p), 4), probabilities)))

    return {
        "predicted_category": str(predicted_class),
        "confidence": round(float(confidence), 4),
        "class_probabilities": class_probs
    }
