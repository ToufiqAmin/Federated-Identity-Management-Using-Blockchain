###  This code is written on as an experiment for a newly conceptualized Blockchain system for national identification
###  
###
###
###


### Importing necessary modules

import hashlib
from base58 import b58encode_check
import random
import string
from flask import Flask, request, render_template, redirect
from twilio.rest import Client
import sqlite3

app = Flask(__name__)


### Credebtuaks to send otp

account_sid = 'AC3a25cf46a16719af1a51eeb23c02a97c'
auth_token = '66489b532a896cdd76e6cebf9a44dd69'
client = Client(account_sid, auth_token)


### Identity owner node

users = {} 


### Database connection at the controller's end

conn = sqlite3.connect('test.db', check_same_thread=False)
c = conn.cursor()

c.execute(
    '''CREATE TABLE IF NOT EXISTS profiles(name text, dateofbirth text, identifier text, shareable_address text, phone_number text, profile_hash text)''')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user information from the form
        name = request.form['name']
        birthdate = request.form['birthdate']
        phone_number = request.form['phone_number']
        zipcode = request.form['zip_code']

        otp = str(random.randint(100000, 999999))
        print(otp)
        """message = client.messages.create(
            body='Your OTP is: ' + otp,
            from_='+18667922086',
            to=phone_number
        )"""

        print(phone_number)
        users[phone_number] = {'name': name, 'birthdate': birthdate, 'zipcode': zipcode.zfill(5), 'otp': otp}

        return redirect('/verify?phone_number=' + phone_number)
    else:
        return render_template('index.html')


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        # Get OTP and phone number from the form
        otp = request.form['otp']
        phone_number = "+" + request.form['phone_number'].strip(" ")

        # Check if OTP is correct
        if otp == users[phone_number]['otp']:
            return redirect('/personal')
        else:
            return redirect('/verify?phone_number=' + phone_number)

    else:
        phone_number = request.args.get('phone_number')

        return render_template('verify.html', phone_number=phone_number)


### PII Section

profile = {}



@app.route('/personal', methods=['GET', 'POST'])
def personal():
    if request.method == 'POST':
        # Get user information from the form
        name = request.form['name']
        birthdate = request.form['birthdate']
        phone_number = request.form['phone_number']
        sex = request.form['sex']
        address = request.form['address']
        zipcode = request.form['zip_code'].zfill(5)

        profile['name'] = name
        profile['birthdate'] = birthdate
        profile['phone'] = phone_number
        profile['sex'] = sex
        profile['address'] = address
        profile['zip_code'] = zipcode

        return redirect('/family')
    return render_template('personal.html')


@app.route('/family', methods=['GET', 'POST'])
def family():
    if request.method == 'POST':
        father_name = request.form['father_name']
        father_phone = request.form['father_phone']
        mother_name = request.form['mother_name']
        mother_phone = request.form['mother_phone']

        profile['father_name'] = father_name
        profile['father_phone'] = father_phone
        profile['mother_name'] = mother_name
        profile['mother_phone'] = mother_phone

        return redirect('/migration')
    return render_template('family.html')


@app.route('/migration', methods=['GET', 'POST'])
def migration():
    if request.method == 'POST':
        placeofbirth = request.form['placeofbirth']
        permaddress = request.form['permaddress']
        curraddress = request.form['curraddress']
        prevaddress = request.form['prevaddress']
        placeofwork = request.form['placeofwork']

        profile['placeofbirth'] = placeofbirth
        profile['permaddress'] = permaddress
        profile['curraddress'] = curraddress
        profile['prevaddress'] = prevaddress
        profile['placeofwork'] = placeofwork

        return redirect('/education')
    return render_template('migration.html')


@app.route('/education', methods=['GET', 'POST'])
def education():
    if request.method == 'POST':
        degree = request.form['degree']
        grade = request.form['grade']

        profile['degree'] = degree
        profile['grade'] = grade

        return redirect('/profession')
    return render_template('education.html')


@app.route('/profession', methods=['GET', 'POST'])
def profession():
    if request.method == 'POST':
        company = request.form['company']
        position = request.form['position']

        profile['company'] = company
        profile['position'] = position

        return redirect('/medical')
    return render_template('profession.html')


@app.route('/medical', methods=['GET', 'POST'])
def medical():
    if request.method == 'POST':
        disease = request.form['disease']
        medicine = request.form['medicine']

        profile['disease'] = disease
        profile['medicine'] = medicine
        return redirect('/criminal')
    return render_template('medical.html')


@app.route('/criminal', methods=['GET', 'POST'])
def criminal():
    if request.method == "POST":
        crime = request.form['crime']
        casestat = request.form['casestat']
        arrestingoffice = request.form['arrestingoffice']

        profile['crime'] = crime
        profile['casestat'] = casestat
        profile['arrestingoffice'] = arrestingoffice

        return redirect('/govtinfo')
    return render_template('criminal.html')


@app.route('/govtinfo', methods=['GET', 'POST'])
def govtinfo():
    if request.method == "POST":
        tinnumber = request.form['tinnumber']
        driverlic = request.form['driverlic']
        voterid = request.form['voterid']

        profile['tinnumber'] = tinnumber
        profile['driverlic'] = driverlic
        profile['voterid'] = voterid





        ### Generate identifier and shareable address using SHA-256 hash


        random.seed()
        zcode = str(profile['zip_code']).zfill(5)
        identifier = zcode + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        sha256_1 = hashlib.sha256((profile['birthdate']+identifier+zcode).encode()).digest()
        ripemd160_1 = hashlib.new('ripemd160', sha256_1).digest()
        sha256_2 = hashlib.sha256(ripemd160_1).digest()
        first_6_digits = sha256_2[:6]
        shareable_address = b58encode_check(first_6_digits + ripemd160_1)

        

        # Store identifier and shareable address in user information dictionary
        
        profile['identifier'] = identifier
        profile['shareable_address'] = shareable_address

        profile_hash = hashlib.sha256(str(profile).encode('utf-8')).hexdigest()

        print(str(profile['name']) + str(profile['birthdate']) + str(profile['identifier']) + str((profile['shareable_address']).decode("utf-8")) + str(profile[
            'phone']) + str(profile_hash))

        c.execute(
            "INSERT INTO profiles (name, dateofbirth, identifier, shareable_address, phone_number, profile_hash) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (profile['name'], profile['birthdate'], profile['identifier'], (profile['shareable_address']).decode("utf-8"), profile['phone'],
             hashlib.sha256(str(profile).encode('utf-8')).hexdigest()))
        conn.commit()

        return render_template('success.html', identifier=identifier, shareable_address=shareable_address)
    return render_template("govtinfo.html")


if __name__ == '__main__':
    app.run(port=6001)
