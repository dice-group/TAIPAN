from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://iermilov:sup3rstr0ngpassw0rd!!!@localhost/tableannotations'

from views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0')
