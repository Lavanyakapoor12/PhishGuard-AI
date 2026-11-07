
from pathlib import Path

import joblib

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, HttpUrl, field_validator

from sqlalchemy.orm import Session

from backend.database import engine, Base, SessionLocal
from backend.models import ScanHistory


# Create database tables.
Base.metadata.create_all(bind=engine)


# Create FastAPI application.
app = FastAPI(
    title="PhishGuard AI",
    description="AI-powered phishing URL detection system",
    version="1.0"
)


# Configure CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://phishguard-ai-2lw.pages.dev",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load the trained ML model.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "ml" / "phishguard_url_model.pkl"

model = joblib.load(MODEL_PATH)


# Database connection.
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# URL request validation.
class URLRequest(BaseModel):

    url: HttpUrl

    @field_validator("url", mode="before")
    @classmethod
    def validate_url_length(cls, value):

        if isinstance(value, str) and len(value) > 2048:
            raise ValueError(
                "URL must not exceed 2048 characters"
            )

        return value


# Home endpoint.
@app.get("/")
def home():

    return {
        "message": "Welcome to PhishGuard AI!",
        "status": "Backend is running"
    }


# Predict phishing URL.
@app.post("/predict")
def predict_url(
    request: URLRequest,
    db: Session = Depends(get_db)
):

    url = str(request.url)

    prediction = model.predict([url])[0]

    probabilities = model.predict_proba([url])[0]

    phishing_probability = probabilities[
        list(model.classes_).index(0)
    ]

    result = "Phishing" if prediction == 0 else "Legitimate"

    probability = round(
        float(phishing_probability) * 100,
        2
    )

    # Save scan result in PostgreSQL.
    new_scan = ScanHistory(
        url=url,
        prediction=result,
        phishing_probability=probability
    )

    try:
        db.add(new_scan)
        db.commit()
        db.refresh(new_scan)

    except Exception:
        db.rollback()
        raise

    return {
        "id": new_scan.id,
        "url": url,
        "prediction": result,
        "phishing_probability": probability,
        "created_at": new_scan.created_at
    }


# Get scan history.
@app.get("/history")
def get_scan_history(
    db: Session = Depends(get_db)
):

    scans = (
        db.query(ScanHistory)
        .order_by(ScanHistory.created_at.desc())
        .all()
    )

    return [
        {
            "id": scan.id,
            "url": scan.url,
            "prediction": scan.prediction,
            "phishing_probability": scan.phishing_probability,
            "created_at": scan.created_at
        }
        for scan in scans
    ]


# Get dashboard statistics.
@app.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db)
):

    total_scans = db.query(ScanHistory).count()

    phishing_scans = (
        db.query(ScanHistory)
        .filter(ScanHistory.prediction == "Phishing")
        .count()
    )

    legitimate_scans = (
        db.query(ScanHistory)
        .filter(ScanHistory.prediction == "Legitimate")
        .count()
    )

    phishing_rate = (
        round((phishing_scans / total_scans) * 100, 2)
        if total_scans > 0
        else 0
    )

    return {
        "total_scans": total_scans,
        "phishing_detected": phishing_scans,
        "legitimate_urls": legitimate_scans,
        "phishing_rate": phishing_rate
    }
