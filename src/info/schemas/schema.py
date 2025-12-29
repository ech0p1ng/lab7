from base.schema import BaseSimpleSchema


class InfoSchema(BaseSimpleSchema):
    subject_area: str
    target_attribute: str
    train_data: dict
    