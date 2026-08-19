from datetime import datetime
from sqlalchemy import create_engine,MetaData,select,Column,Table,DateTime as DT
from sqlalchemy.types import Integer, Float, Text, DateTime,DECIMAL
from sqlalchemy.orm import Session,DeclarativeBase,mapped_column,relationship,Mapped
from sqlalchemy import insert,update,String
from sqlalchemy.sql import func
from sqlalchemy.exc import MultipleResultsFound
import work_card.date as date
from dateutil.relativedelta import relativedelta
import pandas as pd
import work_card.card as card
import numpy as np
import work_card.utils as utils


class Base(DeclarativeBase):
    pass

class CarParkingOT(Base):
    __tablename__ = 'car_parking_ot'
    id: Mapped[int] = mapped_column(primary_key=True)
    car_no:Mapped[str] = mapped_column(String(100))
    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),           # or False
        default=func.now(),                # for INSERT
        onupdate=func.now(),               # ← automatically updates on every UPDATE
        nullable=False
    )
    updated_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),           # or False
        default=func.now(),                # for INSERT
        onupdate=func.now(),               # ← automatically updates on every UPDATE
        nullable=False
    )
    hours:Mapped[float] = mapped_column(Float(2))
    removed_at:Mapped[str] = mapped_column(String(30))
    arose_at:Mapped[str] = mapped_column(String(30))
    def __repr__(self) -> str:
        return f"CarParkingOT(id={self.id!r}, hours={self.hours!r}, card_no={self.car_no!r},start_dt={self.start_dt!r},end_dt={self.end_dt!r})"
class Summary(Base):
    __tablename__ = 'get_car_leave_log_summery_by_month'
    id: Mapped[int] = mapped_column(primary_key=True)
    hours:Mapped[float] = mapped_column(Float(2))
    car_no:Mapped[str] = mapped_column(String(30))
    start_dt:Mapped[str] = mapped_column(String(30))
    updated_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),           # or False
        default=func.now(),                # for INSERT
        onupdate=func.now(),               # ← automatically updates on every UPDATE
        nullable=False
    )
    def __repr__(self) -> str:
        return f"Summary(id={self.id!r}, hours={self.hours!r}, card_no={self.car_no!r},start_dt={self.start_dt!r})"

class Logs(Base):
    __tablename__ = "car_leave_logs"
    
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    车牌号码: Mapped[str] = mapped_column(String(100), unique=True)
    车型: Mapped[str] = mapped_column(String(20),nullable=True)
    车牌颜色: Mapped[str] = mapped_column(String(200),nullable=True)
    套餐类型: Mapped[str] = mapped_column(String(200),nullable=True)
    套餐名称: Mapped[str] = mapped_column(String(200),nullable=True)
    车辆身份: Mapped[str] = mapped_column(String(200),nullable=True)
    记录类型: Mapped[str] = mapped_column(String(20),nullable=True)
    车主姓名: Mapped[str] = mapped_column(String(20),nullable=True)
    手机号码: Mapped[str] = mapped_column(String(200),nullable=True)
    车位产权号: Mapped[str] = mapped_column(
                String(20),
                nullable=False)
    停车时长1: Mapped[str] = mapped_column('停车时长',String(100),nullable=False)
    
    入场时间: Mapped[str] = mapped_column(String(20), default='正常')
    入场通道: Mapped[str] = mapped_column(String(200),nullable=True)
    入场方式: Mapped[str] = mapped_column(String(200),nullable=True)
    入场处理过程: Mapped[str] = mapped_column(String(50),nullable=True)
    入场操作来源: Mapped[str] = mapped_column(String(50),nullable=True)
    出场时间: Mapped[str] = mapped_column(String(100),nullable=True)
    出场通道: Mapped[str] = mapped_column(String(100),nullable=True)
    出场方式: Mapped[str] = mapped_column(String(50),nullable=True)
    出场处理方式: Mapped[str] = mapped_column(String(50),nullable=True)
    出场操作来源: Mapped[str] = mapped_column(String(50),nullable=True)
    总应收金额: Mapped[float] = mapped_column( "总应收金额(元)",DECIMAL(2,20),nullable=True)
    总优惠金额: Mapped[float] = mapped_column("总优惠金额(元)",DECIMAL(2,20),nullable=True)
    总免费金额: Mapped[float] = mapped_column('总免费金额(元)',DECIMAL(2,20),nullable=True)
    总实收金额: Mapped[float] = mapped_column('总实收金额(元)',DECIMAL(2,20),nullable=True)
    车场区域: Mapped[str] = mapped_column(String(100),nullable=True)
    所属项目: Mapped[str] = mapped_column(String(100),nullable=True)
    入场操作人员: Mapped[str] = mapped_column(String(50),nullable=True)
    出场操作人员: Mapped[str] = mapped_column(String(50),nullable=True)
    出场备注: Mapped[str] = mapped_column(String(200),nullable=True)
    停车时长A小时Z: Mapped[float] = mapped_column('停车时长A小时Z',Float(),nullable=True)
    

