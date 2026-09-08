from datetime import datetime
from sqlalchemy import create_engine,MetaData,select,Column,Table,DateTime as DT
from sqlalchemy.types import Integer, Float, Text, DateTime,DECIMAL
from sqlalchemy.orm import Session,DeclarativeBase,mapped_column,relationship,Mapped
from sqlalchemy import insert,update,String,Engine
from sqlalchemy.sql import func
from sqlalchemy.exc import MultipleResultsFound
import work_card.date as date
from dateutil.relativedelta import relativedelta
import pandas as pd
# import work_card.card as card
import numpy as np
import work_card.utils as utils
import logging
import pymysql
from pymysql import Error

class DbConf:


    def __init__(self,user:str,password:str,address:str,port:int,db_name:str) -> None:
        
        self.user = user
        self.password = password
        self.address = address
        self.port = port
        self.db_name = db_name
    


def test_connection_with_context(conf:DbConf):
    """使用 with 语句测试连接（自动管理资源）"""
    try:
        with pymysql.connect(
            host=conf.address,
            user=conf.user,
            password=conf.password,
            database=conf.db_name,
            charset='utf8mb4',
            port=conf.port,
            autocommit=True  # 自动提交
        ) as connection:
            print("✅ 连接成功")
            
            # 执行简单查询测试
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"MySQL 版本: {version[0]}")
                
                cursor.execute("SELECT DATABASE()")
                db_name = cursor.fetchone()
                print(f"当前数据库: {db_name[0]}")
                
            return True
            
    except Error as e:
        print(f"❌ 数据库错误: {e}")
        return False

# 执行
    
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# logging.getLogger('sqlalchemy.orm').setLevel(logging.INFO)
def init_engine(db_conf: DbConf)-> Engine:
    DB_USER = db_conf.user
    DB_PASSWORD = db_conf.password
    DB_HOST = db_conf.address
    DB_PORT = db_conf.port
    DB_NAME = db_conf.db_name
    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        pool_pre_ping=True,        # Helps with stale connections
        echo=False,                # Set True for debugging SQL
        logging_name=None
    )

    return engine
    DB_USER = str_user
    DB_PASSWORD = str_password
    DB_HOST = str_address
    DB_PORT = int_port
    DB_NAME = str_db_name
    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        pool_pre_ping=True,        # Helps with stale connections
        echo=False,                # Set True for debugging SQL
        logging_name=None
    )

    return engine

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
        return f"CarParkingOT(id={self.id!r}, hours={self.hours!r}, card_no={self.car_no!r},removed_at={self.removed_at!r},arose_at={self.arose_at!r})"
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
    deleted_at:Mapped[str] = mapped_column(String(100),nullable=True)
    

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
    created_at:Mapped[datetime] = mapped_column(String(200),nullable=True)
    updated_at:Mapped[datetime] = mapped_column(String(200),nullable=True)




def init_engine_sql():
    DB_USER = 'root'
    DB_PASSWORD = 'root'
    DB_HOST = 'localhost'      # or IP address
    DB_PORT = 3306
    DB_NAME = 'sys'
    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        pool_pre_ping=True,        # Helps with stale connections
        echo=False                 # Set True for debugging SQL
    )

    return engine







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


def update_user_20(db: Session, id: int, **kwargs):

    
    stmt = update(Summary)\
           .where(Summary.id == id)\
           .values(**kwargs,updated_at = func.now() )
    
    result = db.execute(stmt)
    db.commit()
    return result.rowcount  # number of rows updated



def update_or_insert_car_leave_log_summery_by_month(car_no:str,start_dt,session:Session):
        
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
    hours = sum_logs(car_no,start_dt,end_dt,session)
    if car_no == '湘-MKA639':
        print(hours,start_dt,end_dt)
    
    if r is None:
        
        session.execute(insert(Summary),[
            {'car_no':car_no,'start_dt':start_dt,'hours':hours}
        ])

    else:
        
        
        count = update_user_20(session,r.id,hours =  hours)
         


def summary_hour(car_no,date,session:Session)->float:
    car_nos = []
    if "," in car_no:
        car_nos = car_no.split(",")
    else:
        car_nos = [car_no]

    h = session.scalar(select(Summary.hours).where(Summary.start_dt == date)\
                    .where(Summary.car_no.in_(car_nos)))
         
         
    return h or 0


def sum_logs(car_no,start_dt,end_dt,session:Session)->float:

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
   



    stmt = select(func.sum(Logs.停车时长A小时Z))\
    .where(Logs.入场时间 >= start_dt)\
    .where(Logs.出场时间 < end_dt)\
    .where(Logs.车牌号码.in_(car_nos))\
    .where(Logs.deleted_at == None)

    r = session.scalar(stmt)

    # print(stmt,f'start_dt:{start_dt},end_dt:{end_dt},r:{r}')
 

    return r or 0

