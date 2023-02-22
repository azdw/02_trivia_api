# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET /categories
General: Returns a list of categories
Sample: curl http://127.0.0.1:5000/categories
Response:

{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}


GET /questions
General: Returns a list of questions, number of total questions, current category, and categories
Sample: curl http://127.0.0.1:5000/questions
Response:
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    ...
  ],
  "success": true,
  "total_questions": 19
}

DELETE /questions/{question_id}
General: Deletes the question with the given ID
Sample: curl -X DELETE http://127.0.0.1:5000/questions/5
Response:
{
  "deleted": 5,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 1,
      "question": "What is the heaviest organ in the human body?"
    },
    ...
  ],
  "success": true,
  "total_questions": 18
}

POST /questions
General: Adds a new question
Sample: curl -X POST -H "Content-Type: application/json" -d '{"question": "New question?", "answer": "New answer.", "category": "2", "difficulty": "2"}' http://127.0.0.1:5000/questions
Response:
{
  "created": 20,
  "success": true
}


POST /questions/search
General: Searches for questions that match the search term
Sample: curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}' http://127.0.0.1:5000/questions/search
Response:
{
  "questions": [
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 16,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 1
}

GET /categories/{category_id}/questions
General: Returns a list of questions that belong to the given category
Sample: curl http://127.0.0.1:5000/categories/2/questions
Response:
{
  "success": true,
  "questions": [
    {
      "id": 10,
      "question": "Which actor played the character of Harry Potter in the film series?",
      "answer": "Daniel Radcliffe",
      "difficulty": 2,
      "category": 5
    },
    {
      "id": 11,
      "question": "What is the name of the big river in Egypt?",
      "answer": "Nile",
      "difficulty": 2,
      "category": 2
    }
  ],
  "total_questions": 2,
  "current_category": "Art"
}



POST /quizzes

General:
This endpoint is used to get questions to play the quiz. It takes category and previous question parameters and returns a random question within the given category if provided and that is not one of the previous questions.

Example Request:
curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [15, 16], "quiz_category": {"type": "Art", "id": 2}}' http://127.0.0.1:5000/quizzes

Example Response:
{
"success": true,
"question": {
"id": 17,
"question": "What is the name of the famous sculpture by Michelangelo depicting the biblical figure David?",
"answer": "David",
"difficulty": 2,
"category": "Art"
}
}


```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
