from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from config import settings
from logger import logger

router = APIRouter()
templates = Jinja2Templates(directory=settings.app.templates_path)

logger.debug(settings.app.templates_path)


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
