from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import requests
import dateutil.parser
import numpy as np
from datetime import datetime, timedelta
from random import randint
import os

app = Flask(__name__, static_url_path='/static')

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

# format time
@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%b %d, %Y'
    return native.strftime(format) 

@app.template_filter('strftime1')
def _jinja2_filter_datetime(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%H:%M'
    return native.strftime(format) 

@app.template_filter('strftime3')
def _jinja2_filter_datetime(date, fmt=None):
    date = dateutil.parser.parse(date) + timedelta(minutes=30)
    native = date.replace(tzinfo=None)
    format='%H:%M'
    return native.strftime(format) 

@app.route('/')
def index():
    if not session.get('logged_in'):
      return render_template('index.html')
    elif session.get('type') == 'host':
      return redirect('/host/')
    else: #guest login
      return redirect('/guest/')
 
@app.route('/login/', methods=['POST'])
def do_login():
  if request.form['type'] == 'host':
    if request.form['password'] == 'password' and request.form['username'] == 'tania@gmail.com':
      session['logged_in'] = True
      session['type'] = 'host'
      return redirect('/host/')
    else:
      # better to pop up a msg to say password is wrong and open the login form
      return redirect('/')
  elif request.form['type'] == 'guest':
    if request.form['password'] == 'password' and request.form['username'] == 'alok@gmail.com':
      session['logged_in'] = True
      session['type'] = 'guest'
      return redirect('/guest/')
    else:
      # better to pop up a msg to say password is wrong and open the login form
      return redirect('/')
    return redirect('/')

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   # session.pop('username', None)
   session['logged_in'] = False
   return redirect('/')

@app.route('/guest/')
def guest_index():
    return render_template('guest_index.html')

@app.route('/host/')
def host_index():
    return render_template('host_index.html')

@app.route('/space123/')
def space123():
    space = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property/1').json()
    propertyId = "resource:org.acme.ruumi.Property#1"
    listings = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing/').json()
    chosens = [listing for listing in listings if listing['property'] == propertyId]

    datetimes = [dateutil.parser.parse(chosen['datestart']) for chosen in chosens]

    dates = sorted(list(set(map(lambda x: x.strftime('%m/%d/%Y'), datetimes)))) 
    dates = [dateN for dateN in dates if datetime.strptime(dateN, "%m/%d/%Y") >=  datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)]
    start = dates[0]
    end = dates[-1]

    # datesNotAvailable = [] # see from start to end when dun have

    dateWtime = {}
    for x in datetimes:
        dt = x.strftime('%m/%d/%Y')
        if dt in dateWtime.keys():
            dateWtime[dt].append(x.strftime('%H:%M'))
        else:
            dateWtime[dt] = [x.strftime('%H:%M')]

    stime = sorted(dateWtime['04/11/2018'])

    return render_template('single.html', space=space, start=start, end=end, dateWtime = dateWtime, stime=stime)


@app.route('/submitReview/<rentalID>', methods=['GET', 'POST'])
def submitReview(rentalID):
    return render_template('review.html', rentalID = rentalID)

@app.route('/addReview/<rentalID>', methods=['GET', 'POST'])
def addReview(rentalID):
    if request.method == "POST":
        json_val = {
          "$class": "org.acme.ruumi.reviewRental",
          "rental": rentalID,
          "reviewsid": "3807",
          "review": request.form.get("review", ""),
          "wifi": "true",
          "electricity": "true",
          "aircon": "true",
          "enclosed": "true",
          "projector": "true",
          "whiteboard": "true",
          "fan": "true",
          "toilet": "true",
          "parking": "true",
          "pantry": "true",
          "Rating": 4,
          "chairs": 5,
          "tables": 5
        }
        # rentals = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Rental/5432').json() 
        # r = requests.post('')
        r = requests.post('http://localhost:3000/api/org.acme.ruumi.reviewRental', data=json_val)
    # return jsonify(json_val)
    return redirect("/myaccount/")



