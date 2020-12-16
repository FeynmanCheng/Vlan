from flask import Flask
import telnet
app = Flask(__name__)

@app.route('/')
def hello_world():
    telnet.get_connection()
    return 'Hello, World!'

def get_telnet():
    pass 
