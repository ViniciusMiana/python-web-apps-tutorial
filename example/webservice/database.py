#!/usr/bin/python

import sqlite3


class MyServiceDatabase():
    """ Database handler class """

    def __init__(self, db="database.db"):
        """Open database"""
        self.conn = sqlite3.connect(db)

        #Create tables
        self.conn.execute("CREATE TABLE IF NOT EXISTS portfolio (symbol TEXT UNIQUE, last_price TEXT DEFAULT '0')")
        self.conn.execute("CREATE TABLE IF NOT EXISTS settings (name TEXT UNIQUE, value TEXT)")
        self.conn.commit()

    def add_stock(self, symbol):
        """Add a stock to the portfolio"""
        self.conn.execute("INSERT INTO portfolio(symbol) VALUES(?)", (symbol,))
        self.conn.commit()

    def update_stock(self, symbol, price):
        """Update a stock price from the portfolio"""
        self.conn.execute("UPDATE portfolio SET last_price=? WHERE symbol=?", (price, symbol))
        self.conn.commit()

    def get_stock_price(self, symbol):
        """Return a stock price"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT last_price FROM portfolio WHERE symbol=?", (symbol,))
        value = cursor.fetchone()
        if value is None:
            raise ValueError("stock not found")
        return value[0]

    def remove_stock(self, symbol):
        """Remove a stock from the portfolio"""
        self.conn.execute("DELETE FROM portfolio WHERE symbol=?", (symbol,))
        self.conn.commit()

    def list_stocks(self):
        """List all stocks in the portfolio"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT symbol,last_price FROM portfolio")

        stocks = cursor.fetchall()
        return [{"symbol": x[0], "last_price": x[1]} for x in stocks]

    def update_setting(self, name, value):
        """Update a setting, insert if not exists"""
        self.conn.execute("INSERT OR REPLACE INTO settings VALUES (?, ?)", (name, value))
        self.conn.commit()

    def get_setting(self, name):
        """Return a setting value"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE name=?", (name,))
        return cursor.fetchone()

    def list_settings(self):
        """List all stored settings"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM settings")

        stocks = cursor.fetchall()
        return [x[0] for x in stocks]
