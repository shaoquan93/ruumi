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
		session['ID'] = user[0]['ID']
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
   session.pop('ID', None)
   session.pop('type', None)
   return redirect('/')

# ALL THE HOST SITES
@app.route('/host/')
def host_index():
	if session.get('logged_in') and session['type'] == 'host':
		properties = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property').json()
		properties = [x for x in properties if x['owner'][35:] == session["ID"]]
		return render_template('host_index.html', picture=session['picture'], properties=properties)
	return redirect('/') 

@app.route('/myspaces/')
def myspaces():
	if session.get('logged_in') and session['type'] == 'host':
		properties = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property').json()
		properties = [x for x in properties if x['owner'][35:] == session["ID"]]
		return render_template('myspaces.html', picture=session['picture'], properties=properties, title="My Spaces", subtitle="My Spaces")
	return redirect('/')

@app.route('/addProperty/', methods=['GET', 'POST'])
def addProperty():
	if session.get('logged_in') and session['type'] == 'host':
		return render_template("addProperty.html", picture=session['picture'])
	return redirect('/')

@app.route('/addingProperty/', methods=['GET', 'POST'])
def addingProperty():
	if session.get('logged_in') and session['type'] == 'host':
		if request.method == 'POST':
			# come up with property id 
			propertyId = str(random_with_N_digits(4))
			properties = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property').json()
			p = [properti['propertyId']for properti in properties]
			while propertyId in p:
				propertyId = str(random_with_N_digits(4))

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
			picture3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))

			verificationpic = request.files['verificationpic']
			filename4 = str(random_with_N_digits(8))+'.png'
			cannot.append(filename3)
			while filename4 in cannot:
				filename4 = str(random_with_N_digits(8))+'.png'
			verificationpic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename4))

			json_val = {
			  	"$class": "org.acme.ruumi.Property",
			  	"propertyId": propertyId,
			  	"verified": "false",
			  	"Name": request.form.get("name", ""),
			  	"Description": request.form.get("description", ""),
			  	"picture1": int(filename1[:-4]),
			 	"picture2": int(filename2[:-4]),
			  	"picture3": int(filename3[:-4]),
			  	"Address": request.form.get("address", ""),
			  	"Size": int(request.form.get("size", "")),
			  	"price": int(request.form.get("price", "")),
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
			  	"owner": "resource:org.acme.ruumi.SpaceOwner#" + session['ID'],
			  	"verificationpic": int(filename4[:-4])
			}
			r = requests.post('http://localhost:3000/api/org.acme.ruumi.Property', data=json_val)
		return redirect("/myspaces/")
	return redirect('/')

@app.route('/editProperty/<propertyId>', methods=['GET', 'POST'])
def editProperty(propertyId):
	properti = requests.get('http://localhost:3000/api/org.acme.ruumi.Property/' + propertyId).json()
	return render_template('editProperty.html', properti=properti)

@app.route('/editingProperty/<propertyId>', methods=['GET', 'POST'])
def editingProperty(propertyId):
	if session.get('logged_in') and session['type'] == 'host':
		if request.method == 'POST':
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

			json_val = {
			  "$class": "org.acme.ruumi.updateProperty",
			  "property": "resource:org.acme.ruumi.Property#"+ propertyId,
			  "newDescription": request.form.get("description", ""),
			  "newpicture1": request.form.get("picture1", ""),
			  "newpicture2": request.form.get("picture2", ""),
			  "newpicture3": request.form.get("picture3", ""),
			  "newAddress": request.form.get("address", ""),
			  "newPrice": int(request.form.get("price", "")),
			  "newSize": int(request.form.get("size", "")),
			  "newwifi": wifi,
			  "newelectricity": electricity,
			  "newaircon": aircon,
			  "newenclosed": enclosed,
			  "newprojector": projector,
			  "newwhiteboard": whiteboard,
			  "newfan": fan,
			  "newtoilet": toilet,
			  "newparking": parking,
			  "newpantry": pantry,
			  "newchair": int(request.form.get("chairs")),
			  "newtable": int(request.form.get("tables")),
			}
			r = requests.post('http://localhost:3000/api/org.acme.ruumi.updateProperty', data=json_val)
		return redirect("/myspaces/")
	return redirect('/')

