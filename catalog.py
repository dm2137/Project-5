from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from database_setup import Base, Catalog, CatalogItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('/var/www/catalog/catalog/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Pet Catalog Application"

# Connect to Database and create database session
engine = create_engine('postgresql://catalog:cat15log@localhost/catalogitems')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
#    return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# Facebook login
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('/var/www/catalog/catalog/fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('/var/www/catalog/catalog/fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output

# Facebook disconnect
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
#    url = 'https://graph.facebook.com/%s/permissions' % (facebook_id,access_token)
    url = 'https://graph.facebook.com/%s/permissions?fb_exchange_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

# Goggle Login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('/var/www/catalog/catalog/client_secrets.json', scope='')
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
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

# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Making a JSON API Endpoint (GET Request) to view catalog info
@app.route('/catalog/JSON/')
def catalogJSON():
    catalog = session.query(Catalog).all()
    return jsonify(catalog=[i.serialize for i in catalog])

# Making a JSON API Endpoint (GET Request) for items in category
@app.route('/catalog/<int:catalog_id>/items/JSON/')
def CatalogItemsJSON(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(CatalogItem).filter_by(catalog_id=catalog.id).all()
    return jsonify(CatalogItems = [i.serialize for i in items])


#    This is the main page of the Catalog
@app.route('/')
@app.route('/catalog/',methods=['GET','POST'])
def showCatalog():
    catalog = session.query(Catalog).all()
    if 'username' not in login_session:
        return render_template('publiccat.html', catalog = catalog)
    else:
        return render_template('catalog.html', catalog = catalog)

# This is to add a category to the catalog
@app.route('/catalog/new/',methods=['GET','POST'])
def newCatalog():
    catalog = session.query(Catalog).all()
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        if request.form['name']:
            newCat = Catalog(name = request.form['name'], user_id = login_session['user_id'])
            
            session.add(newCat)
            session.commit()
            flash("New catalog category created!")
            return redirect(url_for('showCatalog', catalog = catalog))
        else:
            flash("Name needed!")
            return render_template('newCatalog.html', catalog = catalog) 
    else:
        return render_template('newCatalog.html', catalog = catalog)


# This is to edit a category in the catalog
@app.route('/catalog/<int:catalog_id>/edit/',methods=['GET','POST'])
def editCatalog(catalog_id):
    if 'username' not in login_session:
        return redirect('/login')

    updateCatalog = session.query(Catalog).filter_by(id=catalog_id).one() 
    if updateCatalog.user_id != login_session['user_id']:
        return '''
                <script>function myFunction() {alert('You are not authorized to edit this restaurant.
               Please create your own restaurant in order to edit.');}</script><body onload='myFunction()''>
               '''
    if request.method == 'POST':
        if request.form['name']:
            updateCatalog.name = request.form['name']
            updateCatalog.user_id = login_session['user_id']  

            session.add(updateCatalog)
            session.commit()
            flash("Catalog successfully updated!")
            return redirect(url_for('showCatalog'))
    else:
        return render_template('editCatalog.html', catalog = updateCatalog)


# This shows all the items in the catalog under catagory
@app.route('/catalog/<int:catalog_id>/',methods=['GET','POST'])
@app.route('/catalog/<int:catalog_id>/items/',methods=['GET','POST'])
def showItems(catalog_id):
    catalog = session.query(Catalog).all()
    if catalog == []:
        return render_template('newitem.html', catalog_id = catalog_id)
    
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    creator = getUserInfo(catalog.user_id)
    items = session.query(CatalogItem).filter_by(catalog_id=catalog.id).all() 
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicitems.html', catalog = catalog, items = items, creator=creator)
    else:
        return  render_template('Items.html', catalog = catalog, items = items)
  
@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/',methods=['GET','POST'])
def showItemDesc(catalog_id, item_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()  
    Items = session.query(CatalogItem).filter_by(id=item_id).one()
    creator = getUserInfo(catalog.user_id)
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('PublicItemDesc.html', catalog_id = catalog_id, item_id = item_id, i = Items)
    else:
        return render_template('ItemDesc.html', catalog_id = catalog_id, item_id = item_id, i = Items)

@app.route('/catalog/<int:catalog_id>/items/new/',methods=['GET','POST'])
def newItem(catalog_id):
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
 
    if login_session['user_id'] != catalog.user_id:
                                               
        return '''<script>function myFunction() {alert('You are not authorized to add items to this catalog.');}
                  </script><body onload='myFunction()''>
               '''
    if request.method == 'POST':
        if request.form['name'] == []:
            flash("Name needed!")
            return render_template('newitem.html', catalog_id = catalog_id)  
        newItem = CatalogItem(name = request.form['name'])
        newItem.description = request.form['description']
        newItem.price = request.form['price']
        newItem.catalog_id = catalog_id
        newItem.user_id = catalog.user_id

        session.add(newItem)
        session.commit()
  
        flash("New item created!")
        items = session.query(CatalogItem).filter_by(catalog_id=catalog_id).all()
        return  render_template('Items.html', catalog = catalog, items = items)
       
    else:
        return render_template('newitem.html', catalog_id = catalog_id)  

# This edits an item under the catagory in the catalog  
@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/edit/',methods=['GET','POST'])
def editItem(catalog_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).all()
    category = session.query(Catalog).filter_by(id=catalog_id).one() 
    editedItem = session.query(CatalogItem).filter_by(id=item_id).one()
    if editedItem.user_id != category.user_id:
        return '''
                <script>function myFunction() {alert('You are not authorized to edit this item.');}
                </script><body onload='myFunction()''>
               '''
    if request.method == 'POST':
        if request.form['name']:
          editedItem.name = request.form['name']
        else:
          flash("Name needed!")
          return render_template('edititem.html', catalog_id = catalog_id, item_id = item_id, i = editedItem, c = category, catalog = catalog)

        if request.form['description']:
          editedItem.description = request.form['description']
        if request.form['price']:
          editedItem.price = request.form['price']
        if request.form['category']:
          editedItem.catalog_id = request.form['category']
          print editedItem.catalog_id
        editedItem.user_id = category.user_id
        print editedItem.user_id 
        session.add(editedItem)
        session.commit()
        flash("Item successfully updated!")
        return redirect(url_for('showItems', catalog_id = catalog_id))
 
    else:
        return render_template('edititem.html', catalog_id = catalog_id, item_id = item_id,
                i = editedItem, c = category, catalog = catalog)
            

# This deletes an item under the catagory in the catalog
@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/delete/',methods=['GET','POST'])
def deleteItem(catalog_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()  
    deleteItem = session.query(CatalogItem).filter_by(id=item_id).one()
    if login_session['user_id'] != catalog.user_id:
        return '''<script>function myFunction() {alert('You are not authorized to add items to this catalog.');}
                  </script><body onload='myFunction()''>
               '''
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash("Item successfully deleted!")
        return redirect(url_for('showItems', catalog_id = catalog_id))
    else:
        return render_template('deleteItem.html', catalog_id = catalog_id, item_id = item_id, i = deleteItem)

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showRCatalog'))

 
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
