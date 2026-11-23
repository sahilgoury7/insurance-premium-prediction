from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model.predict import predict_output, MODEL_VERSION, model
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse

# Create FastAPI app
app = FastAPI(title="Insurance Premium Prediction API")


@app.get("/")
def home():
    return {"message": "Insurance premium prediction API is running"}


@app.get("/health")
def healthcheck():
    return {
        "status": "ok",
        "model_version": MODEL_VERSION,
        "model_loaded": model is not None
    }


@app.post("/predict", response_model=PredictionResponse)
def predict_premium(data: UserInput):
    user_input = {
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }
    try:
        prediction = predict_output(user_input)

        return JSONResponse(
            status_code=200, 
            content=prediction
        )
    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": str(e)}
        )
