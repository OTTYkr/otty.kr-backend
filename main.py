from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import EngineConn
from models import Finance, Stock_Rank


app = FastAPI()

engine = EngineConn()
session = engine.sessionmaker()

app.mount("/public", StaticFiles(directory="public"), name="static")

@app.get('/')
async def main():
    return "OTTY API Server"

@app.get('/news/investing')
async def api_news_investing():
    return session.query(Finance).order_by(Finance.date.desc()).limit(10).all()

@app.get('/stock_rank')
async def api_stock_rank():
    return session.query(Stock_Rank).order_by(Stock_Rank.market_cap.desc()).limit(100).all()