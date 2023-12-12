from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from schedulers.stock import GetStockRankModule


class OttyTask:
    def __init__(self):
        # 배경 스케줄러 생성
        self.scheduler = BackgroundScheduler({'apscheduler.timezone': 'UTC'})
        self.StockRankModule = GetStockRankModule()
        # 작업 스케줄링
        self.scheduler.add_job(self.do_task, 'cron', minute='*/1')

    def do_task(self):
        # Cron 작업을 수행할 코드 작성
        # 예시로 현재 시간을 출력해보겠습니다.
        print("현재 시간은:", datetime.now())
        self.StockRankModule.start_module()

    def start(self):
        # 스케줄러 시작
        self.scheduler.start()

    def stop(self):
        # 스케줄러 종료
        self.scheduler.shutdown()