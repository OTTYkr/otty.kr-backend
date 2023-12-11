from sqlalchemy import Column, TEXT, INT, VARCHAR, DATETIME, FLOAT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Finance(Base):
    __tablename__ = "Finance"

    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    provider = Column(VARCHAR, nullable=False)
    post_num = Column(INT, nullable=True)
    title = Column(VARCHAR, nullable=False)
    date = Column(DATETIME, nullable=True)
    content = Column(TEXT, nullable=True)


class Stock_Rank(Base):
    __tablename__ = "Stock_Rank"

    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    name = Column(VARCHAR, nullable=False)
    code = Column(VARCHAR, nullable=False)
    market_cap = Column(FLOAT, nullable=False)
    price = Column(FLOAT, nullable=False)
    day_change = Column(VARCHAR, nullable=False)
    country = Column(VARCHAR, nullable=False)
    date = Column(DATETIME, nullable=True)
    dollar = Column(FLOAT, nullable=True)