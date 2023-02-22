import os
import unittest
import json

from flaskr import create_app
from models import Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:111@localhost/trivia_test"
        })
        self.client = self.app.test_client
        
        self.new_question = {
            'question': 'Who discovered penicillin?',
            'answer': 'Alexander Fleming',
            'difficulty': 2,
            'category': 1
        }

        self.new_quizzes = {
            'previous_questions': [],
            'quiz_category': {
            'id': 5, 
            'type': 'entertainment'}
        }



    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_categories_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_categories_failure(self):
        # Empty the categories table to simulate failure scenario
        with self.app.app_context():
            Category.query.delete()
            res = self.client().get('/categories')
            data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_delete_question_success(self):
        # Create a test question to delete
        with self.app.app_context():
            question = Question(question='Test question', answer='Test answer', category=1, difficulty=1)
            question.insert()
            question_id = question.id

        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        # Check response status code and success value
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # Check that the question was deleted
        self.assertEqual(data['deleted'], question_id)

    def test_delete_question_failure(self):
        # Try to delete a question that doesn't exist
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_retrieve_questions_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertIsNone(data['current_category'])

    def test_retrieve_questions_failure(self):
        # Delete all questions from the database to simulate failure scenario
        with self.app.app_context():
            Question.query.delete()
            res = self.client().get('/questions')
            data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_question_success(self):
        with self.app.app_context():
            new_question = {
                'question': 'What is the capital of France?',
                'answer': 'Paris',
                'category': 3,
                'difficulty': 2
            }
            res = self.client().post('/questions', json=new_question)
            data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

    def test_create_question_failure(self):
        with self.app.app_context():
            new_question = {
                'question': 'What is the capital of France?',
                'answer': 'Paris',
                'difficulty': 2
            }
            res = self.client().post('/questions', json=new_question)
            data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_search_questions(self):
        """Test searching for questions by a search term"""
        search_term = 'title'
        res = self.client().post('/questions/search', json={'searchTerm': search_term})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['questions']), 0)

    def test_search_questions_no_results(self):
        """Test searching for questions with a search term that yields no results"""
        search_term = 'nonexistent'
        res = self.client().post('/questions/search', json={'searchTerm': search_term})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_questions_by_category_success(self):
        category_id = 1
        res = self.client().get(f'/categories/{category_id}/questions')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(data['total_questions'], 0)
        self.assertEqual(data['current_category'], 'Science')

    def test_get_questions_by_category_failure(self):
        category_id = 1000
        res = self.client().get(f'/categories/{category_id}/questions')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
    
    def test_get_questions_to_play_quiz(self):
        res = self.client().post('/quizzes', json = self.new_quizzes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    #failed test
    def test_422_no_questions_to_play_quiz(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
