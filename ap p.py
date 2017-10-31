from flask import Flask, render_template, redirect, url_for, request, session, flash, logging
from flask_mysqldb import MySQL
from wtforms import  StringField, TextAreaField, PasswordField, validators, Form
from passlib.hash import sha256_crypt


app = Flask(__name__)

app.secret_key="sbjkgkuadlasbldsnkaldklasbbanksmladbls"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'shPR2510%*'
app.config['MYSQL_DB'] = 'tech_fest_quiz'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)


class registration(Form):
    group_id = StringField('group_id', [validators.Length(min=1, max=10)])
    user1 = StringField('User1', [validators.Length(min=1, max=10)])
    user2 = StringField('User2', [validators.Length(min=1, max=10)])
    user3 = StringField('User3', [validators.Length(min=1, max=10)])
    user4 = StringField('User4', [validators.Optional()])
    user5 = StringField('User5', [validators.Optional()])
    password = PasswordField('Password', [validators.DataRequired(),validators.EqualTo('confirm', message="passwords do not match")])
    confirm = PasswordField('Confirm Password')



@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        gid = request.form['gid']
        password_candid = request.form['password']

        cur = mysql.connection.cursor()

        result = cur.execute(" SELECT * FROM groups WHERE gid = %s", [gid])

        if result == 0:
            flash('Group id not found ', 'danger')
            return render_template('login.html')
        if result > 0:
            data = cur.fetchone()
            password = data['password']

        if sha256_crypt.verify(password_candid, password):

            session['logged_in'] = True
            session['gid'] = gid
            session['level'] = '0'
            flash('Login successful', 'success')
        else:
            flash('Wrong username/password', 'danger')

        cur.close()

    return render_template('homepage.html')

# @app.route('/register', methods=['GET', 'POST'])
def reg():
    form = registration(request.form)
    if request.method == 'POST' and form.validate():
        gid = form.group_id.data
        user1 = form.user1.data
        user2 = form.user2.data
        user3 = form.user3.data
        user4 = form.user4.data
        user5 = form.user5.data
        if user4 == '':
            user4 = 0
        if user5 == '':
            user5 = 0
        password = sha256_crypt.encrypt(str(form.password.data))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO groups(gid , password, mem1, mem2, mem3, mem4, mem5) VALUES(%s, %s, %s, %s, %s, %s, %s)",(gid, password, user1, user2, user3, user4, user5))
        mysql.connection.commit()
        cur.close()
        flash('You were seccessfully registered', 'success')
        return redirect(url_for('homepage'))
    return render_template('register.html', form=form)


@app.route('/you_are_looking_for_nums', methods=['GET', 'POST'])
def l1():
    if session.level == '0':
        if request.method == 'POST':
            password = request.form['password']
            if password == '9152':
                return render_template('level2.html')
            else:
                flash('wrong password','success')
                return render_template('level1.html')
        else:
            return render_template('level1.html')

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)