# Ruumi web app

Set up ur Hyperledger Blockchain with the .bna file provided and start the rest server that is serving at localhost:3000

### Setting up Hyperledger Blockchain
Navigate to ~/composer-playground on the Vagrant Virtual Machine Cloud IDE and issue the following command:
```
./playground.sh
```
This will start the composer playground container:

After this message is show, the composer-playground is start.

Open the playground web UI in a browserby going to http://localhost:8080

In order to create a network, a valid user credential on the certificate authority is necessary. 

Return to the cloud IDE, and exit the display of log using Ctrl-C.

Create a registrar user account on the certificate authority using the command:
```
docker exec -it ca.org1.example.com fabric-ca-client enroll -M registrar -u
http://admin:adminpw@localhost:7054
```
After which, you can use the credentials of the registrar to further create many user accounts using:
```
docker exec -it ca.org1.example.com fabric-ca-client register -M registrar -u
http://localhost:7054 --id.name <user_id> --id.affiliation org1 --id.attrs
'"hf.Registrar.Roles=client"' --id.type user
```
When the user is created, A corresponding password is also printed out.

Going back to the composer playground, to start a new business network, click on “Deploy a new business network” under the ‘hlfv1’ connection.

Upload the .bna file provided

Provide a new network admin name, and network admin card name(this will show in the composer playground registry), use one of the sample networks as a base template.

Credentials for the network admin should be created using ‘ID and Secret’ method, using the credentials:
```
Enrollment ID: <user id>
Enrollment secret: <password returned from CA>
```  
Once the business network is created(this can take a few minutes), you will be moved to the network editor screen.

At this point, the business network is ready to be used.

An admin business network card will be created as well.
  
### Starting REST server
Enter into the CLI container and start the REST server using:
```
composer-rest-server -c <admin card>
```
This will start the REST server on port 3000, which can be viewed in the browser.


### Running Ruumi App
This is the Ruumi webapp made with Python Flask application.

### General
Download and unzip this project.

Open up command prompt and navigate to the project folder.

Run the prerequisites codes to download necessary dependencies.

Lanch the flask webapp using below codes.

The app will be available on http://localhost:5000

### Prerequisites
```
pip install -r requirements.txt
```
### Launch the flask webapp
```
python main.py
```


### Testing 
Open up testing.doc

The document consist 4 main test cases:

  1. Verified Space Owners able to create Properties, Listings, Verified Space Finders able to rent listings and review listings (Successful)
  2. Unverified Space Owners unable to create new Properties. (Unsuccessful)
  3. Unverified Space Finder unable to rent listings (Unsuccessful)
  4. Space Finders who did not rent a listing unable to write a review (Unsuccessful)
  
Photos used in the test cases are provided in static/samplepics/

All the test cases can be done on the Hyperledger Composer Playground.

Successful test case can be done though the webapp. 

### Testing with Composer
On the test tab, there will be 2 participants and 4 assets.

Participants:
  1. SpaceFinder
  2. SpaceOwner
  
Assets:
  1. Listing
  2. Property
  3. Rental
  4. Reviews
  
The default ID will belong to NetworkAdmin who is granted all access.

SpaceFinder and SpaceOwner IDs can be created ID registry and by mapping them to an exisitng SpaceOwner and SpaceFinder.

### Creating Participants
Under each participants tab, NetworkAdmin can create new participant using the 'Create New Participant' button.

### Creating Assets
SpaceOwners can create:
  1. Property - through the 'Create New Asset' button
  2. Listing - through the 'Create New Asset' button
  
SpaceFinders can create:
  1. Rental - through 'RentListing' transaction
  2. Reviews - through 'ReviewRental' transaction

### Update Assets
SpaceOwner can update:
  1. Property - through 'UpdateProperty' transaction
  2. Listing - through 'updateListing' transaction

### Delete Assets
SpaceOwner can delete:
  1. Property - through delete button
  2. Listing - through delete button

### Testing with webapp
Only test case 1 (successful) can be tested via webapp.

Unsuccessful test cases are not provided interface buttons in the webapp to do the necessary actions.

Screenshots of test case 1 can be found under implementation in report.


### Accessing admin page
go to http://localhost:5000/admin