def ot_record(car_no:str,session:Session)->float:



    stmt = select(func.sum(CarParkingOT.hours))\
    .where(CarParkingOT.car_no == car_no)\
    .where(CarParkingOT.removed_at == None)

    sum_hours = session.scalar(stmt)
    return sum_hours or 0

def expire_card(session:Session,car_no:str,hours:float,overtime:float,free_h:float,car_state:str='过期')->int:

    stmt = update(Card).where(Card.车牌号码 == car_no)\
            .where(Card.卡状态.in_(['正常','临期']))\
            .with_hint('FORCE INDEX (idx_卡状态_车牌号码)',Card)\
            .values({
                '实际停车时长':hours,
                '超时小时':overtime,
                '总免费停车时长':free_h,
                '卡状态':car_state,
                'updated_at':datetime.now().strftime(date.FM_YMDT)
            })
    update_card_res = session.execute(stmt) 
    return update_card_res.rowcount
def add_or_update_ot_record(session:Session,car_no:str,hours:float):

    now = datetime.now().strftime(date.FM_YMDT)
    today = datetime.now().strftime(date.YMD)

    ## if today ot_record exist
    stmt = select(CarParkingOT).where(CarParkingOT.car_no == car_no)\
        .where(CarParkingOT.removed_at == None)\
        .where(CarParkingOT.arose_at == today)

    first = session.execute(stmt).scalar_one_or_none()
    
    if first:
        update(CarParkingOT).where(CarParkingOT.id == first.id)\
        .values({hours:hours})
    else:
        stmt = insert(CarParkingOT).values(
            car_no=car_no,
            hours=hours,
            arose_at=today,
            created_at=now,
            updated_at=now
        )
        session.execute(stmt)

   

def remove_ot_record(car_no:str,session:Session)->int:

    stmt = update(CarParkingOT).where(CarParkingOT.car_no == car_no)\
                    .where(CarParkingOT.removed_at == None)\
                    .values({
                        'removed_at':datetime.now().strftime(date.YMD)
                    })

    res = session.execute(stmt)

    return res.rowcount

def update_card_parking_time(session:Session,start_dt,end_dt,car_no):
    free_h = date.get_free_hours_between(start_dt,end_dt)

   
    hours = get_parked_hours_between(car_no,start_dt,end_dt,session)

    diff = datetime.today() - datetime.strptime(end_dt,date.YMD)


    if(diff.days > 0):
        stmt = update(Card).where(Card.车牌号码 == car_no).values({
            '卡状态':'过期'
        })
        session.execute(stmt)
    ## plus the existing ot_record hours
    sum_ot_record_hours = ot_record(car_no,session=session)
    hours = hours + sum_ot_record_hours

    ot = 0

    
    if hours > free_h:
        ot = hours - free_h
    
    if ot > 0 :
        update_card_res_rowcount = expire_card(session=session,car_no=car_no,hours=hours,overtime=ot,free_h=free_h)
        if  update_card_res_rowcount > 0:
            add_or_update_ot_record(session=session,car_no=car_no,hours=ot)
        if update_card_res_rowcount > 0 and sum_ot_record_hours > 0:
            
            ## update the existing record in CarParkingOT to mark it as removed
            remove_res_rowcount = remove_ot_record(car_no=car_no,session=session)
        

            if  remove_res_rowcount > 0:
                print(f'车牌号:{car_no}，超时记录已移除')
            ## add new record

    else:
        update_card_res_rowcount = expire_card(session=session,car_no=car_no,hours=hours,overtime=0,free_h=free_h,car_state='正常')


def update_card_parking_time_db_by_result(engine:Engine,rows):

    with Session(engine) as session:
        try:

            for r in rows:

                car_no = r[0]
                start_dt = r[1]
                end_dt = r[2]
                update_card_parking_time(session=session,start_dt=start_dt,end_dt=end_dt,car_no=car_no)
                
            session.commit()

            stmt = select(Card).where(Card.超时小时 > 0)

            df = pd.read_sql_query(stmt,con=engine)

            if len(df) > 0:
                df.to_excel(f'{utils.get_project_root()}/{datetime.now().strftime("%Y-%m-%d")}#超时转临停车辆.xlsx',index=False)
            
        except Exception as e:
            print(e)

            session.rollback()