@app.route('/addProperty/', methods=['GET', 'POST'])
def addProperty():
    return render_template("addProperty.html")

@app.route('/checkout/', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        space = request.form.get("space", "")
        datechoose = request.form.get("datechoose","") 
        time1 = request.form.get("time1","")
        time2 = request.form.get("time2","")
    return render_template('checkout.html', space=space, datechoose=datechoose, time1=time1, time2=time2)

@app.route('/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        if request.form.get("projector"):
            projector = "true"
        else:
            projector = "false"
        json_val = {
          "$class": "org.acme.ruumi.Property",
          "propertyId": "6",
          "verified": "false",
          "Name": request.form.get("name", ""),
          "Description": request.form.get("description", ""),
          "picture1": random_with_N_digits(8),
          "picture2": random_with_N_digits(8),
          "picture3": random_with_N_digits(8),
          "Address": request.form.get("address", ""),
          "Size": int(request.form.get("size", "")),
          "wifi": "true",
          "electricity": "true",
          "aircon": "true",
          "enclosed": "true",
          "projector": "false",
          "whiteboard": "false",
          "fan": "false",
          "toilet": "false",
          "parking": "false",
          "pantry": "false",
          "chairs": int(request.form.get("chairs", "")),
          "tables": int(request.form.get("tables", "")),
          "owner": "tania@gmail.com"
        }

        r = requests.post('http://localhost:3000/api/org.acme.ruumi.Property', data=json_val)
    return redirect("/myspaces/")

@app.route('/done/', methods=['GET', 'POST'])
def done():
    if request.method == 'POST':
        space = request.form.get("space", "")
        datechoose = request.form.get("datechoose","") 
        time1 = request.form.get("time1","")
        time2 = request.form.get("time2","")

        dateNew = datetime.strptime(datechoose, "%m/%d/%Y").strftime('%Y-%m-%d')
        startTime = dateNew+"T"+time1+":00.000Z"
        endTime = dateNew+"T"+time2+":00.000Z"

        nowt = datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S.%fZ")
        # time_endTime = datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S.%fZ")
        # nowt += timedelta(minutes=30)
        
        listings = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing/').json()

        for listing in listings:
            if listing['datestart'] == startTime:
                chosen = listing
                break;

        json_val = {
          "$class": "org.acme.ruumi.rentListing",
          "spacefinder": 'alok@gmail.com',
          "listing": chosen['listingID'],
          "rentalid": str(random_with_N_digits(4)),
        }

        r = requests.post('http://localhost:3000/api/org.acme.ruumi.rentListing', data=json_val)
        # then update listing for all the times
    return render_template('done.html')

@app.route('/myrentals/')
def account():
    return render_template('myacc.html')

@app.route('/myspaces/')
def myspaces():
    r = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property') 
    if r.json()==None or r.json()=={}:
        properties = {}
    else:
        properties = r.json()
    return render_template('myplaces.html', title="My Spaces", subtitle="My Spaces", properties=properties)

@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/space123calendar/')
def calendar():
    return render_template('calendar.html', sub=True)

@app.route('/myaccount/')
def myaccount():
    rentals = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Rental').json() 
    listings = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing').json() 
    properties = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property').json() 
    for rental in rentals:
        for listing in listings:
            if rental['listing'] == "resource:org.acme.ruumi.Listing#" + listing['listingID']:
                rental['listing'] = listing
                for propertie in properties:
                    if rental['listing']['property'] == "resource:org.acme.ruumi.Property#" + propertie['propertyId']:
                        rental['listing']['property'] = propertie
                        break
                break
        rental['past'] = datetime.strptime(rental['listing']['datestart'], "%Y-%m-%dT%H:%M:%S.%fZ") < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    return render_template('guest_acc.html', rentals=rentals)

if __name__ == '__main__':
  app.secret_key = os.urandom(12)
  app.run(debug=True, host='127.0.0.1', port=5000)
