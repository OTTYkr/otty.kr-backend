from sqlalchemy import Column, TEXT, INT, VARCHAR, DATETIME, FLOAT, BIGINT, BOOLEAN
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


class KrCapRank(Base):
    __tablename__ = "kr_cap_rank"

    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    exchange = Column(VARCHAR, nullable=False)
    symbol = Column(VARCHAR, nullable=False)
    name = Column(VARCHAR, nullable=False)
    market_price = Column(INT, nullable=True)
    market_change = Column(INT, nullable=True)
    market_change_percent = Column(FLOAT, nullable=True)
    shares_outstanding = Column(BIGINT, nullable=True)
    market_cap = Column(BIGINT, nullable=True)

class KrStocks(Base):
    __tablename__ = "kr_stocks"

    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    symbol = Column(VARCHAR, nullable=False)
    name = Column(VARCHAR, nullable=False)
    regular_price = Column(INT, nullable=True)
    change_per = Column(FLOAT, nullable=True)
    market_cap = Column(BIGINT, nullable=True)
    islogo = Column(BOOLEAN, nullable=True)
    exchange = Column(VARCHAR, nullable=True)