def update_card_parking_time_db(engine:Engine): 

    
    # table = get_cards_table(metadata=MetaData())
    today = datetime.now().strftime("%Y-%m-%d")

    with Session(engine) as session:
        try:


            stmt = select(Card.车牌号码,Card.开始期限,Card.截止期限,Card.总免费停车时长)\
            .where(Card.卡状态.in_(['正常','临期']))
            result = session.execute(stmt).all()

            
            for r in result:

                car_no = r[0]
                start_dt = r[1]
                end_dt = r[2]
                update_card_parking_time(session=session,start_dt=start_dt,end_dt=end_dt,car_no=car_no)
               
            session.commit()

            aroses_stmt = select(CarParkingOT.car_no)\
            .where(CarParkingOT.arose_at == today)
            aroses = session.execute(aroses_stmt).scalars().all()
            


            stmt = select(Card).where(Card.超时小时 > 0)\
            .where(Card.车牌号码.in_(aroses))
            df = pd.read_sql_query(stmt,con=engine)
            
            if len(df) > 0:
                fname = f'{utils.get_project_root()}/{today}#超时转临停车辆.xlsx'
                df.to_excel(fname,index=False)
                return fname
            else:
                return None
            
        except Exception as e:
            print(e)

            session.rollback()
    

def get_parked_hours_between(car_no,start_dt,end_dt,session:Session)->float:
    
    first_date_last_6_month = date.get_first_day_last_6_months(start_dt)
    if (datetime.strptime(first_date_last_6_month,date.YMD) - datetime.strptime(start_dt,date.YMD)).days > 0:
            start_dt = first_date_last_6_month

    
    # print(start_dt)
    #[['2026-09-02', '2026-09-30'], '2026-10-01', ['2026-11-01', '2026-11-15']]
    r = date.seperate_date_into_months(start_dt,end_dt)

    hours = 0;

    for i in r:

        if type(i) == list:

            hours += sum_logs(car_no,i[0],i[1],session)

        else:
           
            hours += summary_hour(car_no,i,session)
    if car_no == '湘-MKA639':
        print(car_no,start_dt,hours)
    return hours


def import_car_cards(df:pd.DataFrame,engine:Engine):

    # table = get_cards_table(metadata=MetaData())
    df = df[df['卡状态'].isin(['正常','过期'])]
    df = df[df['套餐名称'] == '工作卡']

    df = df.replace({np.nan: None})
    with Session(engine) as session:

        for _, row in df.iterrows():
            car_no = row['车牌号码']
            start_dt = row['开始期限']
            end_dt = row['截止期限']
            stmt = select(Card.id).where(Card.车牌号码 == car_no)\
            .where(Card.开始期限 == start_dt)\
            .where(Card.截止期限 == end_dt)

            existing_id = session.execute(stmt).scalar_one_or_none()
           
            values = row.to_dict()

           
            hours = date.get_free_hours_between(start_dt,end_dt)
                
            values['总免费停车时长'] = hours
            if existing_id is None:
                values['created_at'] = datetime.now()
                values['updated_at'] = datetime.now()
                session.execute(insert(Card).values(**values))
            else:
                values['updated_at'] = datetime.now()
                session.execute(update(Card).where(Card.id == existing_id).values(**values))


        
        session.commit()


def import_logs(df:pd.DataFrame,engine:Engine):

    df = df.replace({np.nan: None})

    with Session(engine) as session:

        try:

            for _, row in df.iterrows():

                
                car_no = row['车牌号码']
                enter_time = row['入场时间']
                leave_time = row['出场时间']
                parked_time = row['停车时长']
                if(car_no == '湘-MKA639'):
                    print(parked_time,leave_time,enter_time,car_no)
                

                stmt = select(Logs.id).where(Logs.车牌号码 == car_no)\
                .where(Logs.入场时间 == enter_time)\
                .where(Logs.停车时长1 == parked_time)\
                .where(Logs.deleted_at == None)


                existing_id = session.execute(stmt).scalars().first()
                
                values = dict(row)
                

                if existing_id is None:

                    s_hours = date.sub_hours2(row['出场时间'],row['入场时间'])
                    
                    r = utils.chinese_duration_to_hours(row['停车时长']) 
        

        
                    if len(s_hours) > 1:
                        # need to split it
        
                        for _,r in enumerate(s_hours):
                            q = row.to_dict()
                            q['停车时长A小时Z'] = r['h']
                            q['停车时长'] = row['停车时长']
                            q['入场时间'] = r['入场时间']
                            q['出场时间'] = r['出场时间']
                            session.execute(insert(Logs).values(**q))
                            q_start_dt = datetime.strptime(str(q['入场时间']),date.FM_YMDT)\
                                                        .replace(day=1).strftime(date.YMD)
                                                  
                            update_or_insert_car_leave_log_summery_by_month(car_no,q_start_dt,session=session)
                        session.commit()
                        
                        
                    else:

                        values['停车时长A小时Z'] = r
                        values['停车时长'] = row['停车时长']



                        session.execute(insert(Logs).values(**values))
                        session.commit()
                        start_dt = datetime.strptime(str(row['入场时间']),date.FM_YMDT).replace(day=1).strftime(date.YMD)
                        update_or_insert_car_leave_log_summery_by_month(car_no,start_dt,session=session)


        except Exception as e:
            print(f"Error occurred: {e}")
            session.rollback()
            raise



# engine = init_engine()
# Base.metadata.create_all(engine)





