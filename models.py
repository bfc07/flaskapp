from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


class Input(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=False)
    host: Mapped[str] = mapped_column(unique=False)
    category: Mapped[str] = mapped_column(unique=False)
    time: Mapped[str] = mapped_column(unique=False)