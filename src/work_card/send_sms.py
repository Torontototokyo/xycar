from sms import Sample
import argparse
import pandas as pd
def main():
    parser = argparse.ArgumentParser(description="Import card and log Excel files")
    parser.add_argument('-f', '--file', dest='sends_sms_file', help='path to cards excel file', default=None)

    args = parser.parse_args()

    file = args.sends_sms_file
    if file is None:
        return 0

    df = pd.read_excel(file)

    for _,row in df.iterrows():
        car_no = row['车牌号码']
        phone_number = row['手机号码']
        hour = row['超时小时']
        # print(phone_number,car_no,hour)
        Sample.sms(car_no=car_no,hour=hour,phone_numer=phone_number)
if __name__ == "__main__":
    main()