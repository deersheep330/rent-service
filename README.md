# Rent Service

#### local run
```
sudo apt install python-is-python3

./wait-for-it.sh localhost:3306

python -m venv .
source bin/activate

pip install -r requirements.txt

docker run -it --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=admin -e MYSQL_DATABASE=mydb -d -t mysql:8.0.23
# db connection url = root:admin@127.0.0.1:3306/mydb
```
python -m venv .
cd Scripts
activate.bat
cd ..

docker run -it --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=admin -e MYSQL_DATABASE=mydb -d -t mysql:8.0.23
# db connection url = root:admin@localhost:3306/mydb

docker run --name adminer --link mysql:mydb -p 7890:8080 -d adminer
# can login to console only after mysql initialized

export NAME=VALUE
export DB_CONNECTION_URL="root:admin@$(hostname -I | tr -d "[:blank:]"):3306/mydb"

```

##### start mysql
```
docker run -it --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=admin -e MYSQL_DATABASE=mydb -d -t mysql:8.0.23
```

##### start adminer
```
docker run --name adminer --link mysql:mydb -p 7890:8080 -d adminer
```

##### git flow
```
git checkout -b <branch>
git add .
git commit -m "<message>"
git push origin <branch>
hub pull-request -m "<message>"
git checkout master
git merge <pull-request-url>
git push origin master
git branch -d <branch>
git push origin :<branch>
git remote update -p ?
```