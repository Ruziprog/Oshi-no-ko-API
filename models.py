from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from sqlalchemy import UUID as SQL_UUID

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), primary_key=True, default=uuid4)

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    age: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(String(200))
    role: Mapped[str] = mapped_column(String(50))

    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "character"
    }

class Idol(Character):
    __tablename__ = "idols"

    id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),          
        ForeignKey("characters.id"),     
        primary_key=True,               
        default=uuid4                    
    )


    songs: Mapped[list["Song"]] = relationship(
        "Song", 
        back_populates="idol"
        )

    __mapper_args__ = {
        "polymorphic_identity": "idol"
        }

class Song(Base):
    __tablename__ = "songs"

    id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(100))
    idol_id: Mapped[int] = mapped_column(
        ForeignKey("idols.id")
    )

    idol: Mapped["Idol"] = relationship(
        back_populates="songs"
    )