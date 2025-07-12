from flask import Flask, request, jsonify, render_template
import sqlite3
from twilio.rest import Client


app = Flask(__name__)

# Connect to the SQLite database
conn = sqlite3.connect('test.db', check_same_thread=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        shareable_address = request.form['shareable_address']
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM profiles WHERE shareable_address = ?', (shareable_address,))
        profile = cursor.fetchone()

        if profile is None:
            return jsonify({'success': False, 'message': 'Profile not found'})

        expected_address = profile[3]
        if shareable_address == expected_address:    
            return jsonify({'success': True, 'message': 'Verification Successful'})
        else:
            return jsonify({'success': False, 'message': 'Verification Failed'})

    return render_template('verify_saddress.html')
if __name__ == '__main__':
    app.run(port=6002)
"""
import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute('SELECT name from sqlite_master where type= "table"')
tables = cursor.fetchall()
print(tables)
cursor.execute('SELECT * from profiles')
data = cursor.fetchall()
print(data)
"""