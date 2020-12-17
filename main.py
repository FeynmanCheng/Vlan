from flask import Flask
from flask.globals import request
from flask.wrappers import Response
from telnet import Telnet
app = Flask(__name__)

TN = Telnet()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login/<string:ip>')
def login(ip):
    user = request.args.get('user')
    passwd = request.args.get('passwd')

    return TN.login(ip,user,passwd)

@app.route('/command/<string:ip>',methods=['POST'])
def send_command(ip):

    try:
        cmd = request.get_json()['cmd']

        if ip == 'T':
            ip = '172.19.241.171'
        
        msg = TN.run_cmd(ip,cmd)
        return msg

    except Exception:
        return {'data': None},400


@app.route('/logout/<string:ip>')
def logout(ip):
    return TN.logout(ip)