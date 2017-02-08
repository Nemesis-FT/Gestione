from flask import Flask, session, url_for, redirect, request, render_template, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "fantabosco"

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


# Funzioni del sito
def login(username, password):
    user = User.query.filter_by(username=username).first()
    try:
        return password == user.passwd
    except AttributeError:
        # Se non esiste l'Utente
        return False

# Sito
@app.route('/')
def page_home():
    if 'username' not in session:
        return redirect(url_for('page_login'))
    else:
        session.pop('username')
        return redirect(url_for('page_login'))

@app.route('/login', methods=['GET', 'POST'])
def page_login():
    if request.method == 'GET':
        css = url_for("static", filename="style.css")
        return render_template("login.html.j2", css=css)
    else:
        if login(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('page_dashboard', user=session['username']))
        else:
            abort(403)

@app.route('/dashboard')
def page_dashboard():
    banner = url_for("static", filename="banner.png")
    css = url_for("static", filename="style.css")
    if 'username' not in session:
        return render_template("dashboard.html.j2", css=css, banner=banner)
    else:
        return render_template("dashboard.html.j2", css=css, user=session['username'], banner=banner)

@app.route('/user_add', methods=['GET', 'POST'])
def page_user_add():
    if 'username' not in session:
        return redirect(url_for('page_dashboard'))
    if request.method == 'GET':
        css = url_for("static", filename="style.css")
        return render_template("User/add.html.j2", css=css, type="utenti", user=session["username"])
    else:
        nuovouser = User(request.form['username'], request.form['passwd'])
        db.session.add(nuovouser)
        db.session.commit()
        return redirect(url_for('page_user_list'))

@app.route('/user_del/<int:uid>')
def page_user_del(uid):
    if 'username' not in session:
        return redirect(url_for('page_dashboard'))
    user = User.query.get(uid)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('page_user_list'))

@app.route('/user_list')
def page_user_list():
    if 'username' not in session:
        return redirect(url_for('page_dashboard'))
    users = User.query.all()
    css = url_for("static", filename="style.css")
    return render_template("User/list.html.j2", css=css, users=users, type="utenti", user=session["username"])

@app.route('/user_show/<int:uid>', methods=['GET', 'POST'])
def page_user_show(uid):
    if 'username' not in session:
        return redirect(url_for('page_dashboard'))
    if request.method == "GET":
        users = User.query.get(uid)
        css = url_for("static", filename="style.css")
        return render_template("User/show.html.j2", css=css, users=users, user=session["username"])
    else:
        users = User.query.get(uid)
        users.username = request.form["username"]
        users.passwd = request.form["passwd"]
        db.session.commit()
        return redirect(url_for('page_user_list'))

@app.route('/riassunti_add', methods=['GET', 'POST'])
def page_riassunti_add():
    if 'username' not in session:
        return redirect(url_for('page_dashboard'))
    if request.method == 'GET':
        css = url_for("static", filename="style.css")
        return render_template("Riassunti/add.html.j2", css=css, type="riassunti", user=session["username"])
    else:
        nuovoriassunto= Riassunto(request.form['rnome'], request.form['rmateria'], request.form['rdescrizione'], request.form['rlink'])
        db.session.add(nuovoriassunto)
        db.session.commit()
        return redirect(url_for('page_riassunti_list'))

@app.route('/riassunti_del/<int:rid>')
def page_riassunti_del(rid):
    if 'username' not in session:
        return redirect(url_for('page_dashboard'))
    riassunto = Riassunto.query.get(rid)
    db.session.delete(riassunto)
    db.session.commit()
    return redirect(url_for('page_riassunto_list'))

@app.route('/riassunti_list')
def page_riassunti_list():
    if 'username' not in session:
        riassunti = Riassunto.query.all()
        css = url_for("static", filename="style.css")
        return render_template("Riassunti/list_noob.html.j2", css=css, riassunti=riassunti, type="riassunti")
    riassunti = Riassunto.query.all()
    css = url_for("static", filename="style.css")
    return render_template("Riassunti/list.html.j2", css=css, riassunti=riassunti, type="riassunti", user=session["username"])

@app.route('/riassunti_show/<int:rid>', methods=['GET', 'POST'])
def page_riassunti_show(rid):
    if 'username' not in session:
        return redirect(url_for('page_dashboard'))
    if request.method == "GET":
        riassunto = Riassunto.query.get(rid)
        css = url_for("static", filename="style.css")
        return render_template("Riassunti/show.html.j2", css=css, riassunto=riassunto,type="riassunti", user=session["username"])
    else:
        riassunto = Riassunto.query.get(rid)
        riassunto.rnome = request.form["rnome"]
        riassunto.rmateria = request.form["rmateria"]
        riassunto.rdescrizione = request.form["rdescrizione"]
        riassunto.rlink = request.form["rlink"]
        db.session.commit()
        return redirect(url_for('page_riassunti_list'))
