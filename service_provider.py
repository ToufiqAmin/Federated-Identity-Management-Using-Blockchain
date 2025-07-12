
import hashlib
import random
from flask import Flask, request, jsonify, render_template, redirect
import requests

app = Flask(__name__)


ion_sa = []

@app.route('/', methods=['GET', 'POST'])
def service_request():
    if request.method == "POST":
        shareable_address = request.form['shareable_address']
        ion_sa.append(shareable_address)
        response = requests.post('http://127.0.0.1:6002', data={'shareable_address': shareable_address})
        result = response.json()

        if result['success']:
            return redirect('/confirm')
        else:
            return render_template('service_request.html', error_message='Profile not found')

    return render_template('service_request.html')

@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    if request.method == "POST":
        return redirect('/add_block')
    return render_template('confirm.html')


@app.route('/add_block', methods=['GET', 'POST'])
def add_block():
    print(ion_sa[0])
    block_data = {
        'shareable_address': ion_sa[0],
        'service_response': 'report'
    }

    nonce = random.randint(100000000, 1000000000)
    block_string = str(block_data) + str(nonce)
    block_hash = hashlib.sha256(block_string.encode('utf-8')).hexdigest()
    return jsonify({'message': 'Block added to the blockchain', 'block_hash': block_hash})


if __name__ == '__main__':
    app.run(port=6003)
