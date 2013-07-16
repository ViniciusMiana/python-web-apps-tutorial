To run this example, you will need to install Django and Twisted.

Run: `sudo pip install Django`  
then run: `sudo pip install Twisted`  
then you need to open 2 terminals, one opened in the app directory
to run the app and the other in the webservice directory to run the 
webserver. To run the app, run:
`python manage.py runserver`
and to run the webservice, simply run `python webservice.py` 
finally open `http://localhost:8000/` on your browser. 
The web-service is running on port 8080.
