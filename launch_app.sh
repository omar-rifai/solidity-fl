#!/bin/bash
pip install requirements
npm install
truffle develop &
truffle compile
truffle migrate
flask run &
cd client 
npm install 
npm start

