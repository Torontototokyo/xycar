import db

import pandas as pd

from gather import init_engine,get_car_leave_logs_table

from sqlalchemy import create_engine,MetaData,select,Column,Table,DateTime as DT

from date import sub_hours



def create_summary_car_leave_logs(engine):

    metadata = MetaData()   

    tb = db.get_car_leave_log_summery_by_month_table(metadata=metadata)

    metadata.create_all(engine)

    return tb

def summary_leave_logs_by_month():
    
    engine = init_engine()

    metadata = MetaData()

    table = get_car_leave_logs_table(metadata=metadata)

    stem = select(table.c['车牌号码'],
                  table.c['入场时间'],
                  table.c['出场时间']).order_by(table.c['出场时间'])\
                  .execution_options(yield_per=5000)

    conn = engine.connect()

    result = conn.execute(stem)


    for chunk in result.partitions():
            for row in chunk:
                
                car_no = row[0]
                r_enter_datetime = row[1]
                r_leave_datetime = row[2]

                sp_dates = sub_hours(r_leave_datetime,r_enter_datetime)
                
                for item in sp_dates:

                    db.add_or_insert_car_leave_log_summery_by_month(car_no,item['h'],item['fd'])
        # stm = select(table.c['id']).where(table.c['开始日期'])



def summary_leave_logs_by_month_df(df:pd.DataFrame):
    
   
    for index,row in df.iterrows():

        car_no = row['车牌号码']
        r_enter_datetime = row['入场时间']
        r_leave_datetime = row['出场时间']

        sp_dates = sub_hours(r_leave_datetime,r_enter_datetime)
        
        for item in sp_dates:

            db.add_or_insert_car_leave_log_summery_by_month(car_no,item['h'],item['fd'])

