#!/bin/bash
set echo on
truffle compile
echo "Smart contracts compiled"
truffle migrate
echo "Smart contracts migrated"
echo "Will now start server"
flask run