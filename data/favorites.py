import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Favorite(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'favorites'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    college_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def __str__(self):
        return f"{self.user_id} {self.college_id}"
