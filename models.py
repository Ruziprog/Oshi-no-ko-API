from sqlalchemy import String, ForeignKey, Table, Column, UniqueConstraint
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
        String(255),
        nullable=False
    )


class Character(Base):
    __tablename__ = "characters"
    
    
    __table_args__ = (
    UniqueConstraint("name", name="uq_characters_name"),
)
    
    id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    age: Mapped[int] = mapped_column(nullable=False)

    description: Mapped[str] = mapped_column(
        String(200),
        nullable=True
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "character"
    }


class Idol(Character):
    __tablename__ = "idols"

    id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        ForeignKey("characters.id", ondelete="CASCADE"),
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
    
    __table_args__ = (
    UniqueConstraint("title", name="uq_songs_title"),
)

    id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    idols: Mapped[list["Idol"]] = relationship(
        "Idol",
        secondary=song_idols,
        back_populates="songs"
    )