from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_302_FOUND
from passlib.hash import bcrypt

from app.db.models import Users, Asset, Data
from app.db.db_core import get_session

router = APIRouter()
templates = Jinja2Templates(directory="app/admin/templates")

FAKE_ADMIN = {
    "username": "admin",
    "password": bcrypt.hash("admin123")  # Пример пароля
}


def is_authenticated(request: Request):
    return request.session.get("authenticated") is True


@router.get("/admin/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/admin/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == FAKE_ADMIN["username"] and bcrypt.verify(password, FAKE_ADMIN["password"]):
        request.session["authenticated"] = True
        return RedirectResponse(url="/admin/panel", status_code=HTTP_302_FOUND)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Неверные данные"})


@router.get("/admin/panel", response_class=HTMLResponse)
async def admin_panel(request: Request, session: AsyncSession = Depends(get_session)):
    if not is_authenticated(request):
        return RedirectResponse("/admin/login")

    users = (await session.execute(Users.__table__.select())).fetchall()
    assets = (await session.execute(Asset.__table__.select())).fetchall()
    data = (await session.execute(Data.__table__.select())).fetchall()

    return templates.TemplateResponse("panel.html", {
        "request": request,
        "users": users,
        "assets": assets,
        "data": data
    })
