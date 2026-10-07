from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from uuid import UUID, uuid4

from sqlalchemy import UUID as SQL_UUID


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

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

    id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True
    )

    age: Mapped[int] = mapped_column()

    description: Mapped[str] = mapped_column(
        String(200)
    )

    role: Mapped[str] = mapped_column(
        String(50)
    )

    type: Mapped[str] = mapped_column(
        String(50)
    )

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "character"
    }


class Idol(Character):
    __tablename__ = "idols"

    id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        ForeignKey("characters.id"),
        primary_key=True
    )

    songs: Mapped[list["Song"]] = relationship(
        "Song",
        secondary=lambda: song_idols,
        back_populates="idols"
    )

    __mapper_args__ = {
        "polymorphic_identity": "idol"
    }


song_idols = Table(
    "song_idols",
    Base.metadata,

    Column(
        "song_id",
        SQL_UUID(as_uuid=True),
        ForeignKey("songs.id", ondelete="CASCADE"),
        primary_key=True
    ),

    Column(
        "idol_id",
        SQL_UUID(as_uuid=True),
        ForeignKey("idols.id", ondelete="CASCADE"),
        primary_key=True
    )
)


class Song(Base):
    __tablename__ = "songs"

    id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    title: Mapped[str] = mapped_column(
        String(100)
    )

    idols: Mapped[list["Idol"]] = relationship(
        "Idol",
        secondary=song_idols,
        back_populates="songs"
    )