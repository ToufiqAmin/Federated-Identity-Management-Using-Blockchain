from flask import Flask, render_template, redirect, url_for
from controllernode import app as app1
from saverify import app as app2
from service_provider import app as app3
import subprocess


app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    
    
    app1_port = 6001
    app2_port = 6002
    app3_port = 6003

    app1_process = subprocess.Popen(['python3', 'controllernode.py', str(app1_port)])
    app2_process = subprocess.Popen(['python3', 'saverify.py', str(app2_port)])
    app3_process = subprocess.Popen(['python3', 'service_provider.py', str(app3_port)])
    
    app.run(port=8000)
