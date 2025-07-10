import enum
from xmlrpc.client import DateTime
from app.database.db import Base
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Table,
)
from sqlalchemy.orm import relationship
from app.database.db import Base
from sqlalchemy.types import Enum

# Many to Many relationship
user_role_table = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)


class Usersignup(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)

    roles = relationship("Role", secondary=user_role_table, back_populates="users")
    # user = relationship("UserRole", back_populates="user")


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    products = relationship("Product", back_populates="brand")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    name = Column(String, index=True)
    active = Column(Boolean, default=True)
    product_image = Column(Text, nullable=True)

    brand = relationship("Brand", back_populates="products")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    active = Column(Boolean, default=True)

    users = relationship(
        "Usersignup", secondary=user_role_table, back_populates="roles"
    )
    permissions = relationship("Permission", back_populates="roles")


# class UserRole(Base):
#     __tablename__ = "user_role"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

#     user = relationship("Usersignup", back_populates="user")


class Modules(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    permission = relationship("Permission", back_populates="module")


class AccessName(enum.Enum):
    READ = "READ"
    READ_WRITE = "READ_WRITE"
    NONE = "NONE"


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    access_type = Column(Enum(AccessName))
    role_id = Column(Integer, ForeignKey(Role.id))
    module_id = Column(Integer, ForeignKey(Modules.id))

    roles = relationship("Role", back_populates="permissions")
    module = relationship("Modules", back_populates="permission")


class Email_token(Base):
    __tablename__ = "email_token"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), index=True)
    reset_code = Column(String(50), index=True)
    status = Column(Boolean, default=True)
    expired_in = Column(DateTime)
