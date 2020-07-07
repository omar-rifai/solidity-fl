# solidity-fl


This is a prototype for running a federated learning algorithm using an Ethereum Smart Contract. The prototype has been implemented using the truffle suite and a Python Flask backend server for simulations.

You can use the intialization script by running launch_app.sh. Otherwise, you can manually start the different processes as follows.

Install the node dependencies both in the main folder and in the client folder by running (once for each):

> npm install 

In the main directory, to start the python backend server call:
> pip install requirements.txt

> flask run

Then, run a developpement blockchain using truffle:
> truffle develop 

In a seperate terminal deploy the smart contracts:

>truffle compile; truffle migrate

Finally, to run the react-based client, in the client folder:

> npm start 

##Requirements

This code has been tested with Node version 12.16.1

Make sure that a mongodb service is running in the background


