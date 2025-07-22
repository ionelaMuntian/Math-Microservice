# app/api/frontend.py
from datetime import timedelta

from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse

from .auth import create_access_token, fake_users, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def login_form():
    return """
    <html><body>
      <h2>Math Service Login</h2>
      <form action="/login-form" method="post">
        Username: <input name="username"/><br>
        Password: <input type="password" name="password"/><br>
        <button type="submit">Log In</button>
      </form>
    </body></html>
    """

@router.post("/login-form", response_class=HTMLResponse)
def login_form_submit(
    username: str = Form(...),
    password: str = Form(...)
):
    user = fake_users.get(username)
    if not user or password != user["password"]:
        return HTMLResponse("<h3>Invalid credentials</h3>", status_code=401)

    token = create_access_token(
        {"sub": username},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return f"""
    <html><body>
      <h2>Login Successful</h2>
      <p>Copy this token into Swagger’s Authorize box:</p>
      <textarea rows="5" cols="60">Bearer {token}</textarea><br>
      <a href="/docs">Go to Swagger UI</a>
    </body></html>
    """
