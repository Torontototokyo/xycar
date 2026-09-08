import re
from datetime import datetime
import pandas as pd
import os
import work_card.date as date
from pathlib import Path
from work_card.db import Card,CarParkingOT,DbConf,init_engine
import sqlalchemy as s
from sqlalchemy.orm import Session

def get_engine():
    conf = DbConf(user='root',password='root',db_name='cars_db',address='127.0.0.1',port=3306)
    return init_engine(conf)



def import_expired():

    engine = get_engine()
    with Session(engine) as session:
        

        stmt = s.select(CarParkingOT);
        res = session.execute(stmt).scalars().first()

        print(getattr(res,'id',None))
            
        # s.select(Card.id).where(Card.车牌号码 == )