class Card(Base):          # Example for your previous Chinese column names
    __tablename__ = "car_cards"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    人员姓名: Mapped[str] = mapped_column(String(200))
    车牌号码: Mapped[str] = mapped_column(String(100), unique=True)
    卡号码: Mapped[str] = mapped_column(String(20),nullable=True)
    手机号码: Mapped[str] = mapped_column(String(200),nullable=True)
    套餐名称: Mapped[str] = mapped_column(String(200),nullable=True)
    所属物业: Mapped[str] = mapped_column(String(200),nullable=True)
    适用车场区域: Mapped[str] = mapped_column(String(200),nullable=True)
    车位数: Mapped[str] = mapped_column(String(20),nullable=True)
    车位号: Mapped[str] = mapped_column(String(20),nullable=True)
    物业单元: Mapped[str] = mapped_column(String(200),nullable=True)
    开始期限: Mapped[str] = mapped_column(
                String(20),
                nullable=False)
    截止期限: Mapped[str] = mapped_column(
                 String(20),
                nullable=False)
   
    卡状态: Mapped[str] = mapped_column(String(20), default='正常')
    开卡备注: Mapped[str] = mapped_column(String(200),nullable=True)
    操作备注: Mapped[str] = mapped_column(String(200),nullable=True)
    总免费停车时长: Mapped[int] = mapped_column(Integer,nullable=True)
    实际停车时长: Mapped[float] = mapped_column(Float,nullable=True)
    超时小时: Mapped[float] = mapped_column(Float,nullable=True)

def init_engine():
    DB_USER = 'root'
    DB_PASSWORD = 'root'
    DB_HOST = 'localhost'      # or IP address
    DB_PORT = 3306
    DB_NAME = 'cars_db'
    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        pool_pre_ping=True,        # Helps with stale connections
        echo=False                 # Set True for debugging SQL
    )

    return engine




def init_card():

    metadata = MetaData()
    
    cards = pd.read_excel('车场免费卡报表.xlsx');

    cards = cards[cards['套餐名称'] == '工作卡']

    cards = cards[cards['卡状态'].isin(['临期','正常'])]

    ##如果车位数>1 ,需要将卡拆分为多张

    engine = init_engine()

    columns =['id']+cards.columns.to_list() + ['总免费停车时长','实际停车时长','超时小时']
   
    df = pd.DataFrame(cards,columns=columns)

    for index,row in df.iterrows():
        # row['总免费停车时长'] = get_free_hours_between(row['开始期限'],row['截止期限'])
        df.loc[index,'总免费停车时长'] = date.get_free_hours_between(row['开始期限'],row['截止期限'])

    df = df.replace({np.nan: None})


    with Session(engine) as session:
        for index,row in df.iterrows():
            # session.execute(insert(Card),df.values.tolist())
            session.execute(insert(Card),[row.to_dict()])
        session.commit()
    # df = pd.concat([df,])
    # df.to_sql(
    #     name=TABLE_NAME,
    #     con=engine,
    #     if_exists='append',
    #     index=True,
    #     chunksize=10000,
    #     dtype={
    #             'id':Integer(),
    #             '人员姓名':Text(),	
    #             '车牌号码':Text(),	
    #             '卡号码':Text(),	
    #             '手机号码':Text(),	
    #             '套餐名称':Text(),	
    #             '所属物业':Text(),	
    #             '适用车场区域':Text(),	
    #             '车位数':Text(),	
    #             '车位号':Text(),	
    #             '物业单元':Text(),	
    #             '开始期限':Text(),	
    #             '截止期限':Text(),	
    #             '卡状态':Text(),	
    #             '开卡备注':Text(),
    #             '操作备注':Text(),
    #             '总免费停车时长':Integer(),
    #             '实际停车时长':Float(),
    #             '超时小时':Float()
    #     }
    # )





