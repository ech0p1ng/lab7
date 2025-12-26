from base.schema import BaseSimpleSchema


class JwtToken(BaseSimpleSchema):
    '''
    JwtToken авторизации и аутентификации

    Args:
        access_token (str): Токен
        token_type (str): Тип токена. По-умолчанию: `"bearer"`
    '''
    access_token: str
    token_type: str = 'bearer'
