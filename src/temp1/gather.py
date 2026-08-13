import pandas as pd

from utils import chinese_duration_to_hours

from db import init_engine,get_car_leave_logs_table,Card

from sqlalchemy import create_engine,MetaData,select,Column,Table,DateTime as DT

from sqlalchemy.types import Integer, Float, Text, DateTime

from date import sub_hours,last_day_of_month

from datetime import datetime

from date import FM_YMDT,FM_DAY_END

FILE_NAME = "车辆出场记录_20260717150937296.xlsx";

# MySQL connection details


# Create SQLAlchemy engine




# 读取原始Excel文件
# file_path = "车辆出场记录_20260717150937296.xlsx"
# df_dict = pd.read_excel(file_path, sheet_name=None)  # 读取所有sheet

# # 获取当前目录
# base_dir = os.path.dirname(file_path)

# for sheet_name, df in df_dict.items():
#     # 每个sheet单独保存
#     output_path = os.path.join(base_dir, f"{sheet_name}.xlsx")
#     df.to_excel(output_path, index=False)
#     print(f"已保存: {sheet_name}")


def init_data() :

    
    engine = init_engine()

    TABLE_NAME = 'car_leave_logs'

    for i in range(1,8):

        df =  pd.read_excel(f'数据页{i}.xlsx');

        # print(df)
   
        new_columns = ['id'] + list(df.columns[1:]) + ['停车时长(小时)']    

        none_df = None
        
        for index,row in df.iterrows():

            s_hours = sub_hours(row['出场时间'],row['入场时间'])
            
            r = chinese_duration_to_hours(row['停车时长']) 

            # print(s_hours,row['出场时间'],str(row['入场时间']))

            if len(s_hours) > 1:
                # need to split it

                first = s_hours[0]

                sec = s_hours[1]

                qt = datetime.strptime(str(row['入场时间']),FM_YMDT)

                _last_day_of_month = last_day_of_month(qt)

                qe = datetime.strftime(_last_day_of_month,FM_DAY_END)

                leave_time_bk = row['出场时间']
                row['出场时间'] = qe
                q1 = row.to_list()
                q1.append(first['h'])

                qt2 = datetime.strptime(str(sec['fd'])+ ' 00:00:00',FM_YMDT).replace(day=1).strftime(FM_YMDT)

                row['出场时间'] = leave_time_bk

                row['入场时间'] = qt2

                q2 = row.to_list()
                q2.append(sec['h'])
                
                new_df = pd.DataFrame([q1,q2],columns=new_columns)

                none_df = pd.concat([none_df, new_df], ignore_index=True)
            else:
            
                q  = row.to_list()
                
                q.append(r)

                new_df = pd.DataFrame([q],columns=new_columns)

                none_df = pd.concat([none_df, new_df], ignore_index=True)
        
        none_df.to_sql(
        name=TABLE_NAME,
        con=engine,
        if_exists='append',
        index=False,
        chunksize=10000,
        dtype={
                'id': Integer(),   
                '车牌号码':Text(),
                '车型':Text(),
                '车牌颜色':Text(),
                '套餐类型':Text(),
                '套餐名称':Text(),
                '车辆身份':Text(),	
                '记录类型':Text(),
                '车主姓名':Text(),
                '手机号码':Text(),
                '车位产权号':Text(),
                '停车时长':Text(),
                '入场时间':DateTime(),
                '入场通道':Text(),
                '入场方式':Text(),
                '入场处理过程':Text(),
                '入场操作来源':Text(),
                '出场时间':DateTime(),
                '出场通道':Text(),
                '出场方式':Text(),
                '出场处理方式':Text(),
                '出场操作来源':Text(),	
                '总应收金额(元)':Text(),	
                '总优惠金额(元)':Text(),
                '总免费金额(元)':Text(),
                '总实收金额(元)':Text(),
                '车场区域':Text(),
                '所属项目':Text(),
                '入场操作人员':Text(),
                '出场操作人员':Text(),
                '出场备注':Text() ,
                '停车时长(小时)':Float()
                # 'category': Text(length=50),  # limit length
        }
    )



def create_car_leave_logs():

    engine = init_engine()
    metadata = MetaData()   
    
    table = get_car_leave_logs_table(metadata=metadata)

    metadata.create_all(engine)
    return table



