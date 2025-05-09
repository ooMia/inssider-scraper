from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Address(Base):
    """[experimental] 주소 테이블 모델"""

    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"))

    # User와의 관계 설정 (다대일)
    user = relationship("User", back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


class User(Base):
    """[experimental] 사용자 테이블 모델"""

    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    fullname = Column(String(100))

    # Address와의 일대다 관계 설정
    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Dev(Base):
    """[experimental]"""

    __tablename__ = "dev"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))

    def __repr__(self):
        return f"<Dev(id={self.id}, name='{self.name}')>"
