import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from werkzeug.exceptions import HTTPException

from models import Question, Category, db


QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="postgresql://postgres:111@localhost/trivia"
    )
    
    if test_config is not None:
        app.config.from_mapping(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()
    CORS(app)

    

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
        for all available categories.
    """

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        if len(categories) == 0:
            abort(404)

        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        return jsonify({
            'success': True,
            'categories': categories_dict
        })



    """
        @TODO:
        Create an endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        This endpoint should return a list of questions,
        number of total questions, current category, categories.

        TEST: At this point, when you start the application
        you should see questions and categories generated,
        ten questions per page and pagination at the bottom of the screen for three pages.
        Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.order_by(Category.id).all()
        current_category = None

        if len(current_questions) == 0:
            abort(404)

        if request.args.get("category"):
            category_id = int(request.args.get("category"))
            current_category = Category.query.get(category_id).type
            selection = Question.query.filter_by(category=category_id).all()
            current_questions = paginate_questions(request, selection)

        return jsonify({"success": True,
                        "questions": current_questions,
                        "total_questions": len(Question.query.all()),
                        "categories": {category.id: category.type for category in categories},
                        "current_category": current_category,
                        })


    """
        @TODO:
        Create an endpoint to DELETE question using a question ID.

        TEST: When you click the trash icon next to a question, the question will be removed.
        This removal will persist in the database and when you refresh the page.
    """
    
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
            question = Question.query.get(question_id)

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })


    """
        @TODO:
        Create an endpoint to POST a new question,
        which will require the question and answer text,
        category, and difficulty score.

        TEST: When you submit a question on the "Add" tab,
        the form will clear and the question will appear at the end of the last page
        of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()

        if not ('question' in data and 'answer' in data and 'category' in data and 'difficulty' in data):
            abort(422)

        question = data['question']
        answer = data['answer']
        category = data['category']
        difficulty = data['difficulty']

        try:
            question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id,
            }), 201

        except:
            abort(422)


    """
        @TODO:
        Create a POST endpoint to get questions based on a search term.
        It should return any questions for whom the search term
        is a substring of the question.

        TEST: Search by any phrase. The questions list will update to include
        only question that include that string within their question.
        Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            body = request.get_json()
        except:
            abort(400)

        search_term = body.get('searchTerm', '')

        if search_term:
            sanitized_search_term = f'%{search_term}%'
            questions = Question.query.filter(Question.question.ilike(sanitized_search_term)).all()
            formatted_questions = [question.format() for question in questions]

            total_questions = Question.query.count()

            if len(formatted_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': total_questions
            })
        else:
            abort(400)  


    """
        @TODO:
        Create a GET endpoint to get questions based on category.

        TEST: In the "List" tab / main screen, clicking on one of the
        categories in the left column will cause only questions of that
        category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        """
        GET endpoint to get questions based on category.

        :param category_id: int, id of the category to filter by
        :return: a response containing questions that belong to the given category
        """
        category = Category.query.get(category_id)
        if category is None:
            abort(404)

        questions = Question.query.filter(Question.category == category_id).all()

        if not questions:
            abort(404)

        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(formatted_questions),
            'current_category': category.type
        })


    """
        @TODO:
        Create a POST endpoint to get questions to play the quiz.
        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.

        TEST: In the "Play" tab, after a user selects "All" or a category,
        one question at a time is displayed, the user is allowed to answer
        and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')

            if quiz_category is None:
                abort(400)

            if quiz_category['type'] == 'click':
                available_questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                available_questions = Question.query.filter_by(category=quiz_category['id']).filter(Question.id.notin_(previous_questions)).all()

            new_question = None
            if available_questions:
                new_question = random.choice(available_questions).format()

            return jsonify({
                'success': True,
                'question': new_question
            })

        except:
            abort(422)

    """
        @TODO:
        Create error handlers for all expected errors
        including 404 and 422.
    """

    # define a generic error handler to catch all exceptions
    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify({
            'success': False,
            'error': code,
            'message': str(e)
        }), code


    # define error handlers for expected errors
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "bad request"
        }), 400


    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': "unauthorized"
        }), 401


    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': "forbidden"
        }), 403


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "resource not found"
        }), 404


    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "method not allowed"
        }), 405


    @app.errorhandler(409)
    def conflict(error):
        return jsonify({
            'success': False,
            'error': 409,
            'message': "conflict"
        }), 409


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "unprocessable"
        }), 422


    @app.errorhandler(429)
    def too_many_requests(error):
        return jsonify({
            'success': False,
            'error': 429,
            'message': "too many requests"
        }), 429
    

    return app


        



