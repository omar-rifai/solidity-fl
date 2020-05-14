@echo on
call truffle compile
echo "Smart contracts compiled"
call truffle migrate
echo "Smart contracts migrated"
echo "Will now start server"
call flask run