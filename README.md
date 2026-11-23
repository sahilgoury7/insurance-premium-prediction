# 🏥 Insurance Premium Prediction

An end-to-end Machine Learning web application with a **FastAPI** backend and an interactive **Streamlit** frontend to predict insurance premium categories based on patient demographics, lifestyle, and health indicators.

---

## 🏗️ Project Architecture

```
insurance-premium-prediction/
├── config/
│   └── city_tier.py              # Tier-1 and Tier-2 city categorization
├── model/
│   ├── model.pkl                 # Trained Machine Learning pipeline
│   └── predict.py                # Prediction inference logic & MLflow versioning
├── schema/
│   ├── user_input.py             # Pydantic data validation & computed fields
│   └── prediction_response.py    # Standardized API response schema
├── myapp.py                      # FastAPI application & REST endpoints
├── frontend.py                   # Streamlit web interface
├── requirements.txt              # Project dependencies
├── Dockerfile                    # Containerization config for cloud deployment
├── .dockerignore                 # Excludes heavy/cached files from Docker image
└── .gitignore                    # Excludes virtual environments & temporary files
```

---

## 🚀 Getting Started

### 1. Setup Virtual Environment & Install Dependencies
```powershell
python -m venv myenv
.\myenv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the FastAPI Backend
```powershell
uvicorn myapp:app --reload
```
* **API Home:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Interactive Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Health Check:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### 3. Run the Streamlit Frontend
Open a **new terminal** and run:
```powershell
streamlit run frontend.py
```
* **Web UI:** [http://localhost:8501](http://localhost:8501)

---

## 🐳 Docker Deployment

Build and run the containerized backend:
```powershell
# Build Docker image
docker build -t insurance-api:latest .

# Run container
docker run -d -p 8000:8000 --name insurance-container insurance-api:latest
```

---

## 📡 API Endpoints

### `POST /predict`
* **Request Body:**
```json
{
  "age": 28,
  "weight": 70.0,
  "height": 1.75,
  "income_lpa": 12.0,
  "smoker": false,
  "city": "Mumbai",
  "occupation": "private_job"
}
```
* **Response (200 OK):**
```json
{
  "predicted_category": "Low",
  "confidence": 0.78,
  "class_probabilities": {
    "High": 0.01,
    "Low": 0.78,
    "Medium": 0.21
  }
}
```
