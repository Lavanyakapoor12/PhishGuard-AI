
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from backend.database import Base


class ScanHistory(Base):

    # Database table name
    __tablename__ = "scan_history"

    # Unique ID for every scan
    id = Column(Integer, primary_key=True, index=True)

    # URL entered by the user
    url = Column(String, nullable=False)

    # Prediction: Phishing or Legitimate
    prediction = Column(String, nullable=False)

    # Estimated phishing probability
    phishing_probability = Column(Float, nullable=False)

    # Date and time of the scan
    created_at = Column(DateTime(timezone=True), server_default=func.now())
