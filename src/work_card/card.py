import re
from datetime import datetime
import pandas as pd
import os
import date
from pathlib import Path



def get_project_root():
    """获取项目根目录"""
    # 当前文件路径
    current_file = Path(__file__).resolve()

    # 获取祖父目录（上两级）
    grandparent_dir = current_file.parent.parent.parent

    return grandparent_dir

def get_expired():
    
    path = get_project_root()  # 获取项目根目录

    pattern = r".*超时转.*\.xlsx$"  # Match all files ending with ".txt"

    today = datetime.today()
    
    expired = []
    for filename in os.listdir(path):

        if re.search(pattern, filename):
            sp = filename.split('#')
            
            _date = datetime.strptime(sp[0],date.YMD)

            if (today - _date).days > 0:

                df = pd.read_excel(f'{path}/{filename}')
                df = df[df['超时小时'] > 0]
                
                r = df['车牌号码'].to_list()

                expired += r
                
    
    return expired
