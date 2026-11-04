from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pwdlib import PasswordHash

from login_app.database import (
    create_users_table,
    create_user,
    get_user
)

from login_app.models import UserRegister


app = FastAPI(title="User Login Application")

templates = Jinja2Templates(directory="login_app/templates")

app.mount(
    "/static",
    StaticFiles(directory="login_app/static"),
    name="static"
)

password_hash = PasswordHash.recommended()

# Create database table
create_users_table()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": None}
    )


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"error": None}
    )


@app.post("/register", response_class=HTMLResponse)
def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    try:
        user_data = UserRegister(
            username=username,
            password=password
        )
    except Exception:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "error": "Username must be 3-30 characters and password must be 8-10 characters."
            },
            status_code=400
        )

    hashed_password = password_hash.hash(user_data.password)

    success = create_user(
        user_data.username,
        hashed_password
    )

    if not success:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"error": "Username already exists."},
            status_code=400
        )

    return RedirectResponse(
        url="/",
        status_code=303
    )


@app.post("/login", response_class=HTMLResponse)
def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    user = get_user(username.strip())

    if user is None or not password_hash.verify(
        password,
        user["password"]
    ):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Invalid username or password."},
            status_code=401
        )

    return RedirectResponse(
        url=f"/welcome?username={username.strip()}",
        status_code=303
    )


@app.get("/welcome", response_class=HTMLResponse)
def welcome_page(request: Request, username: str):
    user = get_user(username)

    if user is None:
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="welcome.html",
        context={"username": username}
    )


@app.post("/logout")
def logout_user():
    return RedirectResponse(
        url="/",
        status_code=303
    )
