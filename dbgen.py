from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    passwd = db.Column(db.String(80))

    def __init__(self, username, passwd):
        self.username = username
        self.passwd = passwd

    def __repr__(self):
        return "<User {}>".format(self.username, self.passwd)

class Riassunto(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    rnome = db.Column(db.String(80))
    rmateria = db.Column(db.String(10))
    rdescrizione = db.Column(db.String(100))
    rlink = db.Column(db.String(100))

def __init__(self, rnome, rmateria, rdescrizione, rlink):
        self.rnome = rnome
        self.rmateria = rmateria
        self.rdescrizione = rdescrizione
        self.rlink = rlink

def __repr__(self):
    return "<Riassunto {}>".format(self.rnome, self.rmateria)

class Consegne(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    cnome = db.Column(db.String(80))
    cdata = db.Column(db.String(10))
    clink = db.Column(db.String(100))
    cscript = db.Column(db.String(1000))

def __init__(self, cnome, cdata, clink, cscript):
        self.cnome = cnome
        self.cdata = cdata
        self.clink = clink
        self.cscript = cscript

def __repr__(self):
    return "<Consegna {}>".format(self.cnome, self.cdata)
db.create_all()

nuovouser = User('admin', 'admin')
db.session.add(nuovouser)
db.session.commit()
