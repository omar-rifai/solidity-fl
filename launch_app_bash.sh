#!/bin/bash
set echo on
#start ganache-cli -a 10 -p 7545 -l 0x9C8217DC60
cd scripts
start run_server.sh
start run_client.sh
set echo off