@app.route('/calendar/<propertyId>', methods=['GET'])
def calendar(propertyId):
	if session.get('logged_in') and session['type'] == 'host':
		properti = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property/' + propertyId).json()

		# get all rented timing
		rentals = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Rental').json()
		listings = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing/').json()
		for rental in rentals:
			listingRental = [l for l in listings if "resource:org.acme.ruumi.Listing#" + l['listingID'] in rental['listings']]
			earliest = 0
			for i in range(len(listingRental)):
				if listingRental[i]["datestart"] < listingRental[earliest]["datestart"]:
					earliest =i 
			startListing = listingRental[earliest]
			# startListing = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing/' + rental['listings'][0][32:]).json()
			rental['propertyId'] = startListing['property'][33:]
			rental['datestart'] = startListing['datestart']
			duration = len(rental['listings']) * 0.5
			rental['dateend'] = (datetime.strptime(rental['datestart'][:-5], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=duration)).strftime("%Y-%m-%dT%H:%M:%S")
			finder = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.SpaceFinder/' + rental['finder'][36:]).json()
			rental['finder'] = finder["firstName"] + " " + finder["lastName"]
		rentals = [re for re in rentals if re['propertyId'] == propertyId]

		# get all listed timing that has yet to be rented
		listings = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing').json()
		listedall = [listing for listing in listings if listing['property'][33:] == propertyId]
		listings_false = [listing for listing in listedall if listing['rented']== False]
		listed = []
		for l in listings_false:
			listed.append({"datestart":l['datestart'][:-5], "dateend":(datetime.strptime(l['datestart'][:-5], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=0.5)).strftime("%Y-%m-%dT%H:%M:%S")})

		# get all the free timing from the next hour for 2 weeks
		decided = [datetime.strptime(l['datestart'][:-5], "%Y-%m-%dT%H:%M:%S") for l in listedall]
		Availabletimes =[] # this will contain [{start, end}]
		tNow  = datetime.now()
		# round to the next full hour
		tNow -= timedelta(minutes = tNow.minute, seconds = tNow.second, microseconds =  tNow.microsecond)
		tNow += timedelta(hours = 1)

		newstart = ""
		for i in range(210):
			if tNow.hour == 22:
				if newstart != "":
					Availabletimes.append({"datestart": newstart, "dateend": tNow.strftime("%Y-%m-%dT%H:%M:%S")})
					newstart = ""
				tNow += timedelta(hours = 9)
			elif tNow not in decided:
				if newstart == "":
					newstart = tNow.strftime("%Y-%m-%dT%H:%M:%S")
				tNow += timedelta(hours = 0.5)
			else:
				if newstart != "":
					Availabletimes.append({"datestart":newstart, "dateend":tNow.strftime("%Y-%m-%dT%H:%M:%S")})
					newstart = ""
				tNow += timedelta(hours = 0.5)

		return render_template('calendar.html', sub=True, picture=session['picture'], properti=properti, rentals=rentals, listed=listed, Availabletimes=Availabletimes)
	else:
		return redirect('/')

@app.route('/addListing/', methods=['GET', 'POST'])
def addListing():
	start = datetime.strptime(request.form.get("datestart", "")[4:-9],'%b %d %Y %H:%M:%S')
	end = datetime.strptime(request.form.get("dateend", "")[4:-9],'%b %d %Y %H:%M:%S')
	propertyId = request.form.get("space", "")
	properti = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property/' + propertyId).json()
	curr  = start
	while curr + timedelta(hours = 0.5) <= end:
		json_val = {
		  "$class": "org.acme.ruumi.Listing",
		  "listingID": str(random_with_N_digits(4)),
		  "price": properti['price'],
		  "datestart": curr.strftime("%Y-%m-%dT%H:%M:%S"),
		  "rented": "false",
		  "property": "resource:org.acme.ruumi.Property#" + propertyId
		}
		r = requests.post('http://localhost:3000/api/org.acme.ruumi.Listing', data=json_val)
		curr += timedelta(hours = 0.5)
	return redirect("/calendar/" + propertyId)

