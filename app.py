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



@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        gid = request.form['gid']
        password_candid = request.form['password']

        cur = mysql.connection.cursor()

        result = cur.execute(" SELECT * FROM groups  WHERE gid = %s", [gid])

        if result == 0:
            flash('Group id not found ', 'danger')
            return render_template('login.html')
        if result > 0:
            data = cur.fetchone()
            password = data['password']

        if sha256_crypt.verify(password_candid, password):

            session['logged_in'] = True
            session['gid'] = gid
            session['level'] = '-1'
            flash('Login successful', 'success')
            return redirect(url_for('l2'))
        else:
            flash('Wrong username/password', 'danger')

        cur.close()

    return render_template('homepage.html')


@app.route('/you_are_looking_for_nums', methods=['GET', 'POST'])
def l1():
    return render_template('level1.html')

@app.route('/level2', methods=['GET', 'POST'])
def l2():
    if session['level'] >= '0':
        if request.method == 'POST':
            if request.form['password']=='9152':
                session['level'] = '1'
                return render_template('level2.html')
            else:
                flash('wrong password','danger')
                return redirect(url_for('l1'))
        else:
            return render_template('password_page.html')
    else:
        return redirect(request.referrer)
    return render_template('level2.html')




if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)