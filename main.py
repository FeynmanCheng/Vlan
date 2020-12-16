from flask import Flask
from flask.globals import request
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
    
    tn = TN.login(ip,user,passwd)
    
    return tn.read_until(b'hadoop@Slave2:~$',1).decode('ascii')

@app.route('/command/<string:cmd>')
def send_command(cmd):
    cmd += '\n'
    tn = TN.get_tn()
    tn.write(cmd.encode('utf-8'))
    return tn.read_until(b'hadoop@Slave2:~$',1).decode('ascii')

