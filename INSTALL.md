#Instructions
To get this running you just need to put the contents of the blog directory in the /opt/flask_blog directory.  You will need mysql running and import the SPU tables.  You can use the docker mariadb image or the centos image or a combination of both running within the docker vm.  As long as the db is accessible to the app server it should not matter how you configure your docker image.  Take a look at settings.py.

you will need python, setup_tools, and pip on your app server.
The db will need mysql and utilities.

I'll get to work on a build script.

**Where you extracted the SPU_BLOG directory**  
  
the location of the extracted SOU_BLOG on the lcoal drive

```bash  
DIRECTORY_FOR_flask_blog = ''
```
you have to enter the docker vm from the command line on each shell before you cann attach to or start the docker images.
**to list the vm's**
```bash  
docker-machine ls
```

machine_name = ''  
To connect the shell to the vm  
```bash  
eval "$(docker-machine env $machine_name)"
```
your machine name is probably default 

###Build Process  
```bash  
docker build -t flask_blog .
docker run --name db -e MYSQL_ROOT_PASSWORD=test -d -p 3306:3306 mariadb
docker run -d -p 5000:5000 -v $DIRECTORY_FOR_flask_blog/:/opt/flask-blog --name web --link db:mysql flask-intro-mysql
```  
**from a seperate shell**    
```bash  
docker run --name mysql-client -it --link db:mysql --rm mariadb sh -c 'exec mysql -uroot -ptest -hmysql'
```  
**from app server**
```bash  
pip install -r requirements.txt
python dbinit.py
python tests.py
python manage.py runserver
```  
**If you are running in docker don't forget the docker IP is what serves the web, not localhost.**  

##Troubleshooting
```bash  
python manage.py shell
```  
That should work
####server routes  
host:5000/login  
host:5000/setup  
host:5000/post  
host:5000/admin  
host:5000/index  
host:5000/register
host:5000/  
