from pydantic import BaseModel
from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB


class PydanticType(TypeDecorator):
    """Pydantic type.
    SAVING:
    - Uses SQLAlchemy JSON type under the hood.
    - Accept the pydantic model and converts it to a dict on save.
    - SQLAlchemy engine JSON-encodes the dict to a string.
    RETRIEVING:
    - Pulls the string from the database.
    - SQLAlchemy engine JSON-decodes the string to a dict.
    - Uses the dict to create a pydantic model.
    """

    impl = JSONB(none_as_null=True)

    def __init__(self, pydantic_model: type[BaseModel]):
        super().__init__()
        self.pydantic_model = pydantic_model

    def process_bind_param(self, model: BaseModel, *args):
        return model.model_dump(mode="json") if model else None

    def process_result_value(self, value: dict, *args):
        return self.pydantic_model.model_validate(value) if value else None
