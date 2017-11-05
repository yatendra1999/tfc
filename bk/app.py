from flask import Flask, render_template, redirect, url_for, request, session, flash, logging
from flask_mysqldb import MySQL
from wtforms import  StringField, TextAreaField, PasswordField, validators, Form
from passlib.hash import sha256_crypt


app = Flask(__name__)

app.secret_key="sbjkgkuadlasbldsnkaldklasbbanksmladbls"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'shPR2510%*'
app.config['MYSQL_DB'] = 'idp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return render_template('dashboard.html')
    else:
        flash('User must login first', 'danger')
        return redirect(url_for('login'))

class registration(Form):
    name = StringField('Name', [validators.Length(min=1, max=100)])
    email = StringField('E-mail', [validators.Email(message="please enter a valid e-mail address")])
    username = StringField('Username', [validators.Length(min=1, max=100)])
    password = PasswordField('Password', [validators.DataRequired(),validators.EqualTo('confirm', message="passwords do not match")])
    confirm = PasswordField('Confirm Password')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candid = request.form['password']

        cur = mysql.connection.cursor()

        result = cur.execute(" SELECT * FROM users  WHERE username = %s", [username])

        if result == 0:
            flash('Username not found ', 'danger')
            return render_template('login.html')
        if result > 0:
            data = cur.fetchone()
            password = data['password']

        if sha256_crypt.verify(password_candid, password):

            session['logged_in'] = True
            session['username'] = username
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))

        else:
            flash('Wrong username/password', 'danger')

        cur.close()

    return render_template('login.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def reg():
    form = registration(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username, password, name, email) VALUES(%s, %s, %s, %s)",(username, password, name, email))
        mysql.connection.commit()
        cur.close()
        flash('You were seccessfully registered', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully logged out', 'success')
    return redirect(url_for('login'))


class oide(Form):
    code = TextAreaField('Code', [validators.Length(min=1)])
    input = TextAreaField('Input')

@app.route('/oide')
def oide():
    return render_template('oide.html')


@app.route('/forum')
def forum():
    return render_template('forum.html')


@app.route('/assignments')
def assn():
    return render_template('assignments.html')


@app.route('/practise')
def prac():
    return render_template('practise.html')


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)