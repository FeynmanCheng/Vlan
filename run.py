from flask_script import Manager
from main import app
from flask_cors import CORS

app.debug = True
app.env = 'development'
manager = Manager(app)
CORS(app)

if __name__ == "__main__":
    manager.run()
