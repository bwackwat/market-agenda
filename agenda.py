#!/bin/python

from yahoo_finance import Share
import pycurl, json

import datetime
import time

def log(string):
    with open("agenda.log", "a") as file:
        file.write(string + "\n")
    print string

def notify(action, ticker, price):
    notifier = pycurl.Curl()
    notifier.setopt(pycurl.URL, "http://api.instapush.im/v1/post")
    notifier.setopt(pycurl.HTTPHEADER, [
        "x-instapush-appid: ",
        "x-instapush-appsecret: ",
        "Content-Type: application/json"
    ])
    json_fields = {}
    json_fields["event"] = "trade_suggestion"
    json_fields["trackers"] = {}
    json_fields["trackers"]["action"] = action
    json_fields["trackers"]["ticker"] = ticker
    json_fields["trackers"]["price"] = price
    notifier.setopt(pycurl.POSTFIELDS, json.dumps(json_fields))
    notifier.setopt(pycurl.VERBOSE, True)
    notifier.perform()
    notifier.close()

class Stock(object):
    def __init__(self, ticker, buying, low, high, automatic = False):
        self.ticker = ticker
        self.data = Share(ticker)
        self.buying = buying
        self.low = low
        self.high = high
        self.automatic = automatic

portfolio = [
    Stock("AAPL", False, 90, 100)
]

while True:
    now = datetime.datetime.now()
    if now.weekday() > 4:
        till_next_check = 24.0 + (9.6 - now.hour)
        log("It is the weekend (" + str(now) + "). Waiting " + str(till_next_check) + " hours.")
        time.sleep(till_next_check * 60 * 60)
    elif now.hour < 9.5:
        till_next_check = 9.6 - now.hour
        log("It is before 9:30AM (" + str(now) + "). Waiting " + str(till_next_check) + " hours.")
        time.sleep(till_next_check * 60 * 60)
    elif now.hour > 16:
        till_next_check = 24.0 + (9.6 - now.hour)
        log("It is after 4PM (" + str(now) + "). Waiting " + str(till_next_check) + " hours.")
        time.sleep(till_next_check * 60 * 60)

    log("Iterating portforio... (" + str(now) + ")")
    for stock in portfolio:
        stock.data.refresh()
        stock.price = float(stock.data.get_price())

        log(stock.ticker + " " + str(stock.price) + "(" + str(stock.data.get_trade_datetime()) + ")")

        if stock.buying and stock.price <= stock.low:
            log("Buy " + stock.ticker + " at " + str(stock.price) + "!")
            notify("Buy", stock.ticker, str(stock.price))
        elif not stock.buying and stock.price >= stock.high:
            log("Sell " + stock.ticker + " at " + str(stock.price) + "!")
            notify("Sell", stock.ticker, str(stock.price))

    time.sleep(10 * 60)