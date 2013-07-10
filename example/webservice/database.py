#!/usr/bin/python

import sqlite3


class MyServiceDatabase():
    """ Database handler class """

    def __init__(self, db="database.db"):
        """Open database"""
        self.conn = sqlite3.connect(db)

        #Create tables
        self.conn.execute("CREATE TABLE IF NOT EXISTS portfolio (name TEXT UNIQUE, value TEXT DEFAULT '0')")
        self.conn.execute("CREATE TABLE IF NOT EXISTS settings (name TEXT UNIQUE, value TEXT)")
        self.conn.commit()

    def add_stock(self, name):
        """Add a stock to the portfolio"""
        self.conn.execute("INSERT INTO portfolio(name) VALUES(?)", (name,))
        self.conn.commit()

    def get_stock(self, name):
        """Return a stock value"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM portfolio WHERE name=?", (name,))
        value = cursor.fetchone()
        if value is None:
            raise ValueError("stock not found")
        return value[0]

    def remove_stock(self, name):
        """Remove a stock from the portfolio"""
        self.conn.execute("DELETE FROM portfolio WHERE name=?", (name,))
        self.conn.commit()

    def list_stocks(self):
        """List all stocks in the portfolio"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM portfolio")

        stocks = cursor.fetchall()
        return [x[0] for x in stocks]

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
