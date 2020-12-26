from flask import Flask
from flask.globals import request
from telnet import Telnet
app = Flask(__name__)

TN = Telnet()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login/<string:hostname>')
def login(hostname):
    return TN.login_no_passwd(hostname)

@app.route('/command/<string:hostname>',methods=['POST'])
def send_command(hostname):

    try:
        cmd = request.get_json()['cmd']
        
        msg = TN.run_cmd(hostname, cmd)
        return msg

    except Exception:
        return {'data': None},400


@app.route('/logout/<string:ip>')
def logout(ip):
    return TN.logout(ip)

@app.route('/config/<string:hostname>')
def config(hostname):
    output, code = TN.config(hostname)
    if code != 0:
        return {'data':output},400
    return {'data':output}, 200