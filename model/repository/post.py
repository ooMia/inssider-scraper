from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.repository import User

from sqlalchemy import BigInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.repository._base import Base, TimestampMixin, users_id_fk


class Post(Base, TimestampMixin):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, doc="게시글 PK"
    )
    user_id: Mapped[int] = mapped_column(BigInteger, users_id_fk(), index=True, doc="작성자 ID")
    title: Mapped[str] = mapped_column(String(255), nullable=False, doc="게시글 제목")
    content: Mapped[str] = mapped_column(Text, nullable=False, doc="게시글 내용")

    user: Mapped["User"] = relationship("User", back_populates="posts")
