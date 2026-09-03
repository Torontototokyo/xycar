import argparse
import pandas as pd
import work_card.utils as utils
import math
class Conf:
    free_hour:float
    fee_per_hour:float
    max_fee:int
    
    def __init__(self,free_hour,max_fee,fee_per_hour) -> None:
        
        self.fee_per_hour = fee_per_hour
        self.max_fee = max_fee
        self.free_hour = free_hour


def get_conf(p_name)->Conf:
    default = Conf(0,0,0)
    if '马龙' in p_name:
        return Conf(free_hour=2,max_fee=20,fee_per_hour=1)
    if '龙涌' in p_name:
        return Conf(free_hour=2,max_fee=20,fee_per_hour=1)
    if '黄涌' in p_name:
        return Conf(free_hour=3,max_fee=10,fee_per_hour=0.5)
    if '三洪奇' in p_name:
        return Conf(free_hour=2,max_fee=20,fee_per_hour=1)
    return default


def compute(hours,conf:Conf)->float:

    if hours <= conf.free_hour:
        return 0
    elif hours > 24:
        quotient = hours // 24  # INT(N966/24)
        remainder = hours - (quotient * 24)  # (N966/24 - INT(N966/24)) * 24
        remainder_value = math.ceil(remainder) * conf.fee_per_hour
        return (quotient * conf.max_fee) + (conf.max_fee if remainder_value >= conf.max_fee else remainder_value)
    else:
        value = math.ceil(hours) * conf.fee_per_hour
        return conf.max_fee if value >= conf.max_fee else value

def hanledf(df):
    end = df.iloc[0];

    start = df.iloc[-1]

    car_no = start['车牌号码']

    

    start_date = start['入场时间'].date().strftime('%Y-%m-%d')
    end_date = end['入场时间'].date().strftime('%Y-%m-%d') #datetime.strptime()


    p_name = start['车场区域']

    car_no = f'{car_no}-{p_name}'

    conf = get_conf(p_name=p_name)

    total_fee = 0    

    df = df[df['出场通道'].notnull()]
    df = df[df['出场通道'].str.contains('出口')]

    df = df.assign(
        停车时长小时=lambda x: x['停车时长'].apply(utils.chinese_duration_to_hours),
        应付停车费=lambda x: x.apply(
            lambda row: compute(row['停车时长小时'], conf=conf),
            axis=1
        )
    )

    total_fee = df['应付停车费'].sum() 

    
    df.to_excel(f'{car_no}.xlsx')
    print(f'from {start_date} to {end_date} ;total fee : {round(total_fee,2)} 元')
    print(f'车牌号码：{car_no},从 {start_date} 到 {end_date} ;应付停车费 : {round(total_fee,2)} 元')
        
        

def main():
    parser = argparse.ArgumentParser(description="files")

    parser.add_argument('-f', '--excel', dest='file', help='path to logs excel file', default=None)

    args = parser.parse_args()

    file = args.file

    df = pd.read_excel(file)

    hanledf(df=df)


if __name__ == "__main__":
    main()
