import wikipedia
from sqlalchemy import *
from models import KrStocks
from database import EngineConn


wikipedia.set_lang('ko')

engine = EngineConn()
db_session = engine.sessionmaker()


if __name__ == "__main__":
    db = db_session()
    t = db.query(KrStocks).all()
    for i in t:
        if i.summary is None:
            try:
                search = wikipedia.search(f'한국: {i.symbol}')
                if len(search) == 0 or search[0] == "코스피 50":
                    q = wikipedia.search(i.name)[0]
                else:
                    q = search[0]
                i.summary = wikipedia.summary(q)
                print(f'{i.name} : {i.summary}')
            except Exception as e:
                print(f'{i.name} 에러. ({e})')
                continue

    # DB 커밋 후 종료
    db.commit()
    db.close()