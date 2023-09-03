from sqlalchemy import Column, Text, Integer, Date

from models.sqlalchemy.base import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    tg_user_id = Column(Integer, nullable=False)
    last_name = Column(Text, nullable=False)
    first_name = Column(Text, nullable=False)
    middle_name = Column(Text, nullable=False)
    birthdate = Column(Date, nullable=False)

    def __repr__(self):
        return f"<Profile({self.tg_user_id=}, {self.last_name=}, {self.first_name=}, " \
               f"{self.middle_name=}, {self.birthdate=})>"
