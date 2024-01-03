from pydantic import BaseModel


class Model(BaseModel):
    class Config:
        populate_by_name = True
        coerce_numbers_to_str = True
