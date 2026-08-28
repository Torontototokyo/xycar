import pandas as pd


def _2025():
    file1 = '2025-1-6.xlsx'
    file2 = '2025-7-12.xlsx'

    df1 = pd.read_excel(file1)

    df1 = df1[
        df1['续费有效期'].str.contains('2025', na=False) &
        df1['续费有效期'].str.contains('2026', na=False)
    ]

    df1 = df1[df1['所属项目'] !='花卉世界停车场']
    
    df1 = df1[df1['实收金额(元)'] > 1000]

    df2 = pd.read_excel(file2)
    
    df2 = df2[
        df2['续费有效期'].str.contains('2025', na=False) &
        df2['续费有效期'].str.contains('2026', na=False)
    ]

    df2 = df2[df2['所属项目'] !='花卉世界停车场']
    
    df2 = df2[df2['实收金额(元)'] > 1000]

    df = pd.concat([df1, df2], ignore_index=True)

    df.to_excel('2025年跨年缴费记录.xlsx')
    
def _2024():
    file = '月卡缴费记录_20260828161630822.xlsx';

    df = pd.read_excel(file)

    df = df[
        df['续费有效期'].str.contains('2024', na=False) &
        df['续费有效期'].str.contains('2025', na=False)
    ]


    df = df[df['所属项目'] !='花卉世界停车场']

    df = df[df['实收金额(元)'] > 1000]
    df.to_excel('2024年跨年缴费记录.xlsx')

_2025()