def get_car_leave_logs_table(metadata):
    table = Table(
        'car_leave_logs',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('车牌号码', Text),
        Column('车型', Text),
        Column('车牌颜色', Text),
        Column('套餐类型', Text),
        Column('套餐名称', Text),
        Column('车辆身份', Text),
        Column('记录类型', Text),
        Column('车主姓名', Text),
        Column('手机号码', Text),
        Column('车位产权号', Text),
        Column('停车时长',Text),
        Column('入场时间',DT),
        Column('入场通道',Text),
        Column('入场方式',Text),
        Column('入场处理过程',Text),
        Column('入场操作来源',Text),
        Column('出场时间',DT),
        Column('出场通道',Text),
        Column('出场方式',Text),
        Column('出场处理方式',Text),
        Column('出场操作来源',Text),
        Column('总应收金额(元)',Text),
        Column('总优惠金额(元)',Text),
        Column('总免费金额(元)',Text),
        Column('总实收金额(元)',Text),
        Column('车场区域',Text),
        Column('所属项目',Text),
        Column('入场操作人员',Text),
        Column('出场操作人员',Text),
        Column('出场备注',Text),
        Column('停车时长(小时)',Float),
    )

    return table


def get_car_leave_log_summery_by_month_table(metadata):
   
    engine = init_engine()
    # Create table if it doesn't exist
    metadata = MetaData()
    tb = Table(
        'car_leave_log_summery_by_month', metadata,
        Column('id', Integer, primary_key=True),
        Column('车牌号码', Text),
        Column('停车时长(小时)', Float),
        Column('开始日期', Text),


    )

    metadata.create_all(engine)
    return tb

def update_user_20(db: Session, id: int, **kwargs):

    
    stmt = update(Summary)\
           .where(Summary.id == id)\
           .values(**kwargs,updated_at = func.now() )
    
    result = db.execute(stmt)
    db.commit()
    return result.rowcount  # number of rows updated

def add_or_insert_car_leave_log_summery_by_month(car_no:str,hours:float,start_dt:str):
    
    engine = init_engine()

    with Session(engine) as session:
        
        # car_leave_log_summery_by_month = get_car_leave_log_summery_by_month_table(metadata)

        r = session.query(Summary).filter(Summary.car_no == car_no).filter(Summary.start_dt == start_dt).first()


        if r is None:
            
            session.execute(insert(Summary),[
                {'car_no':car_no,'start_dt':start_dt,'hours':hours}
            ])

            session.commit()
        else:
            
            
            count = update_user_20(session,r.id,hours = r.hours+ hours)



def update_or_insert_car_leave_log_summery_by_month(car_no:str,start_dt):
    
    engine = init_engine()

    with Session(engine) as session:
        
        # car_leave_log_summery_by_month = get_car_leave_log_summery_by_month_table(metadata)

        r = session.query(Summary).filter(Summary.car_no == car_no).filter(Summary.start_dt == start_dt).first()

        if type(start_dt) == str:
            start_dt = datetime.strptime(start_dt, date.YMD).strftime(date.YMD)
            # print(f'start_dt:{start_dt},{type(start_dt)}')
        else:
            start_dt = start_dt.strftime(date.YMD)
            # print(f'start_dt:{start_dt},{type(start_dt)}')
        

        end_dt = date.last_day_of_month(datetime.strptime(start_dt, date.YMD)).strftime(date.YMD)
        # print(f'car_no:{car_no},start_dt:{start_dt},{type(start_dt)},end_dt:{end_dt}')
        hours = sum_logs(car_no,start_dt,end_dt)

        if r is None:
            
            session.execute(insert(Summary),[
                {'car_no':car_no,'start_dt':start_dt,'hours':hours}
            ])

            session.commit()
        else:
            
            
            count = update_user_20(session,r.id,hours =  hours)
            session.commit()


