from flask import Flask, render_template, request, redirect, url_for
import calendar as cal
import sqlite3

app = Flask(__name__)



# 년, 월 선택 기능
@app.route('/')
def index():
    current_year = 2024
    return render_template('index.html', current_year=current_year)

# calendar 기눙
@app.route('/calendar', methods=['POST'])
def calendar():
    year = int(request.form['year'])
    month = int(request.form['month'])
    first_day, num_days = get_days_in_month(year, month)
    conn = sqlite3.connect('web.db')
    cursor = conn.cursor()
    select_query = """
    SELECT year, month, day
    FROM boards WHERE year = ? AND month = ? status = 1
    """
    cursor.execute(select_query, (year, month))
    events = cursor.fetchall()
    return render_template('calendar.html', year=year, month=month, first_day=first_day, num_days=num_days, events=events)

# 학사일정 추가 기능
@app.route('/add', methods=['GET', 'POST'])
def add_event():
    current_year = 2024
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
