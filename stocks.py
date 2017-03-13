#!/usr/bin/env python
import csv
import datetime
from pathlib import Path
from yahoo_finance import Share


def get_new_stops(symbol, current_stop, spread, start_date):
    share = Share(symbol)
    newdate = (datetime.datetime.strptime(start_date,"%Y-%M-%d") + datetime.timedelta(days=1)).strftime("%Y-%M-%d")
    prices = share.get_historical(start_date, today)
    days_high=max([float(y['High']) for y in prices])
    days_low=min([float(y['Low']) for y in prices])

    if days_low < current_stop:
        print "%s - stop activated!" % symbol
        print days_low
    elif (days_high - spread) > current_stop:
        print "%s - new stop: %s" % (symbol, days_high - spread)


if __name__ == '__main__':
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    data_path = Path('stocks.csv')

    with data_path.open() as data_file:
        data_reader = csv.DictReader(data_file)
        for row in data_reader:
            get_new_stops(row['symbol'],
                          float(row['current_stop']),
                          float(row['spread']),
                          row['start_date'])
