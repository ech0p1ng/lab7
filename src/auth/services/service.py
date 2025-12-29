from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import settings
from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from exceptions.exception import BadCredentialsError, NotFoundError
from user.models.model import UserModel
from user.services.service import UserService
import uuid
from auth.schemas.token import JwtToken


http_bearer = HTTPBearer()


class AuthService:
    USER_ID_KEY = 'user_id'
    UUID_KEY = 'uuid'
    ROLE_KEY = 'role'

    def __init__(self, user_service: UserService):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.security = HTTPBearer()
        self.user_service = user_service

    async def __create_token(self, user_id: int) -> str:
        '''
        Создание JWT-токена по id пользователя

        Args:
            user_id (int): Id пользователя

        Raises:
            NotFoundError: Не удалось найти пользователя по id

        Returns:
            str: JWT-токен

        '''
        user = await self.user_service.get({"id": user_id})

        expire = datetime.now() + timedelta(
            seconds=settings.jwt.access_token_expire
        )

        payload = {
            'user_id': user.id,
            'role_id': user.role.id,
            'exp': int(expire.timestamp()),
            'uuid': str(uuid.uuid4())
        }

        encoded_jwt = jwt.encode(
            payload,
            key=settings.jwt.secret_key,
            algorithm=settings.jwt.algorithm
        )
        return encoded_jwt

    async def get_user_by_token(
        self,
        token: str,
        from_service: bool = True
    ) -> UserModel | tuple[int, int, str]:
        '''
        Получение данных пользователя по JWT-токену

        Args:
            token (str): JWT-токен
            from_service(bool): True - Получить SQLAlchemy-модель \
                пользователя, False - получить кортеж вида \
                    (id пользователя, id роли, uuid)

        Returns:
            UserModel: Пользователь **если `user_from_service=True`**, \
                в противном случае `tuple[int, int, str]`: \
                    id пользователя, id роли, uuid

        Raises:
            BadCredentialsError: Не удалось проверить учетные данные
            NotFoundError: Не удалось найти пользователя
        '''
        credentials_exception = BadCredentialsError(
            "Не удалось проверить учетные данные"
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt.secret_key,
                algorithms=[settings.jwt.algorithm]
            )
            user_id = int(str(payload.get(AuthService.USER_ID_KEY)))
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        if from_service:
            user = await self.user_service.get(
                {"id": user_id}, [UserModel.role]
            )
            return user
        else:
            await self.user_service.exists({"id": user_id})
            role_id = int(str(payload.get(AuthService.ROLE_KEY)))
            jwt_uuid = str(payload.get(AuthService.UUID_KEY))
            return (user_id, role_id, jwt_uuid)

    async def get_token(self, user_id: int) -> JwtToken:
        '''
        Получить JWT-токен по id пользователя

        Args:
            user_id (int): Id пользователя

        Raises:
            NotFoundError: Не удалось найти пользователя по id

        Returns:
            JwtToken: Словарь с ключами `access_token` и `token_type` \
                и значениями токена и `bearer` соответственно

        Example:
        ```
        {
            'access_token': access_token_example,
            'token_type': 'bearer'
        }
        ```
        '''
        try:
            user = await self.user_service.get({"id": user_id})
            access_token = await self.__create_token(user.id)
        except NotFoundError as nfe:
            raise nfe
        return JwtToken(access_token=access_token)
        # return {
        #     'access_token': access_token,
        #     'token_type': 'bearer'
        # }
