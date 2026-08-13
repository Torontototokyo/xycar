from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta


YMD = '%Y-%m-%d'
FM_DAY_END = '%Y-%m-%d 23:59:59'
FM_DAY_START = '%Y-%m-%d 00:00:00'
FM_YMDT = "%Y-%m-%d %H:%M:%S"
HOUR_PER_MONTH = 360


def last_day_of_month(any_day):
    # The day 28 exists in every month. 4 days later, it's always next month
    next_month = any_day.replace(day=28) + timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    return next_month - timedelta(days=next_month.day)


def seperate_date_into_months(start_date,end_date):

    if type(start_date) == str:

        start_date = datetime.strptime(start_date,YMD)

    if type(end_date) == str:

        end_date = datetime.strptime(end_date,YMD)

    first_day_of_month_start_date = start_date.replace(day=1).strftime('%Y-%m-%d')

    date_flag = first_day_of_month_start_date

    first_day_of_month_end_date = end_date.replace(day=1).strftime('%Y-%m-%d')

    result = []

    if  (end_date - start_date).days < 30 or start_date + relativedelta(months=1) > end_date:

        return [[start_date.strftime(YMD),end_date.strftime(YMD)]]

    
    if start_date.strftime(YMD) == first_day_of_month_start_date :

        r = first_day_of_month_start_date

    else:
        _last_day_of_start_month = last_day_of_month(start_date.date())

        r = [start_date.strftime(YMD),_last_day_of_start_month.strftime(YMD)]

    result.append(r)

    while date_flag != first_day_of_month_end_date:
        
        # Add 1 month and set day to 1
        date_date_flag = (datetime.strptime(date_flag,YMD) + relativedelta(months=1)).replace(day=1)

        date_flag = datetime.strftime(date_date_flag,YMD)

        result.append(date_flag)
        
    
    last_d = result.pop()

    
    result.append([last_d,end_date.strftime(YMD)])
    
    return result
    




def sub_hours(datetime1,datetime2):
    K = "%Y-%m-%d %H:%M:%S"

    K2 = "%Y-%m-%d 23:59:59"

    round_to=2
    if type(datetime1) == str:
        datetime1 = datetime.strptime(datetime1,K)
    if type(datetime2) == str:
        datetime2 = datetime.strptime(datetime2,K)


    _last_day_of_month = datetime.strftime(last_day_of_month(datetime2),K2)

    e = datetime.strptime(_last_day_of_month,K)
    
    d1 = e - datetime2 

    d2 = datetime1 - e

    if d1.total_seconds() > 0 and d2.total_seconds() > 0:
        h1 = d1.total_seconds()/3600
        h2 = d2.total_seconds()/3600
        fd1 = datetime1.replace(day=1).strftime(YMD)
        fd2 = datetime2.replace(day=1).strftime(YMD)
        return [{'fd':fd2,'h':round(h1,round_to)},{'fd':fd1,'h':round(h2,round_to)}]

    diff = datetime1 - datetime2
    hours = diff.total_seconds() / 3600

    first_day = datetime1.replace(day=1).strftime(YMD)
    return [{'fd':first_day,'h':round(hours, round_to)}]








def get_first_day_last_6_months(_date):

    INIT_DATE = '2026-05-01'
    init_date = datetime.strptime(INIT_DATE,YMD)

    my_date = datetime.strptime(_date,YMD)

    diff = init_date - my_date

    if diff.days > 0:
        return INIT_DATE
    else:
        return my_date.strftime(YMD)

    today = datetime.now().date()

    start_date = datetime.strptime(_date,'%Y-%m-%d').date()

    start_date_diff = today - start_date


    while start_date_diff.days > 6 * 30:
        start_date = start_date + relativedelta(months=1)
        start_date_diff = today - start_date
    
    return start_date.strftime('%Y-%m-%d')



def get_free_hours_between(date_start_string,date_end_str)->int:

    date_start_string = get_first_day_last_6_months(date_start_string)
    
    months = recursive_count_months(date_start_string,date_end_str)

    start_date = datetime.strptime(date_start_string,YMD)

    end_date = datetime.strptime(date_end_str,YMD)

    r = start_date + relativedelta(months=months)

    if r == end_date + relativedelta(days=1):
        return months * HOUR_PER_MONTH
    if r > end_date + relativedelta(days=1):
        reduce_days = (r - end_date).days - 2
        #'2026-06-10','2026-08-17' 8 days
        return int(months * HOUR_PER_MONTH - round(reduce_days / 30 * HOUR_PER_MONTH,2))
    if r < end_date + relativedelta(days=1):
        reduce_days = (end_date - r).days - 2
        return int(months * HOUR_PER_MONTH + round(reduce_days / 30 * HOUR_PER_MONTH,2))


def recursive_count_months(start_date,end_date):
    if type(start_date) == str:

        start_date = datetime.strptime(start_date,YMD)

    if type(end_date) == str:
        
        end_date = datetime.strptime(end_date,YMD)
    if start_date > end_date:
        return 0

    next_month = start_date + relativedelta(months=1)

    if next_month > end_date:
        return 1
    else:
        return 1 + recursive_count_months(next_month,end_date)




