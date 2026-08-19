import pandas as pd
import sqlalchemy as s
from work_card import db
from sqlalchemy.orm import Session
import datetime
# r = pd.read_excel('Result_5.xlsx')
engine = db.init_engine()
with Session(engine) as session:

    # stmt = s.select(db.Card).where(db.Card.卡状态.in_(['正常', '临期']));

    # start_dt = '2026-08-01'

    # result = session.execute(stmt).scalars().all()

    # for card in result:
    #     car_no = card.车牌号码
    #     db.update_or_insert_car_leave_log_summery_by_month(car_no, start_dt)


    stmt = s.select(db.Card).where(db.Card.超时小时 > 0);

    result = session.execute(stmt).scalars().all()


    for _,row in enumerate(result):

        car_no = row.车牌号码

        print(f'正在处理车牌号: {car_no}')

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        stmt = s.insert(db.CarParkingOT).values(
            car_no=car_no,
            hours=row.超时小时,
            arose_at=today,
            created_at=now,
            updated_at=now
        )
        session.execute(stmt)

        session.commit()
    # for _,row in r.iterrows():


    #     stmt = s.select(db.Logs.id).where(db.Logs.入场时间 == row['入场时间'])

    #     res = session.execute(stmt).first()

    #     delete = s.delete(db.Logs).where(db.Logs.id == res.id)

    #     ___r = session.execute(delete)
    #     # for _row in res:
    #     print(___r)
    # session.commit()



