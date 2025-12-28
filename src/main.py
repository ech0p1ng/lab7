import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dependencies.exceptions_handlers import set_exceptions_handlers
from user.routers.router import router as user_router
from role.routers.router import router as role_router
from auth.routers.router import router as auth_router
from analytics.routers.router import router as analytics_router
from webpages.pages import router as web_router
from info.routers.router import router as info_router
from config import settings

import debugpy

debugpy.listen(("0.0.0.0", 5678))
# debugpy.wait_for_client()  # опционально


def get_application(
    api_routers: list[APIRouter],
    other_routers: list[APIRouter] = []
) -> FastAPI:
    '''
    Возвращает объект класса `FastAPI` с настроенными роутерами

    Args:
        api_routers (list[APIRouter]): Список роутеров для API
        other_routers(list[APIRouter]): Список остальных роутеров \
            (Пустой поумолчанию)

    Returns:
        FastAPI: объект класса `FastAPI` с настроенными роутерами
    '''
    app = set_exceptions_handlers(FastAPI())

    origins = [
        # Локальные адреса для разработки
        'http://localhost',
        'http://localhost:80',
        'http://localhost:3000',
        'http://localhost:5173',
        'http://localhost:8080',
        'http://127.0.0.1',
        'http://127.0.0.1:80',
        'http://127.0.0.1:3000',
        'http://127.0.0.1:5173',
        'http://127.0.0.1:8080',
        'http://0.0.0.0',
        'http://0.0.0.0:80',
        'http://0.0.0.0:3000',
        'http://0.0.0.0:5173',
        'http://0.0.0.0:8080',

        # Docker-адреса фронтенда
        'http://education-bot-frontend-1',
        'http://education-bot-frontend-1:80',
        'http://education-bot-frontend-1:3000',
        'http://education-bot-frontend-1:5173',
        'http://education-bot-frontend-1:8080',

        # Docker-адреса бэкенда
        'http://education-bot-app-1',
        'http://education-bot-app-1:80',
        'http://education-bot-app-1:3000',
        'http://education-bot-app-1:5173',
        'http://education-bot-app-1:8080',
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    for router in api_routers:
        app.include_router(router, prefix='/api')

    for router in other_routers:
        app.include_router(router)

    app.mount(
        '/static',
        StaticFiles(directory=settings.app.static_path),
        name='static'
    )

    return app


app = get_application(
    api_routers=[
        role_router,
        user_router,
        auth_router,
        analytics_router,
        info_router,
    ],
    other_routers=[
        web_router,
    ]
)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
