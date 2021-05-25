# Rent Service  [![CircleCI](https://circleci.com/gh/deersheep330/rent-service.svg?style=shield)](https://app.circleci.com/pipelines/github/deersheep330/rent-service)

#### local run

(1) setup python
```
sudo apt install python-is-python3
```

(2) setup venv
```
python -m venv .
source bin/activate
```

(3) install dependencies
```
pip install -r requirements.txt
```

(4) setup test database
```
docker run -it --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=admin -e MYSQL_DATABASE=mydb -d -t mysql:8.0.23
# db connection url = root:admin@127.0.0.1:3306/mydb
./wait-for-it.sh localhost:3306
```

(5) setup adminer for test database
```
docker run --name adminer --link mysql:mydb -p 7890:8080 -d adminer
# can login to adminer console only after mysql initialized
```

(6) export db host and db connection url
```
export DB_HOST="$(hostname -I | tr -d "[:blank:]"):3306"
export DB_CONNECTION_URL="root:admin@${DB_HOST}/mydb"
```

(7) run the application with docker
```
docker build -f Dockerfile -t rent .
docker run -it -e DB_CONNECTION_URL=$DB_CONNECTION_URL rent
```

(8) test the application
```
pytest -v --junitxml=test-results/junit.xml test.py
```

(9) test the application with docker
```
docker build -f Dockerfile-test -t rent-test .
docker run -it -v "$(pwd)/test-results":/home/app/test-results -e DB_HOST="$(hostname -I | tr -d "[:blank:]"):3306" -e DB_CONNECTION_URL="root:admin@${DB_HOST}/mydb" rent-test
```