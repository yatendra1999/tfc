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
    if 'logged_in' in session:
        if session['level'] == '0':
            return redirect(url_for('l1'))
        elif session['level'] == '1':
            return redirect(url_for('l2'))
        elif session['level'] == '2':
            return redirect(url_for('l3'))
        elif session['level'] == '3':
            return redirect(url_for('l4'))
        elif session['level'] == '4':
            return redirect(url_for('l5'))
        elif session['level'] == '5':
            return redirect(url_for('lboard'))
        else:
            return redirect(url_for('logout'))

    else:
        if request.method == 'POST':
            username = request.form['username']
            password_candid = request.form['password']
            cur = mysql.connection.cursor()
            result = cur.execute(" SELECT * FROM users WHERE user = %s", [username])
            if result == 0:
                flash('Username not found ', 'danger')
                return render_template('homepage.html')
            if result > 0:
                data = cur.fetchone()
                password = data['password']

            if password == password_candid:

                session['logged_in'] = True
                session['username'] = username
                session['level'] = '0'
                flash('Login successful', 'success')
                return redirect(url_for('l1'))
            else:
                flash('Wrong username/password', 'danger')
                return redirect(url_for('homepage'))
            cur.close()

        return render_template('homepage.html')


@app.route('/level1', methods=['GET', 'POST'])
def l1():
    if 'logged_in' in session:
        if request.method == 'POST':
            print("running loop")
            red = int(request.form['red'])
            green = int(request.form['green'])
            blue = int(request.form['blue'])
            yellow = int(request.form['yellow'])
            if yellow == 0:
                if blue == 3:
                    if green == 3:
                        if red == 3:
                            session['level'] = '1'
                            return redirect(url_for('l2'))
                        else:
                            flash('WRONG ANSWER ', 'danger')
                            return render_template('level1.html')
                    else:
                        flash('WRONG INPUT ', 'danger')
                        return render_template('level1.html')
                else:
                    flash('WRONG INPUT ', 'danger')
                    return render_template('level1.html')
            else:
                print("Wrong4")
                flash('WRONG INPUT ', 'danger')
                return render_template('level1.html')
        else:
            return render_template('level1.html')
    else:
        flash('User must login first', 'danger')
        return redirect(url_for('homepage'))


@app.route('/potato_io/shots/count/enterhere', methods=['GET', 'POST'])
def l2():
    if 'logged_in' in session:
        if session['level'] >= '1':
            return render_template('level2.html')
        else:
            return redirect(request.referrer)
    else:
        flash('user must login first', 'danger')
        return redirect(url_for(homepage))

@app.route('/potato_io/shots/count/46745', methods=['GET', 'POST'])
def svs():
    if 'logged_in' in session:
        if session['level'] == '1':
            session['level'] = '2'
            return redirect(url_for('l3'))
        else:
            return redirect(request.referrer)
    else:
        flash('user must login first', 'danger')
        return redirect(url_for(homepage))

@app.route('/you_are_looking_for_nums', methods=['GET', 'POST'])
def l3():
    if 'logged_in' in session:
        if session['level'] >= '2':
            if request.method == 'POST':
                if request.form['password'] == '9152':
                    session['level'] = '3'
                    return redirect(url_for('l4'))
                else:
                    flash('wrong password', 'danger')
                    return redirect(url_for('l3'))
            else:
                return render_template('level3.html')
        else:
            return redirect(request.referrer)
    else:
        flash('User must login first', 'danger')
        return redirect(url_for('homepage'))


@app.route('/level4', methods=['GET', 'POST'])
def l4():
    if 'logged_in' in session:
        if session['level'] >= '3':
            return render_template('level4.html')
        else:
            return redirect(request.referrer)
    else:
        flash('User must login first', 'danger')
        return redirect(url_for('homepage'))


@app.route('/route_5', methods=['GET', 'POST'])
def logg5():
    if 'logged_in' in session:
        if session['level'] >= '3':
            if request.method == 'POST':
                if request.form['password'] == '':
                    return redirect(url_for('l5'))
                else:
                    flash('wrong password', 'danger')
                    return render_template('password_page.html')
            else:
                return render_template('r5.html')
        else:
            return redirect(url_for('homepage'))
    else:
        flash('User must login first', 'danger')
        return redirect(url_for('homepage'))

@app.route('/turtle', methods=['GET', 'POST'])
def l5():
    if 'logged_in' in session:
        if session['level'] >= '4':
            session['level'] = '5'
            return re




@app.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully logged out', 'success')
    return redirect(url_for('homepage'))


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)