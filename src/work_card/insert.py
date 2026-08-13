import argparse
import pandas as pd
import db


def main():
    parser = argparse.ArgumentParser(description="Import card and log Excel files")
    parser.add_argument('-c', '--cards', dest='card_excel', help='path to cards excel file', default=None)
    parser.add_argument('-l', '--logs', dest='logs_excel', help='path to logs excel file', default=None)
    args = parser.parse_args()


    card_excel = args.card_excel
    logs_excel = args.logs_excel

    if card_excel:
        df = pd.read_excel(card_excel)

        db.import_car_cards(df)

    if logs_excel:

        df = pd.read_excel(logs_excel)
        
        db.import_logs(df)

    db.update_card_parking_time()


if __name__ == "__main__":
    main()