@app.route('/myrentals/')
def myrentals():
	if session.get('logged_in') and session['type'] == 'host':
		rentals = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Rental').json()
		for rental in rentals:
			datetimes = []
			for listing in rental['listings']:
				l = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing/'+ listing[32:]).json()
				datetimes.append(dateutil.parser.parse(l['datestart']))
			datetimes = sorted(datetimes)
			times = sorted(list(map(lambda x: x.strftime('%H:%M'), datetimes)))
			rental['date'] = datetimes[0].strftime('%d %b %Y')
			rental['timestart'] = times[0]
			rental['duration'] = 0.5*len(times)
			rental['propertyId'] = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing/'+ rental['listings'][0][32:]).json()['property'][33:]
			rental['property'] = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property/'+ rental['propertyId']).json()
			rental['before'] = True if datetimes[-1].replace(tzinfo=None) < datetime.now() else False
			rental['finder'] = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.SpaceFinder/'+ rental['finder'][36:]).json()
		
		rentals = [rental for rental in rentals if rental['property']['owner'][35:] == session['ID']]
		return render_template('myrentals.html', picture=session['picture'], rentals=rentals)
	else:
		return redirect('/')

@app.route('/dashboard/')
def dashboard():
	if session.get('logged_in') and session['type'] == 'host':
		return render_template('dashboard.html', picture=session['picture'])
	else:
		return redirect('/')

# ALL THE GUEST SITES
@app.route('/guest/')
def guest_index():
	if session.get('logged_in') and session['type'] == 'guest':
		listings = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing').json()
		propertiesId = list(set([x['property'][33:] for x in listings]))
		properties = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property').json()
		properties = [x for x in properties if x['propertyId'] in propertiesId] 
		return render_template('guest_index.html', picture=session['picture'], properties=properties)
	else:
		return redirect('/')

@app.route('/space/<propertyId>')
def space(propertyId):
	if session.get('logged_in') and session['type'] == 'guest':
		space = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property/' + propertyId).json()
		listings = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing/').json()
		chosens = [listing for listing in listings if listing['property'][33:] == propertyId and listing['rented']==False]

		datetimes = [dateutil.parser.parse(chosen['datestart']) for chosen in chosens]
		dates = sorted(list(set([dt.replace(hour=0, minute=0, second=0, microsecond=0) for dt in datetimes])))

		datesNotAvailable = []

		delta = dates[-1]-dates[0]
		for i in range(1, delta.days + 1):
			check = dates[0] + timedelta(days=i)
			if check not in dates:
				datesNotAvailable.append(check.strftime('%m/%d/%Y'))

		dates = sorted(list(set(map(lambda x: x.strftime('%m/%d/%Y'), datetimes)))) 
		dates = [dateN for dateN in dates if datetime.strptime(dateN, "%m/%d/%Y") >=  datetime.now()]
		start = dates[0]
		end = dates[-1]

		dateWtime = {}
		for x in datetimes:
			dt = x.strftime('%m/%d/%Y')
			if dt in dateWtime.keys():
				dateWtime[dt].append(x.strftime('%H:%M'))
			else:
				dateWtime[dt] = [x.strftime('%H:%M')]

		for k in dateWtime.keys():
			dateWtime[k] = sorted(dateWtime[k])


		reviews = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Reviews').json()
		for review in reviews:
			rental = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Rental/' + review['rental'][31:]).json()
			review['listings'] = rental['listings'] 
			review['finder'] = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.SpaceFinder/' + rental['finder'][36:]).json()
			review['propertyId'] = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing/' + review['listings'][0][32:]).json()['property'][33:]

		reviews = [r for r in reviews if r['propertyId'] == propertyId]
		return render_template('single.html', picture=session['picture'], space=space, start=start, end=end, dateWtime=dateWtime, datesNotAvailable=datesNotAvailable, reviews=reviews)
	else:
		return redirect('/')


@app.route('/checkout/', methods=['GET', 'POST'])
def checkout():
	if request.method == 'POST':
		space = request.form.get("space", "")
		spacename = request.form.get("spacename", "")
		datechoose = request.form.get("datechoose","") 
		time1 = request.form.get("time1","")
		time2 = request.form.get("time2","")
	return render_template('checkout.html', space=space, spacename=spacename, datechoose=datechoose, time1=time1, time2=time2)


