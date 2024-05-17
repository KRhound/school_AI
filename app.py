from flask import Flask, render_template, request, redirect, url_for
import calendar as cal
import sqlite3
from datetime import datetime

app = Flask(__name__)

# 년, 월 선택 기능
@app.route('/')
def index():
    current_year = datetime.now().year
    return render_template('index.html', current_year=current_year)

# calendar 기눙
@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if request.method == 'GET':
        now = datetime.now()
        year = now.year
        month = now.month
        first_day, num_days = get_days_in_month(year, month)
        conn = sqlite3.connect('web.db')
        cursor = conn.cursor()
        select_query = """
        SELECT day, event, description
        FROM events WHERE year = ? AND month = ? AND status = 1
        """
        cursor.execute(select_query, (year, month))
        events = cursor.fetchall()
        if events:
            return render_template('calendar.html', year=year, month=month, first_day=first_day, num_days=num_days, events=events)
        else:
            return render_template('calendar.html', year=year, month=month, first_day=first_day, num_days=num_days)
    elif request.method == 'POST':
        year = int(request.form['year'])
        month = int(request.form['month'])
        first_day, num_days = get_days_in_month(year, month)
        conn = sqlite3.connect('web.db')
        cursor = conn.cursor()
        select_query = """
        SELECT day, event, description
        FROM events WHERE year = ? AND month = ? AND status = 1
        """
        cursor.execute(select_query, (year, month))
        events = cursor.fetchall()
        if events:
            return render_template('calendar.html', year=year, month=month, first_day=first_day, num_days=num_days, events=events)
        else:
            return render_template('calendar.html', year=year, month=month, first_day=first_day, num_days=num_days)

# 학사일정 추가 기능
@app.route('/add', methods=['GET', 'POST'])
def add_event():
    current_year = datetime.now().year
    if request.method == 'POST':
        year = int(request.form['year'])
        month = int(request.form['month'])
        day = int(request.form['day'])
        event = request.form['event']
        description = request.form['description']

        conn = sqlite3.connect('web.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO events (year, month, day, event, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (year, month, day, event, description))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    else:
        return render_template('add.html', current_year=current_year)

def get_days_in_month(year, month):
    first_day, num_days = cal.monthrange(year, month)
    return first_day, num_days # 첫 요일, 총 일수

if __name__ == '__main__':
    app.run(debug=True)
