import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Favorite(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'favorites'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    site = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __str__(self):
        return f"{self.id} {self.name}"
