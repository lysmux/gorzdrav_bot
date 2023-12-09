from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData(
    naming_convention={
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s',
    }
)


class BaseModel(DeclarativeBase):
    metadata = metadata
    __allow_unmapped__ = False

    def __repr__(self) -> str:
        class_ = self.__class__.__name__
        attrs = sorted(
            (k, getattr(self, k)) for k in self.__mapper__.columns.keys()
        )
        formatted_attrs = ', '.join('{}={!r}'.format(*x) for x in attrs)

        return f"{class_}({formatted_attrs})"
