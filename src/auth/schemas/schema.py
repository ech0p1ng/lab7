from pydantic import Field
from base.schema import BaseSimpleSchema


class AuthSchema(BaseSimpleSchema):
    id: int = Field(gt=0)
