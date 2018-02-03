# Import tables model from models.py
from models import Base
from models import User
from models import Categories
from models import CategoryItem

from flask import Flask
from flask import render_template
from flask import url_for
from flask import jsonify
from flask import request
from flask import redirect
from flask import flash
from flask import g
from flask import session as login_session
from flask import make_response

from flask_httpauth import HTTPBasicAuth

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import desc

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import random
import string
import httplib2
import json
import requests

# import google oauth configuration file
CLIENT_ID = json.loads(open('client_secret.json', 'r').
                       read())['web']['client_id']

engine = create_engine('sqlite:///itemCatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

auth = HTTPBasicAuth()


# To generate token and learn about @auth.login_required
@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@auth.verify_password
def verify_password(username_or_token, password):
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
    else:
        user = (session.query(User).filter_by(username=username_or_token).
                first())
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


# Helper function while login with google or facebook
def createUser(login_session):
    newUser = User(username=login_session['username'],
                   email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# When user tries to login user google account
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already '
                                            'connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    return output


# Logout if logged in through google
@app.route('/gdisconnect')
@auth.login_required
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not '
                                 'connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given '
                                 'user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# When user tries to login user facebook account
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    app_id = json.loads(open('fb_client_secret.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secret.json', 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/oauth/access_token'
           '?grant_type=fb_exchange_token&client_id=%s&client_secret'
           '=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token))
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.11/me"
    '''
        Due to the formatting for the result from the server token exchange
        we have to split the token first on commas and select the first index
        which gives us the key : value for the server access token then we
        split it on colons to pull out the actual token value and replace
        the remaining quotes with nothing so that it can be used directly
        in the graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = ('https://graph.facebook.com/v2.11/me?access_token=%s&fields='
           'name,id,email' % token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    flash("Now logged in as %s" % login_session['username'])
    return output


# Logout if logged in through facebook
@app.route('/fbdisconnect')
@auth.login_required
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = ('https://graph.facebook.com/%s/permissions?'
           'access_token=%s' % (facebook_id, access_token))
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Disconnect based on provider(google, facebook, local)
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        if login_session['provider'] == 'local':
            pass
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('index'))
    else:
        flash("You were not logged in")
        return redirect(url_for('index'))


# Login page url
@app.route('/login/')
def showLogin():
    state = (''.join(random.choice(string.ascii_uppercase +
             string.digits) for x in xrange(32)))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# API endpoint
@app.route('/catalog.json')
def catalogJSON():
    categories = session.query(Categories).all()
    result = {'Category': []}
    i = 0
    for category in categories:
        temp = category.serialize
        result['Category'].append(temp)
        items = (session.query(CategoryItem).filter_by(category_id=category.id)
                 .all())
        result['Category'][i]['items'] = [item.serialize for item in items]
        i = i+1
    return jsonify(result)


# Home page for item catalog app
@app.route('/')
def index():
    categories = session.query(Categories).filter_by().all()
    items = (session.query(CategoryItem).order_by(desc(CategoryItem.id)).
             limit(3))
    if 'username' not in login_session:
        return render_template('publicindex.html',
                               categories=categories,
                               items=items)
    else:
        user = session.query(User).filter_by(id=login_session['user_id']).one()
        return render_template('index.html',
                               categories=categories,
                               items=items,
                               user=user)


# List of items of a particular category
@app.route('/catalog/<category>/items')
def category_items(category):
    categories = session.query(Categories).filter_by().all()
    query_category = session.query(Categories).filter_by(name=category).one()
    items = (session.query(CategoryItem).
             filter_by(category_id=query_category.id).all())
    return render_template('category_items.html',
                           categories=categories,
                           items=items,
                           current_category=query_category)


# Detail about a particular item
@app.route('/catalog/<int:category>/<item>')
def item(category, item):
    item = session.query(CategoryItem).filter_by(name=item).one()
    category = session.query(Categories).filter_by(id=item.category_id).one()
    user = session.query(User).filter_by(id=item.user_id).one()
    creator = getUserInfo(user.id)
    if(('username' not in login_session) or
        (creator.id != login_session['user_id'])
       ):
        return render_template('publicItem.html',
                               item=item,
                               category=category,
                               user=user)
    else:
        return render_template('item.html',
                               item=item,
                               category=category,
                               user=user)


# Creating a new item
@app.route('/catalog/new', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        category = (session.query(Categories).
                    filter_by(name=request.form['vl']).one())
        user = session.query(User).filter_by(id=login_session['user_id']).one()
        newItem = CategoryItem(name=request.form['name'],
                               description=request.form['description'],
                               price="$" + request.form['price'],
                               category_id=category.id,
                               categories=category,
                               user_id=user.id,
                               user=user)
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('index'))

    else:
        categories = session.query(Categories).filter_by().all()
        return render_template('newItem.html', categories=categories)


# Editing existing item
@app.route('/catalog/<int:category>/<item>/edit', methods=['GET', 'POST'])
def editItem(category, item):
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(CategoryItem).filter_by(name=item).one()
    if login_session['user_id'] != item.user_id:
        return ("<script>function myFunction() {alert("
                "'You are not authorized to edit menu items to this restaurant"
                ".Please create your own restaurant in order to add items.');}"
                "</script><body onload='myFunction()''>")
    if request.method == 'POST':

        category = (session.query(Categories).
                    filter_by(name=request.form['vl']).one())

        user = session.query(User).filter_by(id=login_session['user_id']).one()

        editedItem = (session.query(CategoryItem).
                      filter_by(name=request.form['name']).one())

        if request.form['name'] != editedItem.name:
            editedItem.name = request.form['name']
        if request.form['description'] != editedItem.description:
            editedItem.description = request.form['description']
        if request.form['price'] != editedItem.price:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('index'))

    else:
        category = (session.query(Categories).
                    filter_by(id=item.category_id).one())
        return render_template('editItem.html', item=item, category=category)


# Deleting existing item
@app.route('/catalog/<int:category>/<item>/delete', methods=['GET', 'POST'])
def deleteItem(category, item):
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(CategoryItem).filter_by(name=item).one()
    if login_session['user_id'] != item.user_id:
        return ("<script>function myFunction() {"
                "alert('You are not authorized to delete menu items to this "
                "restaurant. Please create your own restaurant in order to "
                "add items.');}</script><body onload='myFunction()''>")
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('index'))
    else:
        return render_template('deleteItem.html', category=category, item=item)


# Making a new user from registration form
@app.route('/new_users/', methods=['GET', 'POST'])
def new_users():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if username is None or password is None:
            return redirect(url_for('index'))
        if((session.query(User).filter_by(username=username).first())
            is not None
           ):
            user = session.query(User).filter_by(username=username).first()
            if user.verify_password(password):
                return jsonify({'message': 'user already exists'}), 200
        user = User(username=username, email=email)
        user.hash_password(password)
        session.add(user)
        session.commit()
        flash("New user added: %s" % username)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


# Login using login form
@app.route('/existing_users/', methods=['GET', 'POST'])
def existing_users():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email is None or password is None:
            abort(400)
        user = session.query(User).filter_by(email=email).first()
        if user is not None:
            login_session['username'] = user.username
            login_session['email'] = user.email
            login_session['provider'] = 'local'
            login_session['user_id'] = user.id
            if user.verify_password(password):
                flash("User logged in: %s" % user.username)
                return redirect(url_for('index'))
            else:
                flash("Wrong credentials")
                return redirect(url_for('index'))
        else:
            flash("Wrong credentials")
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


# How auth.login_required works
@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


# Running this file
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
