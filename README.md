# solidity-fl


This is a prototype for running a federated learning algorithm using an Ethereum Smart Contract. The prototype has been implemented using the truffle suite and a Python Flask backend server for simulations.

For client side libraries installation go to the client folder and type

> npm install 

After installing the required dependencies specified above, call inside the client directory:

> npm start 

In the main directory, to start the python backend server call:

> flask run

For running a developpement blockchain call:
> truffle develop 

Then, in a seperate terminal for deploying the smart contracts:

>truffle compile; truffle migrate

##Requirements

This code has been tested with Node version 12.16.1
Make sure that a mongodb service is running in the background


