# schemas.py
#
# This file defines the Pydantic models (schemas) used for:
#   - Validating incoming requests
#   - Formatting outgoing responses
#
# FastAPI uses these schemas automatically to:
#   - Validate and parse request bodies and query parameters
#   - Generate OpenAPI documentation (visible in /docs)
#
# Each schema is a subclass of Pydantic's BaseModel and defines the expected structure.

from pydantic import BaseModel, Field, validator

# Request schema for the power operation
# Expected in POST /api/v1/pow body:
# {
#   "x": 2.0,
#   "y": 3.0
# }
class PowRequest(BaseModel):
    x: float  # Base number
    y: float  # Exponent

# Request schema for factorial operation
# Used as query parameters in GET /api/v1/factorial?n=5
# Validates that n is an integer and n >= 0
class FactorialRequest(BaseModel):
    n: int = Field(..., ge=0)  # Field(...) makes it required; ge=0 ensures it's >= 0

# Response schema returned by all endpoints
# Example response:
# {
#   "result": 120
# }
class ResultResponse(BaseModel):
    result: int  # The result of the operation (can also be float if needed)