def summary_hour(car_no,date)->float:
    engine = init_engine()
    car_nos = []
    if "," in car_no:
        car_nos = car_no.split(",")
    else:
        car_nos = [car_no]

    with Session(engine) as session:
         h = session.scalar(select(Summary.hours).where(Summary.start_dt == date)\
                         .where(Summary.car_no.in_(car_nos)))
         
         
    return h or 0


def sum_logs(car_no,start_dt,end_dt)->float:

    car_nos = []
    if "," in car_no:
        car_nos = car_no.split(",")
    else:
        car_nos = [car_no]

    if start_dt == end_dt:

        end_dt = datetime.strptime(end_dt,date.YMD) + relativedelta(days=1)
    
        end_dt = end_dt.strftime(date.YMD)

    # print(end_dt)
    # exit()
    
    end_dt = datetime.strptime(end_dt,date.YMD) + relativedelta(days=1)
    
    end_dt = end_dt.date()
   
    engine = init_engine()

    with Session(engine) as session:

        stmt = select(func.sum(Logs.停车时长A小时Z))\
        .where(Logs.入场时间 > start_dt)\
        .where(Logs.出场时间 < end_dt)\
        .where(Logs.车牌号码.in_(car_nos))

        r = session.scalar(stmt)

        # print(stmt,f'start_dt:{start_dt},end_dt:{end_dt},r:{r}')
 

    return r or 0
    

def update_card_parking_time():

    
    # table = get_cards_table(metadata=MetaData())
    engine = init_engine()

    with Session(engine) as session:

        expired = card.get_expired()
        stmt = select(Card.车牌号码,Card.开始期限,Card.截止期限,Card.总免费停车时长)\
        .where(Card.卡状态.in_(['正常','临期']))\
        .where(Card.车牌号码.notin_(expired))
        result = session.execute(stmt).all()
        
        for r in result:

            car_no = r[0]
            start_dt = r[1]
            end_dt = r[2]
            # free_h = r[3]
            
            free_h = date.get_free_hours_between(start_dt,end_dt)

            hours = get_parked_hours_between(car_no,start_dt,end_dt)
            
            diff = datetime.today() - datetime.strptime(end_dt,date.YMD)

            if(diff.days > 0):
                stmt = update(Card).where(Card.车牌号码 == car_no).values({
                    '卡状态':'过期'
                })
                session.execute(stmt)
            ot = 0
            if hours > free_h:
                ot = hours - free_h

            stmt = update(Card).where(Card.车牌号码 == car_no)\
            .values({
                '实际停车时长':hours,
                '超时小时':ot,
                '总免费停车时长':free_h
            })
            session.execute(stmt)
        session.commit()

        stmt = select(Card).where(Card.超时小时 > 0)\
        .where(Card.车牌号码.notin_(expired))
        df = pd.read_sql_query(stmt,con=engine)

        if len(df) > 0:
            df.to_excel(f'{card.get_project_root()}/{datetime.now().strftime("%Y-%m-%d")}#超时转临停车辆.xlsx',index=False)
        
    
    

def get_parked_hours_between(car_no,start_dt,end_dt):
    
    first_date_last_6_month = date.get_first_day_last_6_months(start_dt)
    if (datetime.strptime(first_date_last_6_month,date.YMD) - datetime.strptime(start_dt,date.YMD)).days > 0:
            start_dt = first_date_last_6_month

    
    # print(start_dt)
    #[['2026-09-02', '2026-09-30'], '2026-10-01', ['2026-11-01', '2026-11-15']]
    r = date.seperate_date_into_months(start_dt,end_dt)

    hours = 0;

    for i in r:

        if type(i) == list:

            hours += sum_logs(car_no,i[0],i[1])

        else:
           
            hours += summary_hour(car_no,i)
    # print(car_no,start_dt,hours)
    return hours


