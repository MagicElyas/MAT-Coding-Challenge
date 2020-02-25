echo Welcome to the McLaren Applied Technologies Fan Engagement Application! Wait a little while we set up all the dependencies
docker-compose pull
pip3 install pipenv
cd apps/fan_engagement
pipenv install
docker-compose stop
docker-compose up -d
echo All set! Launching application, now you can go to localhost:8084 and start watching the cars go around 
pipenv run python3 main.py
