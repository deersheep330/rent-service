# Rent Service

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
```