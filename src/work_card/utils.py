import re
import sys
import os
import sqlalchemy as s
from work_card import db
from sqlalchemy import text
from sqlalchemy.orm import Session
from pathlib import Path
from sqlalchemy.sql import func
from work_card.date import first_day_of_month
from datetime import datetime

def get_project_root():
    """获取项目根目录"""
    # 当前文件路径
    current_file = Path(__file__).resolve()

    # 获取祖父目录（上两级）
    grandparent_dir = current_file.parent.parent.parent

    return grandparent_dir


def resummarize(conf):
    engine = db.init_engine(conf)
    with Session(engine) as session:
        stmt = s.select(db.Card).where(db.Card.卡状态.in_(['正常', '临期','过期']));

        start_dt = '2026-09-01'

        result = session.execute(stmt).scalars().all()

        for card in result:
            car_no = card.车牌号码
            db.update_or_insert_car_leave_log_summery_by_month(car_no, start_dt,engine)
           

def delete_dupl(conf):
    engine = db.init_engine(conf)
    with Session(engine) as session:

 


    # stmt = s.select(db.Card).where(db.Card.超时小时 > 0);

    # result = session.execute(stmt).scalars().all()


    # for _,row in enumerate(result):

    #     car_no = row.车牌号码

    #     print(f'正在处理车牌号: {car_no}')

    #     now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     today = datetime.datetime.now().strftime('%Y-%m-%d')
    #     stmt = s.insert(db.CarParkingOT).values(
    #         car_no=car_no,
    #         hours=row.超时小时,
    #         arose_at=today,
    #         created_at=now,
    #         updated_at=now
    #     )
    #     session.execute(stmt)

    #     session.commit()
        result = session.execute(text("SELECT `出场时间`, `入场时间`,`车牌号码`, COUNT(*) as duplicate_count \
    FROM car_leave_logs \
    GROUP BY `出场时间`, `入场时间`,`车牌号码` \
    HAVING COUNT(*) > 1;"))

        rows = result.fetchall()
        for row in rows:

            leave_time = row[0];
            enter_time = row[1];

            car_no = row[2];

            stmt = s.select(db.Logs.id).where(db.Logs.入场时间 == enter_time)\
            .where(db.Logs.出场时间 == leave_time)\
            .where(db.Logs.车牌号码 == car_no)\
            .where(db.Logs.deleted_at == None)

            res = session.execute(stmt).first()


            update = s.update(db.Logs).where(db.Logs.id != res.id)\
            .where(db.Logs.入场时间 == enter_time)\
            .where(db.Logs.出场时间 == leave_time)\
            .where(db.Logs.车牌号码 == car_no)\
            .values(deleted_at = func.now())
            

            ___r = session.execute(update)
        #     # for _row in res:
        #     print(___r)
        session.commit()


def get_resource_path(relative_path):
    """获取打包后资源的绝对路径"""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # 程序被打包运行时，资源在 sys._MEIPASS 目录下
        base_path = sys._MEIPASS
    else:
        # 开发环境下，资源就在脚本的当前目录
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def chinese_duration_to_hours(text: str) -> float:
    """Convert '2天3小时15分30秒' → total hours (float)"""
    if not isinstance(text, str) or not text.strip():
        return 0.0
    
    text = text.strip()
    
    days    = re.search(r'(\d+)\s*天', text)
    hours   = re.search(r'(\d+)\s*小时', text)
    minutes = re.search(r'(\d+)\s*分', text)
    seconds = re.search(r'(\d+)\s*秒', text)
    
    total = 0.0
    if days:    total += int(days.group(1)) * 24
    if hours:   total += int(hours.group(1))
    if minutes: total += int(minutes.group(1)) / 60.0
    # if seconds: total += int(seconds.group(1)) / 3600.0
    
    return round(total, 2)   # Change to 2 if you prefer

