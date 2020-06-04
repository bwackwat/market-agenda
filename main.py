#!/usr/local/bin/python3
import os, sys, json

from yahoo_fin.stock_info import get_data, get_live_price

makey = os.environ.get("makey")


def index(request):
    key = None
    stock = None
    if request.args and "key" in request.args:
        key = request.args["key"]
    else:
        return 400

    if key != makey:
        return 403

    if request.args and "stock" in request.args:
        stock = request.args["stock"]
    else:
        return 400

    stocks = stock.split(",")
    response = {}
    for ticker in stocks:
        response[ticker] = get_live_price(ticker)

    return "<pre>" + json.dumps(response, indent=4) + "</pre>"


class Request():
    def __init__(self, args):
        self.args = args


if __name__ == "__main__":
    makey = sys.argv[1]
    print(json.dumps(index(Request({
        "key": sys.argv[1],
        "stock": sys.argv[2]
    }))))
