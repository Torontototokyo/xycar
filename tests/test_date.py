from work_card import date as dt
from work_card.db import ot_record,init_engine,DbConf
from sqlalchemy.orm import Session


def get_engine():
    conf = DbConf(user='root',password='root',address='127.0.0.1',port=3306,db_name='cars_db')
    return init_engine(conf)

def test_get_free_hours_between():
    r = dt.get_free_hours_between('2026-06-10','2026-08-09')
    assert r == 720

    r = dt.get_free_hours_between('2026-06-10','2026-08-10')
    assert r == 732

    r = dt.get_free_hours_between('2026-06-10','2026-08-11')
    assert r == 744

    r = dt.get_free_hours_between('2026-06-10','2026-08-17')
    assert r == 816

    r = dt.get_free_hours_between('2026-03-12','2026-10-08')
    assert r == 1896


def test_recursive_count_months():
    r = dt.recursive_count_months('2026-06-10','2026-08-09')
    assert r == 2

    r = dt.recursive_count_months('2026-06-10','2026-08-10')
    assert r == 3

    r = dt.recursive_count_months('2026-06-10','2027-08-11')
    assert r == 15

    r = dt.recursive_count_months('2026-06-10','2027-08-17')
    assert r == 15



def test_sub_hours():


    r = dt.sub_hours('2026-08-01 09:27:13', '2026-07-16 18:31:37')

    assert r == [{'fd': '2026-07-01', 'h': 365.47}, {'fd': '2026-08-01', 'h': 9.45}]

    r = dt.sub_hours('2026-02-19 01:23:34', '2026-01-19 01:23:34')
    
    assert r == [{'fd': '2026-01-01', 'h': 310.61}, {'fd': '2026-02-01', 'h': 433.39}]

    r = dt.sub_hours('2026-01-31 23:59:59','2026-01-31 12:09:46')
    
    assert r == [{'fd': '2026-01-01', 'h': 11.84}]


def test_seperate_date_into_months():

    r = dt.seperate_date_into_months(start_date='2025-11-03',end_date='2026-03-08')

    assert r == [['2025-11-03', '2025-11-30'], '2025-12-01', '2026-01-01', '2026-02-01', ['2026-03-01', '2026-03-08']]

    r = dt.seperate_date_into_months(start_date='2025-11-03',end_date='2025-11-30')

    assert r == [['2025-11-03', '2025-11-30']]


def test_ot_record():

    car_no = '川-GRT678'


    engine = get_engine()
    r = ot_record(car_no,session=Session(engine))

    assert r == 45.57