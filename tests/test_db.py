from sqlalchemy import create_engine,MetaData,select,Column,Table,DateTime as DT
from sqlalchemy.types import Integer, Float, Text, DateTime,DECIMAL
from sqlalchemy.orm import Session,DeclarativeBase,mapped_column,relationship,Mapped
from sqlalchemy import insert,update,String
from sqlalchemy.sql import func
from sqlalchemy.exc import MultipleResultsFound
from work_card.db import CarParkingOT,init_engine


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