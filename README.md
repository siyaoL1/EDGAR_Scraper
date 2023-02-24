# User Documentation
### Usage 
* Visit http://18.217.8.244:5000/ to access the frontend UI.
* There are six tabs at the top of the page:
  
  ```Home```, ```Raw Reports```, ```Generated Reports```, ```Report Generation```, ```Login```, ```Register```
* To create an account, go to ```Register``` tab to register an account in our system.
* To log into your account, go to ```Login``` tab to log into your registered account.
  * (Add the info for zoom meeting)
* To get a raw report of a company's 10K documentation, go to ```Raw Reports```, fill in the information and submit request.
* To create a customized generate report, go to ```Report Generation```. 
  * First fill in the general information for the report you want to create, and click the next step button. (Note that the report name needs to be distinct for each generated report) 
  * On the next page, pick the sheets and rows you want to include in the generated report, then submit the information.
* To get the existing generated report in the current account, go to ```Generated Reports```.
  * (Add the info for analysis)

we need to explain all of things a user can do on the frontend.

### Sphinx Documentation
The following commands will create an index.html file in docs/build/html/index.html
```bash
  cd docs
  make.bat html
```

# Developer Documentation

### Accessing Cloud Instance
* Download the scraper.pem security key

* SSH into the instance
    ```bash
    chmod 400 scraper.pem
    ssh -i "scraper.pem" ec2-user@ec2-18-217-8-244.us-east-2.compute.amazonaws.com
    ```

### Starting the Production Containers
```bash
docker-compose up --build -d
```

### Setup database
```bash
docker exec django-server python3 manage.py makemigrations
docker exec django-server python3 manage.py migrate
```

### Setup superuser
```bash
docker exec -it django-server python3 manage.py createsuperuser
```

### Running Tests

#### Starting Test Containers
```bash
docker-compose -f testing-compose.yaml build --build-arg TESTING="True"
docker-compose -f testing-compose.yaml up -d
```

#### Backend Tests
```bash
docker exec django-test-server python manage.py test
```

#### Backend Tests with coverage

```bash
docker exec django-test-server coverage run --omit venv/*,*/migrations*,*test* --source company_schema,report_schema manage.py test

docker exec django-test-server coverage report
```

#### Frontend Tests
```bash
docker exec flask-test-server pytest flask_app/test_flask_app
```

#### Frontend Tests with coverage
```bash
docker exec flask-test-server coverage run --omit venv/*,*test* -m pytest flask_app/test_flask_app.py

docker exec flask-test-server coverage report
```

### System Architecture
#### Flask Frontend Routes

* ```/```
  
  The index route, which is the welcome page for the website. It has links to navigate to the Login and Register pages.

* ```/register```
  
  The register route, which takes in a username, password, and email address from the user's input and sends a POST request to http://18.217.8.244:8000/api/users/create-user/.  Assuming a successful response is received(ie no duplicate users or network connectivity issues), there will be a user created with the given credentials and email ready for a login.

* ```/login```

  The login route, which takes in a username and password from the user's input and renders the login template, setting the username and password to their respective variables in the session object.

* ```/logout```

  The logout route which logout the current user from the session and displays a logout message when the user has logged out of their account.

* ```/raw_report```

  The raw report route which displays the form of raw reports request and allow logged-in user to retrieve new raw reports. 

* ```/generated_report```

  The generated report route which displays the generated reports for the logged-in user.  
* ```/zoom_link```

  The zoom link route which takes a user to a page where they may decide to login to their own zoom account to host a meeting
  or use the public multi-user link
  


* ```/report_generation```

  The report generation route which allows the logged-in user to create generated reports.  

Note:  Timeout errors will be the result of network and internet speeds dropping.

#### Django API Endpoints
describe what the various endpoints do

