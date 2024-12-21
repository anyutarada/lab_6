# -*- coding: cp1251 -*-
from flask import Flask, request, render_template
import sqlite3
from random import randint


def connectDB():
    connection = sqlite3.connect('database.db')
    connection.cursor().execute('pragma encoding=UTF8')
    return connection


def disconnectDB(connection):
    connection.commit()
    connection.close()


def createBD():
    connection = connectDB()
    cursor = connection.cursor()
    cursor.execute('pragma encoding=UTF8')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Gifts (
    personid INTEGER PRIMARY KEY,
    Fullname TEXT NOT NULL,
    Gift TEXT NOT NULL,
    Price INTEGER,
    Status TEXT NOT NULL
    )
    ''')

    if len(cursor.execute('SELECT * FROM Gifts').fetchall()) == 0:
        for i in range(1, 11):
            cursor.execute('INSERT INTO Gifts (fullname, gift, price, status) VALUES (?, ?, ?, ?)',
                           (f'<ФИО{i}>', f'<Подарок{i}>',
                            randint(1000, 10000), f'{"не " * randint(0, 1)}куплен'.capitalize()))

    disconnectDB(connection)


def checkBDdata():
    connection = connectDB()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Gifts')
    for x in cursor.fetchall():
        print(x)

    disconnectDB(connection)


createBD()
checkBDdata()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    gifts = connectDB().cursor().execute('SELECT * FROM Gifts').fetchall()
    return render_template('template.html', gifts=gifts,
                           headers=['ФИО', 'Подарок', 'Цена', 'Статус']), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
