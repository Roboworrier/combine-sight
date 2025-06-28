from flask import Flask, render_template, request, redirect, url_for
import os
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

@app.route('/', methods=['GET', 'POST'])
def landing_page():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            return render_template('landing.html', name=name)
    return render_template('landing.html', name=None)

@app.route('/redirect/<target>')
def redirect_to_target(target):
    # If coming from /welcome, always go to login page
    referrer = request.referrer or ''
    if '/welcome' in referrer:
        if target == 'option1':
            return redirect('https://localhost:5000/login')  # BotSight login page
        elif target == 'option2':
            return redirect('http://localhost:5001/login')   # ChipSight login page
        else:
            return redirect(url_for('general_landing'))
    # Default/legacy logic (for plant head SSO/auto-login)
    if target == 'option1':
        return redirect(url_for('auto_login1'))
    elif target == 'option2':
        return redirect(url_for('auto_login2'))
    else:
        return redirect(url_for('landing_page'))

def generate_sso_token():
    s = URLSafeTimedSerializer('your-very-secret-key')
    return s.dumps({'user': 'plant_head'}, salt='sso-login')

@app.route('/auto_login1')
def auto_login1():
    # BotSight does not support SSO or passwordless login, so use the old auto-login form
    return render_template('auto_login1.html')

@app.route('/auto_login2')
def auto_login2():
    token = generate_sso_token()
    return redirect(f'http://localhost:5001/sso_login?token={token}')  # CHIPSIGHT

@app.route('/welcome')
def general_landing():
    return render_template('general_landing.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True) 