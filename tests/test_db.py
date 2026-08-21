from sqlalchemy import create_engine,MetaData,select,Column,Table,DateTime as DT
from sqlalchemy.types import Integer, Float, Text, DateTime,DECIMAL
from sqlalchemy.orm import Session,DeclarativeBase,mapped_column,relationship,Mapped
from sqlalchemy import insert,update,String
from sqlalchemy.sql import func
from sqlalchemy.exc import MultipleResultsFound
from work_card.db import CarParkingOT,init_engine,init_engine_sql
from sqlalchemy import text


def test_scalar_one_or_none():

    
    engine = init_engine()
    
    car_no = '川-GRT678'
    
    with Session(engine) as session:
    
        stmt = select(CarParkingOT).where(CarParkingOT.car_no == car_no)

        res = session.execute(stmt).scalar_one_or_none()
        assert res is not None

        assert res.car_no == car_no

        assert res.id == 1

        not_exist_car_no = '户-GRT678'


        stmt = select(CarParkingOT).where(CarParkingOT.car_no == not_exist_car_no)
        
        res = session.execute(stmt).scalar_one_or_none()

        assert res == None

def test_raw_query():
    
    engine = init_engine_sql()
    with Session(engine) as session:
        result = session.execute(
        text("""
SELECT
  r.trx_id AS waiting_trx_id,          -- 等待中的事务ID
  r.trx_mysql_thread_id AS waiting_thread, -- 等待中的会话线程ID
  r.trx_query AS waiting_query,        -- 等待中的SQL
  b.trx_id AS blocking_trx_id,         -- 阻塞者的事务ID
  b.trx_mysql_thread_id AS blocking_thread,-- 阻塞者的会话线程ID
  b.trx_query AS blocking_query        -- 阻塞者正在执行的SQL
FROM
  information_schema.INNODB_LOCK_WAITS w
  INNER JOIN information_schema.INNODB_TRX b
    ON b.trx_id = w.blocking_trx_id     -- 关联阻塞者的事务
  INNER JOIN information_schema.INNODB_TRX r
    ON r.trx_id = w.requesting_trx_id;  -- 关联请求者(被阻塞)的事务
        """)
        )
        rows = result.fetchall()
        print(rows)  # 打印列表

        assert False