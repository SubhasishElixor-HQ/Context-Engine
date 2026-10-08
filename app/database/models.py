"""SQLAlchemy tables for users, profiles, skills, projects, and preferences."""

from datetime import datetime

from sqlalchemy import (
    JSON,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class UserRecord(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    profile: Mapped["ProfileRecord"] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    skills: Mapped[list["SkillRecord"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    projects: Mapped[list["ProjectRecord"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    preferences: Mapped[list["PreferenceRecord"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    memories: Mapped[list["MemoryRecord"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    documents: Mapped[list["DocumentRecord"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class ProfileRecord(Base):
    __tablename__ = "profiles"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(200))
    education: Mapped[str] = mapped_column(String(300))
    user: Mapped[UserRecord] = relationship(back_populates="profile")


class SkillRecord(Base):
    __tablename__ = "skills"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_skill_per_user"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100))
    user: Mapped[UserRecord] = relationship(back_populates="skills")


class ProjectRecord(Base):
    __tablename__ = "projects"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_project_per_user"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(300))
    user: Mapped[UserRecord] = relationship(back_populates="projects")


class PreferenceRecord(Base):
    __tablename__ = "preferences"
    __table_args__ = (UniqueConstraint("user_id", "key", name="uq_preference_per_user"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    key: Mapped[str] = mapped_column(String(100))
    value: Mapped[str] = mapped_column(String(500))
    user: Mapped[UserRecord] = relationship(back_populates="preferences")


class MemoryRecord(Base):
    __tablename__ = "memories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(String(2000))
    category: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    user: Mapped[UserRecord] = relationship(back_populates="memories")


class DocumentRecord(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped[UserRecord] = relationship(back_populates="documents")
    chunks: Mapped[list["DocumentChunkRecord"]] = relationship(
        back_populates="document", cascade="all, delete-orphan",
        order_by="DocumentChunkRecord.chunk_index",
    )


class DocumentChunkRecord(Base):
    __tablename__ = "document_chunks"
    __table_args__ = (
        UniqueConstraint("document_id", "chunk_index", name="uq_chunk_per_document"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE")
    )
    chunk_index: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(Text)

    document: Mapped[DocumentRecord] = relationship(back_populates="chunks")
    embedding: Mapped["DocumentEmbeddingRecord | None"] = relationship(
        back_populates="chunk",
        cascade="all, delete-orphan",
        uselist=False,
    )


class DocumentEmbeddingRecord(Base):
    __tablename__ = "document_embeddings"

    chunk_id: Mapped[int] = mapped_column(
        ForeignKey("document_chunks.id", ondelete="CASCADE"),
        primary_key=True,
    )
    vector: Mapped[list[float]] = mapped_column(JSON)

    chunk: Mapped[DocumentChunkRecord] = relationship(back_populates="embedding")
