# Web scraping application on Django (scraping Git-Hub repository commits)
##### PostgreSQL Database integration
## Using Redis, Celery, BS4, Asyncio, Aiohttp, PostgreSQL, DjangoREST framework

## To run this application.
##### Clone the repository
```
$ git clone https://github.com/stillnurs/git_parser/
```

##### Activate virtual environment and
##### install required dependencies from requirements.txt using pip

```
$ pip install -r requirements.txt
```

##### Migrate django and Celery models
```
$ python manage.py makemigrations
$ python manage.py migrate
```

##### Run redis server 
```
$ redis-server
```

##### Run Celery worker
```
$ celery -A git_parser worker -l info
```

##### Fire up the Celery beat
```
$ celer -A git_parser beat -l info
```

##### Add Django superuser and run Django server to add Repositories in admin panel
```
$ python manage.py createsuperuser
$ python manage.py runserver
```

### By default Celery scheduled to parse commits every 10-15 seconds,
### but you can change it to any schedule you like from admin panel or celery.py file.
