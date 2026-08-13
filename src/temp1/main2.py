import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import date
import math
HOUR_PER_MONTH = 360

RECORDS = "车辆出场记录_20260716090836783.xlsx"

df = pd.read_excel(RECORDS)

df = df[df['车牌号码'] == '粤-EY7N61']


df.to_excel('粤-EY7N61.xlsx',index=False)
def get_start_counting_date(start_date_string) -> date:
    today = datetime.now().date()

    date = datetime.strptime(start_date_string, "%Y-%m-%d").date()

    next_month = date + relativedelta(months=1) 

    f = next_month < today

    if f:
    
        r = next_month + relativedelta(months=1) 
        f = r < today
    else:
        next_month = date

    if f:

        while f:

            next_month = next_month + relativedelta(months=1) 

            f = (next_month + relativedelta(months=1) ) < today

            start_date_string = next_month.strftime('%Y-%m-%d')
            
        

    return next_month


    
def get_hours_by_dates(start_counting_date,date_end_str):
    
    today = datetime.now().date()

    date_end = datetime.strptime(date_end_str,'%Y-%m-%d').date()

    diff = date_end - today

    if diff.days > 30:
        
        return HOUR_PER_MONTH

    else:
    
        diff = today - start_counting_date + relativedelta(days=1)
        
        
        return int(diff.days / 30 * HOUR_PER_MONTH) 

def get_start_counting_date_arr(start_date_string):

    
    today = datetime.now().date()

    date = datetime.strptime(start_date_string, "%Y-%m-%d").date()

    arr = [date]

    next_month = date + relativedelta(months=1) 

    f = next_month < today

    if f:
    
        r = next_month + relativedelta(months=1) 
        arr.append(next_month)
        
        f = r < today
    else:
        next_month = date

        return [next_month]

    if f:

        while f:

            next_month = next_month + relativedelta(months=1) 

            arr.append(next_month)
            f = (next_month + relativedelta(months=1) ) < today

            start_date_string = next_month.strftime('%Y-%m-%d')
            
      

    return arr

    
def get_hours_by_dates_2(date_start_string,date_end_str):

     ##最多只能统计6个月，因为出入场记录最多只能导出6个月
    
    today = datetime.now().date()

    start_date = datetime.strptime(date_start_string,'%Y-%m-%d').date()

    start_date_diff = today - start_date

    

    while start_date_diff.days > 6 * 30:
        start_date = start_date + relativedelta(months=1)
        start_date_diff = today - start_date

    date_start_string = start_date.strftime('%Y-%m-%d')

    print(date_start_string)
   

    arr = get_start_counting_date_arr(date_start_string)
    
    last = arr.pop()

    count = len(arr)
    
    today = datetime.now().date()

    date_end = datetime.strptime(date_end_str,'%Y-%m-%d').date()
   
    diff_days = (date_end - last).days
   
    if diff_days >= 28:

        diff = relativedelta(date_end,last)

        how_many_months_exact = diff.months

        _date = last + relativedelta(months=how_many_months_exact)

        how_many_days_exact = (date_end - _date).days + 1

        return int(((count + how_many_months_exact) * HOUR_PER_MONTH)  + round(how_many_days_exact / 30 * HOUR_PER_MONTH ,2))

    else:
    
        diff = today - last + relativedelta(days=1)
        
        return int(count * HOUR_PER_MONTH +round(diff.days / 30 * HOUR_PER_MONTH) )
    

r1 = get_start_counting_date('2026-06-01')
r2 = get_hours_by_dates(r1,'2026-08-01')
r3 = get_start_counting_date_arr('2026-06-01')
r4 = get_hours_by_dates_2('2026-05-28','2026-07-27')


print(r4)