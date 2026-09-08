import pandas as pd
import sqlalchemy as s
from work_card import db
from sqlalchemy import text,select
from sqlalchemy.orm import Session
from work_card.date import first_day_of_month
from sqlalchemy.sql import func
from work_card.utils import delete_dupl,resummarize,get_project_root
from work_card.card import import_expired,get_engine
from datetime import datetime

# r = pd.read_excel('Result_5.xlsx')
conf = db.DbConf(user='root',password='root',address='127.0.0.1',db_name='cars_db',port=3306)

# delete_dupl(conf)

resummarize(conf)
# import_expired()



