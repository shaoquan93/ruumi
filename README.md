# Ruumi web app

This is the Ruumi webapp made with Python Flask application.

Set up ur Hyperledger Blockchain with the .bna file provided and start the rest server that is serving at localhost:3000

### Setting up Hyperledger Blockchain
Navigate to ~/composer-playground on the Vagrant Virtual Machine Cloud IDE and issue the following command:
...
./playground.sh up
...
This will start the composer playground container:
After this message is show, the composer-playground is start.
Open the playground web UI in a browserby going to http://localhost:8080
In order to create a network, a valid user credential on the certificate authority is necessary. 
Return to the cloud IDE, and exit the display of log using Ctrl-C.
Create a registrar user account on the certificate authority using the command:
...
docker exec -it ca.org1.example.com fabric-ca-client enroll -M registrar -u
http://admin:adminpw@localhost:7054
...
After which, you can use the credentials of the registrar to further create many user accounts using:
...
docker exec -it ca.org1.example.com fabric-ca-client register -M registrar -u
http://localhost:7054 --id.name <user_id> --id.affiliation org1 --id.attrs
'"hf.Registrar.Roles=client"' --id.type user
...
When the user admin2 was created, A corresponding password is also printed out.


### Prerequisites
```
pip install -r requirements.txt
```
### Launch the flask webapp
```
python main.py
```

