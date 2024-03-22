# Event-management-system

Download the Xammp server, and start both apach and mysql services. click on Admin in mysql which will take you to the localhost of phpmyadmin in the browser.

Download VisualStudio and Python, Clone the Repository "git clone https://github.com/techwithradhika/Event-management-system.git" in terminal from VSC.

In terminal navigate to the current folder and install virtual environment "pip install virtualenv", Create new VENV "python -m virtualenv venv", 
Activate the VENV ".\venv\Scripts\activate" and also install the dependencies using pip "pip install mysql-connector-python requests fastapi sqlalchemy pydantic uvicorn".

Now first to create the events table to store the data in database, open file "table.py" and replace the hostname, username and password with your credentials.
and run the table python file in terminal by entering "python table.py".
after successful running of the pyhon file check if the database "events_database" is created with the table "events" in the localhost.

now open the "insert_data.py" python file and replace "events.csv" with your CSV dataset file path
and run the python file "python insert_data.py" and then verify that the data is inserted into the table.

Now run the app.py python file by entering "uvicorn api:app --reload" in terminal which will start the Fastapi Application.
In the browser open the link "http://127.0.0.1:8000/docs"  It allows you to interact with the API request.
Now you can get the data in the response body at "Get/api/events/find" by entering latitude, longitude, date, and page number.
