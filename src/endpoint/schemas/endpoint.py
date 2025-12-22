from base.schema import BaseSimpleSchema, BaseSchema


class EndpointSimpleSchema(BaseSimpleSchema):
    '''
    Pydantic-схема ручки

    Args:
        name (str): Внутреннее имя ручки (например theme_post)
    '''
    name: str


class EndpointSchema(BaseSchema, EndpointSimpleSchema):
    '''
    Pydantic-схема ручки

    Args:
        id (int): Идентификатор
        name (str): Внутреннее имя ручки (например theme_post)
    '''
