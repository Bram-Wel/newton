#!/usr/bin/python3
"""Flask routes."""

from flask import request, redirect, render_template, url_for, flash, abort
from flask_login import login_user, logout_user, login_required
from deriv_api.errors import ResponseError

from deriv import app, active_symbols, json
from deriv.forms import LoginForm

user = None
api_token = ''


@app.route('/')
@app.route('/index/')
@app.route('/home/')
def index():
    """Index page."""
    return render_template('index.html')


@app.route('/even-odd-percentage')
def EO_percentage():
    """Even/Odd percentages."""
    return render_template('even_odd.html', symbols=active_symbols)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login to deriv account."""
    form = LoginForm()
    if form.validate_on_submit():
        global user, api_token
        api_token = form.token.data
        from deriv import asyncio
        from deriv.models import User, get_authorise
        try:
            authorise = asyncio.run(get_authorise(api_token))
        except ResponseError as e:
            flash(f"{e.message}", category='danger')
        else:
            if 'authorize' in authorise:
                authorise = authorise['authorize']
                # authorise['token'] = api_token
                # with open('deriv/deriv.json', 'w+',encoding='utf-8') as file:
                #    json.dump(authorise, file)
                # user = User(authorise['fullname'], authorise['loginid'],
                #            authorise['user_id'], authorise['email'],
                #            authorise['balance'], authorise['currency'])
                user = User(authorise)
                login_user(user)
                flash(f"{authorise['loginid']} | Balance:\
                        {authorise['balance']} {authorise['currency']}",
                      category='success')
                next = request.args.get('next')
                # will implement validation for next url later -> security
                # if not url_has_allowed_host_and_scheme(next, request.host):
                #   return abort(400)
                return redirect(next or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register')
def register():
    """Register deriv account."""
    return redirect('https://api.deriv.com')


@app.route('/logout')
def logout():
    """Log the user out."""
    logout_user()
    flash(f"{user.fullname} logged out!", category='info')
    return redirect(url_for('index'))


@app.route('/user')
@login_required
def loaded_user():
    """Extra page."""
    return render_template('user.html', symbols=active_symbols)
