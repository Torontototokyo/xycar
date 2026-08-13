import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import date
import time

import re

def cheak_header(df):
    HEADER_NO = 0
    header = df.head(HEADER_NO)
    if "Unnamed: 15" in header:
        # update the column name to "占用时长"
        df.rename(columns={"Unnamed: 15": "占用时长"}, inplace=True)


def save_excel(df, filename):
    df.to_excel(filename, index=False)


def confirm_start_date_end_date(row):
    start_date = row["开始期限"]
    end_date = row["截止期限"]
    card_no = row['车牌号码']
    if pd.isnull(start_date) or pd.isnull(end_date):
        print(f"Row {row.name}: Start date or end date is missing.")
    else:
        # the day of start date - 1 eq the day of end date
        if (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days != 1:
            print(f"Row {row.name}: Start date and end date are not consistent.")
        else:
            print(f"Row {row.name}: Start date and end date are consistent.")
        # print(f"Row {row.name}: Start date is {start_date}, End date is {end_date}.")

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
        
    arr = get_start_counting_date_arr(date_start_string)
    
    last = arr.pop()

    count = len(arr)

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


# program_start_time = time.perf_counter()

# print(f'start time {program_start_time}')

# FN= "车场免费卡报表.xlsx"

# SAVED_FN= "车场免费卡报表——修改后.xlsx"

# RECORDS = "车辆出场记录_20260716090836783.xlsx"

# RECORDS = "粤-EY7N61.xlsx"

# CARD = "粤-EY7N61"

# today = datetime.today().strftime("%Y-%m-%d")

# df = pd.read_excel(FN,sheet_name="SheetJS",header=0,skiprows=0)

# df = df[df['套餐名称'] == '工作卡']

# df = df[df['卡状态'].isin(['临期', '正常'])]

# # df = df[df['车牌号码'] == CARD]


# cheak_header(df)

# df_lq = None

# df_zc = None

# HOUR_PER_MONTH = 360

# columns = df.columns.to_list()

# columns.append('总免费停车时长')
# columns.append('实际停车时长')
# columns.append('超时小时')


# for index, row in df.iterrows():
   
         
#     date_start = row['开始期限']

#     date_end = row['截止期限']

#     card = row['车牌号码']

    
#     # Same day last month

#     total_hours = get_hours_by_dates_2(date_start,date_end)

#     rl = row.to_list()

#     rl.append(total_hours)

#     total_pk_hours= 0

#     if total_hours > 0:

        
#         df_sum = pd.read_excel(RECORDS,sheet_name='数据页1')
#         # df_sum = pd.read_excel(RECORDS,sheet_name='Sheet1')
        
#         df_pk = df_sum[df_sum['车牌号码'] == card]

#         df_pk = df_pk[df_pk['入场时间'] > date_start]

#         # pk_columns = df_pk.columns.to_list()

#         # pk_columns.append('停车时长')
#         # new_dff = pd.DataFrame(columns=pk_columns)
#         for pk_index,pk_row in df_pk.iterrows():
        
#             pk_hours =chinese_duration_to_hours(pk_row['停车时长'])
            
#             # pk_row['停车时长'] = pk_hours
#             total_pk_hours+=pk_hours
#             # new_row = pd.DataFrame([pk_row], columns=pk_columns)
#             # new_dff = pd.concat([new_dff,new_row],ignore_index=True)
#         # new_dff.to_excel('12.xlsx',index=False)
#     rl.append(total_pk_hours)

#     over_hours = (0,total_pk_hours - total_hours) [total_pk_hours > total_hours ]
    
#     rl.append(over_hours)

#     new_row = pd.DataFrame([rl], columns=columns)
    
#     df_lq = pd.concat([df_lq, new_row], ignore_index=True)

# df_lq.to_excel(f'{datetime.now().strftime("%Y-%m-%d")}#超时转临停车辆.xlsx',index=False)

# program_end_time = time.perf_counter()

# diff = program_end_time - program_start_time


# print(f"运行时间: {program_end_time - program_start_time:.6f} 秒")