def import_car_cards(df:pd.DataFrame):

    # table = get_cards_table(metadata=MetaData())
    engine = init_engine()
    df = df[df['卡状态'].isin(['正常','过期'])]
    df = df[df['套餐名称'] == '工作卡']

    df = df.replace({np.nan: None})
    with Session(engine) as session:

        for _, row in df.iterrows():
            car_no = row['车牌号码']
            stmt = select(Card.id).where(Card.车牌号码 == car_no)

            existing_id = session.execute(stmt).scalar_one_or_none()
           
            values = row.to_dict()

            start_dt = row['开始期限']
            end_dt = row['截止期限']
            hours = date.get_free_hours_between(start_dt,end_dt)
                
            values['总免费停车时长'] = hours
            if existing_id is None:
                session.execute(insert(Card).values(**values))
            else:
                session.execute(update(Card).where(Card.id == existing_id).values(**values))


        
        session.commit()


def import_logs(df:pd.DataFrame):

    engine = init_engine()


    df = df.replace({np.nan: None})

    with Session(engine) as session:

        try:

            for _, row in df.iterrows():

                
                car_no = row['车牌号码']
                enter_time = row['入场时间']
                leave_time = row['出场时间']
                parked_time = row['停车时长']

                stmt = select(Logs.id).where(Logs.车牌号码 == car_no)\
                .where(Logs.入场时间 == enter_time)\
                .where(Logs.出场时间 == leave_time)\
                .where(Logs.停车时长1 == parked_time)\


                existing_id = session.execute(stmt).scalar_one_or_none()
                
                values = dict(row)
                

                if existing_id is None:

                    s_hours = date.sub_hours(row['出场时间'],row['入场时间'])
                    
                    r = utils.chinese_duration_to_hours(row['停车时长']) 
        
                    # print(s_hours,row['出场时间'],str(row['入场时间']))
        
                    if len(s_hours) > 1:
                        # need to split it
        
                        first = s_hours[0]
        
                        sec = s_hours[1]
        
                        qt = datetime.strptime(str(row['入场时间']),date.FM_YMDT)
        
                        _last_day_of_month = date.last_day_of_month(qt)
        
                        qe = datetime.strftime(_last_day_of_month,date.FM_DAY_END)
        
                        leave_time_bk = row['出场时间']
                        row['出场时间'] = qe
                        q1 = row.to_dict()
                        # q1.append(first['h'])
                        q1['停车时长A小时Z']=first['h']
        
                        qt2 = datetime.strptime(str(sec['fd'])+ ' 00:00:00',date.FM_YMDT).replace(day=1).strftime(date.FM_YMDT)
        
                        row['出场时间'] = leave_time_bk
        
                        row['入场时间'] = qt2
        
                        q2 = row.to_dict()
                        q2['停车时长A小时Z'] = sec['h']
                        # q2.append(sec['h'])
                        
                        # new_df = pd.DataFrame([q1,q2],columns=new_columns)

                        # none_df = pd.concat([none_df, new_df], ignore_index=True)
                        session.execute(insert(Logs).values(**q1))
                        session.execute(insert(Logs).values(**q2))
                        session.commit()
                        q1_start_dt = datetime.strptime(str(q1['入场时间']),date.FM_YMDT).replace(day=1).strftime(date.YMD)
                        q2_start_dt = datetime.strptime(str(q2['入场时间']),date.FM_YMDT).replace(day=1).strftime(date.YMD)
                        update_or_insert_car_leave_log_summery_by_month(car_no,q1_start_dt)
                        update_or_insert_car_leave_log_summery_by_month(car_no,q2_start_dt)
                    else:


                        values['停车时长A小时Z'] = r
                        values['停车时长'] = row['停车时长']



                        session.execute(insert(Logs).values(**values))
                        session.commit()
                        start_dt = datetime.strptime(str(row['入场时间']),date.FM_YMDT).replace(day=1).strftime(date.YMD)
                        update_or_insert_car_leave_log_summery_by_month(car_no,start_dt)

        except Exception as e:
            print(f"Error occurred: {e}")
            session.rollback()
            raise
def update_summary_logs():
    pass


engine = init_engine()
Base.metadata.create_all(engine)





