"""SQLAlchemy tables for users, profiles, skills, projects, and preferences."""

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
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
