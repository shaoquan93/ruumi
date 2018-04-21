from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import requests
import dateutil.parser
import numpy as np
from datetime import datetime, timedelta
from random import randint
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(12)

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
		if session.get('message'):
			return render_template('index.html', message=session['message'], type=session['type'])
		else:
			return render_template('index.html')
	elif session.get('type') == 'host':
		return redirect('/host/')
	else: #guest login
		return redirect('/guest/')
 
@app.route('/login/', methods=['POST'])
def do_login():
	session['type'] = request.form['type']
	if session['type'] == 'host':
		hosts = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.SpaceOwner').json()
		user = [host for host in hosts if host['Email'] == request.form['username']]
	else:
		guests = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.SpaceFinder').json()
		user = [guest for guest in guests if guest['Email'] == request.form['username']]
	if user: 
		session['username'] = request.form['username']
		session['logged_in'] = True
		session['picture'] = str(user[0]['picture']) + '.png'
		session.pop('message', None)
	else:
		session['message'] = "wrong username or password"
	return redirect('/')


@app.route('/logout')
def logout():
   session.pop('username', None)
   session.pop('logged_in', None)
   session.pop('picture', None)
   return redirect('/')

# ALL THE HOST SITES
@app.route('/host/')
def host_index():
	if session.get('logged_in'):
		properties = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property').json()
		properties = [x for x in properties if x['owner'][35:] == session["username"]]
		return render_template('host_index.html', picture=session['picture'], properties=properties)
	return redirect('/') 

@app.route('/myspaces/')
def myspaces():
	if session.get('logged_in'):
		properties = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property').json()
		properties = [x for x in properties if x['owner'][35:] == session["username"]]
		return render_template('myspaces.html', picture=session['picture'], properties=properties, title="My Spaces", subtitle="My Spaces")
	return redirect('/')

@app.route('/addProperty/', methods=['GET', 'POST'])
def addProperty():
	if session.get('logged_in'):
		return render_template("addProperty.html", picture=session['picture'])
	return redirect('/')

@app.route('/addingProperty/', methods=['GET', 'POST'])
def addingProperty():
	if session.get('logged_in'):
		if request.method == 'POST':
			propertyId = len(requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property').json()) + 1
			wifi  = "true" if request.form.get("wifi") else "false"
			electricity  = "true" if request.form.get("electricity") else "false"
			aircon  = "true" if request.form.get("aircon") else "false"
			enclosed  = "true" if request.form.get("enclosed") else "false"
			projector = "true" if request.form.get("projector") else "false"
			whiteboard  = "true" if request.form.get("whiteboard") else "false"
			fan  = "true" if request.form.get("fan") else "false"
			toilet  = "true" if request.form.get("toilet") else "false"
			parking  = "true" if request.form.get("parking") else "false"
			pantry  = "true" if request.form.get("pantry") else "false"

			picture1 = request.files['picture1']
			filename1 = str(random_with_N_digits(8))+'.png'
			cannot = os.listdir("static/uploads/")
			while filename1 in cannot:
				filename1 = str(random_with_N_digits(8))+'.png'
			picture1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

			picture2 = request.files['picture2']
			filename2 = str(random_with_N_digits(8))+'.png'
			cannot.append(filename1)
			while filename2 in cannot:
				filename2 = str(random_with_N_digits(8))+'.png'
			picture2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))

			picture3 = request.files['picture3']
			filename3 = str(random_with_N_digits(8))+'.png'
			cannot.append(filename2)
			while filename3 in cannot:
				filename3 = str(random_with_N_digits(8))+'.png'
			picture3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

			json_val = {
			  	"$class": "org.acme.ruumi.Property",
			  	"propertyId": str(propertyId),
			  	"verified": "false",
			  	"Name": request.form.get("name", ""),
			  	"Description": request.form.get("description", ""),
			  	"picture1": filename1[:-4],
			 	"picture2": filename2[:-4],
			  	"picture3": filename3[:-4],
			  	"Address": request.form.get("address", ""),
			  	"Size": int(request.form.get("size", "")),
			  	"Price": int(request.form.get("price", "")),
			  	"wifi": wifi,
			  	"electricity": electricity,
			  	"aircon": aircon,
			  	"enclosed": enclosed,
			  	"projector": projector,
			  	"whiteboard": whiteboard,
			  	"fan": fan,
			  	"toilet": toilet,
			  	"parking": parking,
			  	"pantry": pantry,
			  	"chairs": int(request.form.get("chairs")),
			  	"tables": int(request.form.get("tables")),
			  	"owner": session["username"]
			}
			r = requests.post('http://localhost:3000/api/org.acme.ruumi.Property', data=json_val)
		return redirect("/myspaces/")
	return redirect('/')

@app.route('/myrentals/')
def myrentals():
	if session.get('logged_in'):
		rentals = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Rental').json()
		for rental in rentals:
			# # if listing is single
			# rental['listing'] = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing/'+ rental['listing'][32:]).json()
			# rental['property'] = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property/'+ rental['listing']['property'][33:]).json()

			# if listing is a list
			datetimes = []
			for listing in rental['listing']:
				l = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing/'+ listing[32:]).json()
				datetimes.append(dateutil.parser.parse(l['datestart']))
			datetimes = sorted(datetimes)
			times = sorted(list(map(lambda x: x.strftime('%H:%M'), datetimes)))
			rental['timestart'] = times[0]
			rental['duration'] = 0.5*len(times)
			rental['property'] = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property/'+ rental['listing'][0]['property'][33:]).json()
			rental['before'] = True if datetime.strptime(datetimes[-1], "%Y-%m-%dT%H:%M:%S.%fZ") < datetime.now() else False
		
		rentals = [rental for rental in rentals if rental['property']['owner'][35:] == session['username']]
		return render_template('myrentals.html', picture=session['picture'])
	else:
		return redirect('/')

@app.route('/dashboard/')
def dashboard():
	if session.get('logged_in'):
		return render_template('dashboard.html', picture=session['picture'])
	else:
		return redirect('/')

@app.route('/calendar/<propertyId>')
def calendar(propertyId):
	if session.get('logged_in'):
		properti = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property/' + propertyId)
		listings = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing').json()
		listings = [listing for listing in listings if listing['property'][33:] == properti]
		# then format em for the calendar
		return render_template('calendar.html', sub=True, picture=session['picture'], properti)
	else:
		return redirect('/')

# ALL THE GUEST SITES
@app.route('/guest/')
def guest_index():
	if session.get('logged_in'):
		listings = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing').json()
		propertiesId = list(set([x['property'][33:] for x in listings]))
		properties = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property').json()
		properties = [x for x in properties if x['propertyId']in propertiesId] 
		return render_template('guest_index.html', picture=session['picture'], properties=properties)
	else:
		return redirect('/')

@app.route('/space/<propertyId>')
def space123(propertyId):
	space = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property/' + propertyId).json()
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

@app.route('/checkout/', methods=['GET', 'POST'])
def checkout():
	if request.method == 'POST':
		space = request.form.get("space", "")
		datechoose = request.form.get("datechoose","") 
		time1 = request.form.get("time1","")
		time2 = request.form.get("time2","")
	return render_template('checkout.html', space=space, datechoose=datechoose, time1=time1, time2=time2)



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
