from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import EngineConn
from models import Finance, Stock_Rank
from schedulers.task import OttyTask


app = FastAPI()

engine = EngineConn()
session = engine.sessionmaker()

# 공유 폴더 접근 가능하게
app.mount("/public", StaticFiles(directory="public"), name="static")

my_task = OttyTask()

@app.on_event("startup")
async def startup_event():
    # Cron 작업 시작
    my_task.start()

@app.on_event("shutdown")
async def shutdown_event():
    # Cron 작업 중지
    my_task.stop()

@app.get('/')
async def main():
    return "OTTY API Server"

@app.get('/news/investing')
async def api_news_investing():
    return session.query(Finance).order_by(Finance.date.desc()).limit(10).all()

@app.get('/stock_rank')
async def api_stock_rank():
    return session.query(Stock_Rank).order_by(Stock_Rank.market_cap.desc()).limit(100).all()