@app.route('/done/', methods=['GET', 'POST'])
def done():
	if request.method == 'POST':
		space = request.form.get("space", "")
		spacename = request.form.get("spacename", "")
		datechoose = request.form.get("datechoose","") 
		time1 = request.form.get("time1","")
		time2 = request.form.get("time2","")

		dateNew = datetime.strptime(datechoose, "%m/%d/%Y").strftime('%Y-%m-%d')
		startTime = dateNew+"T"+time1+":00.000Z"
		endTime = dateNew+"T"+time2+":00.000Z"

		times = [startTime]

		nowt = datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S.%fZ")
		time_endTime = datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S.%fZ")
		nowt += timedelta(minutes=30)
		while nowt < time_endTime:
			times.append(nowt.strftime("%Y-%m-%dT%H:%M:%S.000Z"))
			nowt += timedelta(minutes=30)

		listings = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing/').json()
		chosens = [l['listingID'] for l in listings if (l['property'][33:] == space and l['datestart'] in times)]

		rentalid =  str(random_with_N_digits(4))

		json_val = {
		  "$class": "org.acme.ruumi.rentListing",
		  "spacefinder": "resource:org.acme.ruumi.SpaceFinder#" + session['ID'],
		  "listings": chosens,
		  "rentalid": rentalid,
		}

		r = requests.post('http://localhost:3000/api/org.acme.ruumi.rentListing', data=json_val)
		# then update listing for all the times
	# return jsonify(json_val)
	return render_template('done.html', space=space, spacename=spacename, datechoose=datechoose, time1=time1, time2=time2)

@app.route('/myaccount/')
def myaccount():
	rentals = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Rental').json() 
	for rental in rentals:
		startListing = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Listing/' + rental['listings'][0][32:]).json()
		rental['datestart'] = startListing['datestart']
		rental['duration'] = len(rental['listings'])*0.5
		rental['property'] = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property/' + startListing['property'][33:]).json()
		rental['past'] = datetime.strptime(startListing['datestart'], "%Y-%m-%dT%H:%M:%S.%fZ") < datetime.now()

	return render_template('guest_acc.html', rentals=rentals)

@app.route('/submitReview/<rentalID>', methods=['GET', 'POST'])
def submitReview(rentalID):
	return render_template('review.html', rentalID = rentalID)

@app.route('/addReview/<rentalID>', methods=['GET', 'POST'])
def addReview(rentalID):
	if request.method == "POST":
		json_val = {
		  "$class": "org.acme.ruumi.reviewRental",
		  "rental": "resource:org.acme.ruumi.Rental#" + rentalID,
		  "reviewsid": str(random_with_N_digits(4)),
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
		r = requests.post('http://localhost:3000/api/org.acme.ruumi.reviewRental', data=json_val)
	return redirect("/myaccount/")

@app.route('/admin')
def admin():
	hosts = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.SpaceOwner').json()
	guests = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.SpaceFinder').json()
	properties = requests.get('http://127.0.0.1:3000/api/org.acme.ruumi.Property').json()
	return render_template("admin.html", hosts=hosts, guests=guests, properties=properties)

@app.route('/verifyGuest/<ID>', methods=['GET', 'POST'])
def verifyGuest(ID):
	json_val = {
		"$class": "org.acme.ruumi.verifySpaceFinder",
  		"spacefinder": "resource:org.acme.ruumi.SpaceFinder#" + ID
	}
	requests.post('http://localhost:3000/api/org.acme.ruumi.verifySpaceFinder', data=json_val)
	return redirect("/admin")

@app.route('/verifyHost/<ID>', methods=['GET', 'POST'])
def verifyHost(ID):
	json_val = {
		"$class": "org.acme.ruumi.verifySpaceOwner",
  		"spaceowner": "resource:org.acme.ruumi.SpaceOwner#" + ID
	}
	requests.post('http://localhost:3000/api/org.acme.ruumi.verifySpaceOwner', data=json_val)
	return redirect("/admin")

@app.route('/verifyProperty/<ID>', methods=['GET', 'POST'])
def verifyProperty(ID):
	json_val = {
		"$class": "org.acme.ruumi.verifyProperty",
  		"property": "resource:org.acme.ruumi.Property#" + ID
	}
	requests.post('http://localhost:3000/api/org.acme.ruumi.verifyProperty', data=json_val)
	return redirect("/admin")


if __name__ == '__main__':
  app.secret_key = os.urandom(12)
  app.run(debug=True, host='127.0.0.1', port=5000)
