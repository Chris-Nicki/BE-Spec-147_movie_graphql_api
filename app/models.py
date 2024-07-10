from app import db
from sqlalchemy.orm import Mapped, mapped_column

class Movie(db.Model):
    id: Mapped[int] = mapped_column( primary_key=True)
    title: Mapped[str] = mapped_column(db.String(150), nullable=False)
    director: Mapped[str] = mapped_column(db.String(100), nullable=False)
    release_year: Mapped[int] = mapped_column(db.Integer, nullable=False)
    genre: Mapped[str] = mapped_column(db.String(50), nullable=False)
    rating: Mapped[float] = mapped_column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Movie {self.title}>"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()