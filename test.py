from unittest import TestCase
from app import app, handle_data
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_homepage(self):
        print('Testing homepage')
        with self.client:
            response = self.client.get('/')
            html = response.get_data(as_text=True)
            
            self.assertIn('board', session)
            self.assertIs(session['highscore'], None)
            self.assertIs(session['times-played'], None)
            self.assertIn('<div id="highscore">', html)
            self.assertIn('<div class="scores">', html)
            self.assertIn('<div id="timer">', html)
        
    def test_valid_words(self):
        print('Testing valid words')
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['P','A','R','T','Y'], 
                                 ['P','A','R','T','Y'], 
                                 ['P','A','R','T','Y'], 
                                 ['P','A','R','T','Y'], 
                                 ['P','A','R','T','Y']]
            response = client.get('/check-word?word=party')
            self.assertEqual(response.json['result'], 'ok')
    
    def test_not_on_board(self):
        print('Testing not on board')
        self.client.get('/')
        response = self.client.get('/check-word?word=inconsequentially')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_not_a_word(self):
        print('Testing not a word')
        self.client.get('/')
        response = self.client.get('/check-word?word=abc')
        self.assertEqual(response.json['result'], 'not-word')


            
