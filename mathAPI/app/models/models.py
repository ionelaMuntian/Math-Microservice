# app/models/models.py
# models.py
#
# This file defines the database model for logging API requests using SQLAlchemy ORM.
# The model below (RequestLog) will map to a table called 'request_log' in the SQLite database.
# Each API call (e.g., pow, fibonacci, factorial) will be stored in this table, including:
#   - the type of operation performed,
#   - the input parameters (as JSON),
#   - the resulting output (as JSON),
#   - and a timestamp of when the request was made.
#
# This helps keep a history of how the API is used and can support features like analytics, auditing, or debugging.

from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from ..models.database import Base

class RequestLog(Base):
    __tablename__ = "request_log"
    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, nullable=False)
    input_data = Column(JSON, nullable=False)
    result = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)