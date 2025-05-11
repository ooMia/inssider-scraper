from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.repository import User

from sqlalchemy import BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from model.repository._base import Base, TimestampMixin


class Post(MappedAsDataclass, Base, TimestampMixin):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, doc="게시글 PK"
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
        doc="작성자 ID",
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, doc="게시글 제목")
    content: Mapped[str] = mapped_column(Text, nullable=False, doc="게시글 내용")

    user: Mapped["User"] = relationship("User", back_populates="posts")

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="post_tags",
        back_populates="posts",
        doc="게시글에 달린 태그들",
    )


class PostTag(MappedAsDataclass, Base):
    __tablename__ = "post_tags"

    post_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )


class Tag(MappedAsDataclass, Base, TimestampMixin):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, doc="태그 PK")
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, doc="태그 이름")

    posts: Mapped[list["Post"]] = relationship("Post", secondary="post_tags", back_populates="tags")
