from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session, flash

app = Flask(__name__)
app.config["SECRET_KEY"] = "something-secret"

boggle_game = Boggle()

@app.route('/')
def show_board():
    """Makes game board and saves it to the session storage"""
    board = boggle_game.make_board()
    session['board'] = board
    session['highscore'] = None
    session['times-played'] = None
    
    return render_template('base.html', board=board)

@app.route('/check-word')
def check_word():
    """Accepts a parameter of 'score' and passes it to 'check_valid_word', returns a result"""
    word = request.args['word']
    result = boggle_game.check_valid_word(session['board'], word)

    if result == "ok":
        return jsonify({"result": f"{result}"})
    else:
        return jsonify({"result": f"{result}"})
    
@app.route('/game-stats', methods=["POST"])
def store_stats():
    """Post route calls handle_data"""
    handle_data(request.json['score'])

    return jsonify({"highscore": f"{session['highscore']}"})

def handle_data(score):
    """Checks for session['times-played'] and increments appropriately"""

    if session['times-played']:
        session['times-played'] += 1
    else:
        session['times-played'] = 1 
    
    if session['highscore']:
        if score > session['highscore']:
            session['highscore'] = score
    else:
        session['highscore'] = score
    return session['highscore']

@app.route('/data')
def return_data():
    return jsonify(session)

