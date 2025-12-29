from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from config import settings

router = APIRouter(tags=['Страницы'])
templates = Jinja2Templates(directory=settings.app.templates_path)
tags=['Общая информация']

@router.get('/')
async def main_page(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/analytics')
async def analytics_page(request: Request):
    return templates.TemplateResponse('analytics.html', {'request': request})


@router.get('/about')
async def about_page(request: Request):
    return templates.TemplateResponse('about.html', {'request': request})


@router.get('/register')
async def register_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})


@router.get('/sign-in')
async def sign_in_page(request: Request):
    return templates.TemplateResponse('sign-in.html', {'request': request})
