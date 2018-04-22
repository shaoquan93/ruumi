# Ruumi web app

This is the Ruumi webapp made with Python Flask application.

Set up ur Hyperledger Blockchain with the .bna file provided and start the rest server that is serving at localhost:3000

### Setting up Hyperledger Blockchain
Navigate to ~/composer-playground on the Vagrant Virtual Machine Cloud IDE and issue the following command:
```
./playground.sh up
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
Enrollment ID: <user id>
Enrollment secret: <password returned from CA>
Once the business network is created(this can take a few minutes), you will be moved to the network editor screen.
At this point, the business network is ready to be used.
  
### Starting REST server
Enter into the CLI container and start the REST server using:
composer-rest-server -c <admin card>
This will start the REST server on port 3000, which can be viewed in the browser.

### Prerequisites
```
pip install -r requirements.txt
```
### Launch the flask webapp
```
python main.py
```

