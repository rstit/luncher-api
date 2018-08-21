from sqlalchemy import Column, Integer, String, DateTime, func


class SurrogatePK:
    """A mixin that adds a surrogate integer 'primary key' column named ``id``
    to any declarative-mapped class."""

    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)


class ValueMixin:
    __table_args__ = {'extend_existing': True}

    value = Column(String, unique=True, nullable=False)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.value}"


class TimeSign:
    __table_args__ = {'extend_existing': True}

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(),
                        onupdate=func.now())
