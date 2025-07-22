# app/controllers/math_controller.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.auth import verify_token, oauth2_scheme
from app.models.database      import get_db
from app.services.math_service import compute_pow, compute_fib, compute_factorial
from app.models.models        import RequestLog

router = APIRouter(prefix="/api/v1", tags=["math"])

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)

@router.post("/pow", response_model=dict)
def pow_endpoint(
    x: float = Query(...),
    y: float = Query(...),
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    result = compute_pow(x, y)
    db.add(RequestLog(operation="pow", input_data={"x":x,"y":y}, result=result))
    db.commit()
    return {"result": result}

@router.get("/fibonacci/{n}", response_model=dict)
def fib_endpoint(
    n: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    if n<0:
        raise HTTPException(400,"n must be ≥ 0")
    result = compute_fib(n)
    db.add(RequestLog(operation="fibonacci",input_data={"n":n},result=result))
    db.commit()
    return {"result": result}

@router.get("/factorial", response_model=dict)
def fact_endpoint(
    n: int = Query(..., ge=0),
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    result = compute_factorial(n)
    db.add(RequestLog(operation="factorial",input_data={"n":n},result=result))
    db.commit()
    return {"result": result}
