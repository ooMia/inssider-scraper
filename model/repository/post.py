from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.repository import User

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from model.repository._base import Base, TimestampMixin


class Post(MappedAsDataclass, Base, TimestampMixin):
    __tablename__ = "posts"

    # 1. PK
    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, doc="게시글 PK", init=False
    )

    # 2. 필수값
    title: Mapped[str] = mapped_column(String(255), nullable=False, doc="게시글 제목")
    content: Mapped[str] = mapped_column(Text, nullable=False, doc="게시글 내용")
    media_url: Mapped[str] = mapped_column(String(255), nullable=False, doc="게시글 미디어 URL")
    media_upload_time: Mapped[str] = mapped_column(
        DateTime, nullable=False, doc="미디어 업로드 시점"
    )

    # 3. 관계 필드 (init=True)
    user: Mapped["User"] = relationship(
        "User",
        back_populates="posts",
        doc="작성자 객체",
        init=True,
    )
    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="posts",
        doc="게시글이 속한 카테고리",
        init=True,
        uselist=False,
    )

    # 4. 외래키 (init=False)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
        doc="작성자 ID",
        init=False,
    )
    category_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("categories.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
        doc="카테고리 ID",
        init=False,
    )

    # 5. 옵션 관계 (default_factory=list, init=True)
    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="post_tags",
        back_populates="posts",
        default_factory=list,
        doc="게시글에 달린 태그들",
        init=True,
    )


class Category(MappedAsDataclass, Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, doc="카테고리 PK", init=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, doc="카테고리 이름")

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="category",
        default_factory=list,
        doc="카테고리에 속한 게시글 목록",
    )

    upper_category_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("categories.id", ondelete="CASCADE"), nullable=True, default=None
    )

    upper_category: Mapped["Category"] = relationship(
        "Category",
        remote_side="Category.id",  # indicates many-to-one relationship
        back_populates="sub_categories",
        default=None,
        doc="상위 카테고리",
    )

    sub_categories: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="upper_category",
        cascade="all, delete-orphan",
        default_factory=list,
        doc="하위 카테고리 목록",
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


class Comment(MappedAsDataclass, Base, TimestampMixin):
    __tablename__ = "comments"

    # 1. PK
    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, doc="댓글 PK", init=False
    )

    # 2. 내용 (soft-delete 지원: None 허용)
    content: Mapped[str | None] = mapped_column(Text, nullable=True, doc="댓글 내용 (삭제 시 None)")

    # 3. 외래키
    post_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("posts.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        doc="게시글 ID",
        init=False,
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
        doc="작성자 ID",
        init=False,
    )

    # 4. 대댓글(부모 댓글) 기능
    parent_comment_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("comments.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
        doc="부모 댓글 ID (대댓글용)",
    )
    parent_comment: Mapped["Comment"] = relationship(
        "Comment",
        remote_side="Comment.id",
        back_populates="child_comments",
        default=None,
        doc="부모 댓글",
    )
    child_comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="parent_comment",
        default_factory=list,
        doc="대댓글 목록",
    )


# users : detail one-to-one
# introduction : text
# category: post one-to-one
# upload_시간: 해당 미디어가 업로드 된 시점
# 회원가입 규정에 따라 삭제 대신 일정 기간 보관
