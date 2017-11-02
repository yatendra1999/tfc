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
            session['level'] = '0'
            flash('Login successful', 'success')
            return redirect(url_for('l1'))
        else:
            flash('Wrong username/password', 'danger')
            return redirect(url_for('homepage'))
        cur.close()

    return render_template('homepage.html')


@app.route('/level1',methods=['GET', 'POST'])
def l1():
    if 'logged_in' in session:
        if request.method == 'POST':
            red = request.form['red']
            green = request.form['green']
            blue = request.form['blue']
            yellow = request.form['yellow']
            if yellow == '0':
                if blue == '3':
                    if green == '3':
                        if red == '3':
                            session['level'] = '1'
                            return redirect(url_for('l2'))
                        else:
                            flash('WRONG INPUT ', 'danger')
                            return render_template('new_level1.html')
                    else:
                        flash('WRONG INPUT ', 'danger')
                        return render_template('new_level1.html')
                else:
                    flash('WRONG INPUT ', 'danger')
                    return render_template('new_level1.html')
            else:
                flash('WRONG INPUT ', 'danger')
                return render_template('new_level1.html')
        else:
            return render_template('new_level_1.html')
    else:
        flash('User must login first', 'danger')
        return redirect(url_for('homepage'))


@app.route('/level2', methods=['GET', 'POST'])
def l2():
    if 'logged_in' in session:
        if session['level'] >= '1':
            if request.form['password'] == '':
                session['level'] = '2'
                return render_template('level2.html')
            else:
                flash('wrong password', 'danger')
                return redirect(url_for('l1'))
        else:
            return redirect(request.referrer)
    else:
        flash('User must login first', 'danger')
        return redirect(url_for('homepage'))


@app.route('/you_are_looking_for_nums', methods=['GET', 'POST'])
def l3():
    if 'logged_in' in session:
        if session['level'] >= '1':
            if request.method == 'POST':
                if request.form['password'] == '':
                    session['level'] = '2'
                    return render_template('level3.html')
                else:
                    flash('wrong password', 'danger')
                    return redirect(url_for('l2'))
            else:
                return render_template('password_page.html')
        else:
            return redirect(request.referrer)
    else:
        flash('User must login first', 'danger')
        return redirect(url_for('homepage'))


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully logged out', 'success')
    return redirect(url_for('homepage'))


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)