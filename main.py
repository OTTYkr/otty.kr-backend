from fastapi import FastAPI, Depends, Response
from fastapi.staticfiles import StaticFiles
from database import EngineConn
from models import Finance, Stock_Rank, KrCapRank
from schedulers.task import OttyTask
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import datetime

# 실행 방법 : 터미널 gunicorn --bind 0:8000 main:app --worker-class uvicorn.workers.UvicornWorker

app = FastAPI()

engine = EngineConn()
session = engine.sessionmaker()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


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
async def main(response: Response):
    response.headers['content-type'] = 'application/json; charset=utf-8;'
    return "오티 - 오늘의 티커 v1.1"

class NewsItem(BaseModel):
    id: int
    provider: str
    post_num: int
    title: str
    date: datetime.datetime
    content: str


@app.get('/news/investing', response_model=List[NewsItem])
async def api_news_investing(response: Response, db: Session = Depends(get_db)):
    response.headers['content-type'] = 'application/json; charset=utf-8;'
    return db.query(Finance).order_by(Finance.date.desc()).limit(10).all()

@app.get('/stock_rank')
async def api_stock_rank(response: Response, db: Session = Depends(get_db)):
    response.headers['content-type'] = 'application/json; charset=utf-8;'
    return db.query(Stock_Rank).order_by(Stock_Rank.market_cap.desc()).limit(100).all()


@app.get('/kr_cap_rank')
async def api_stock_rank(response: Response, db: Session = Depends(get_db)):
    response.headers['content-type'] = 'application/json; charset=utf-8;'
    return db.query(KrCapRank).order_by(KrCapRank.market_cap.desc()).limit(100).all()