import argparse
import pandas as pd
import db



def main():
    parser = argparse.ArgumentParser(description="Import card and log Excel files")
    parser.add_argument('-c', '--cards', dest='card_excel', help='path to cards excel file', default=None)
    parser.add_argument('-l', '--logs', dest='logs_excel', help='path to logs excel file', default=None)
    parser.add_argument('-p', '--port', dest='db_port', help='path to logs excel file', default=None)
    parser.add_argument('-u', '--user', dest='db_user', help='path to logs excel file', default=None)
    parser.add_argument('-a', '--address', dest='address', help='path to logs excel file', default=None)
    parser.add_argument('-P', '--password', dest='password', help='path to logs excel file', default=None)
    parser.add_argument('-N', '--db-name', dest='db_name', help='path to logs excel file', default=None)
    
    args = parser.parse_args()


    card_excel = args.card_excel
    logs_excel = args.logs_excel
    user = args.db_user
    password = args.password
    address = args.address
    port = args.db_port
    db_name = args.db_name
    if not (card_excel or logs_excel):
        print("Please provide at least one of the Excel files to import.")
        return
    if not (user and password and address and port and db_name):
        print("Please provide all database connection parameters.")
        return
    

    conf = db.DbConf(user=user,password=password,address=address,port=port,db_name=db_name)

    engine = db.init_engine(conf)
    if card_excel:
        df = pd.read_excel(card_excel)

        db.import_car_cards(df,engine)

    if logs_excel:

        df = pd.read_excel(logs_excel)
        
        db.import_logs(df,engine)

    db.update_card_parking_time(engine=engine)


if __name__ == "__main__":
    main()
