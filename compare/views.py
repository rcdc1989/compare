from flask import render_template, request, redirect, url_for, flash, session
from . import app
from .game import *


"""
TO DO LIST:

-handle timer
-handle timed and marathon version
-fix that damn footer
-add a progress bar
-flash messages if user is about to exit
-summary page
-generate more test data
-figure out some ways to improve formatting ...how can I customize this?
"""


@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/", methods=["POST"])
@app.route("/home", methods=["POST"])
def home_post():
    
    game = Game.create_new_game()
    game.game_type = request.form["game_type"] 

    
    if game.game_type == "question_limit":
        game.question_limit = int(request.form["question_limit"])
        game.select_questions(question_limit = game.question_limit)

    elif game.game_type == "time_limit":
        game.time_limit = int(request.form["time_limit"])
        game.select_questions()
        
    elif game.game_type == "marathon":
        game.time_limit = int(request.form["time_limit"])
        game.select_questions()
    
    game.next_question()

    return redirect(url_for("game_get"))
    
@app.route("/game")
def game_get():
    
    
    game = Game.current_game
    question = game.current_question
    
    #prevent user from cycling through questions by refreshing page
    try:
        if game.current_question["user_response"]:
            question = game.next_question()
    except KeyError:
        pass
    
    return render_template("game.html", 
                            game=game, 
                            question=question,
                            )

@app.route("/game", methods=["POST"])
def game_post():
    
    """
    I want to create a pair of string lists to compare in the 'scoring' function
    rather than relying on numerical indices. 
    This will allow for possible shuffling later on.
    """
    game = Game.current_game
    question = game.current_question
    
    answer_keys = request.form["answer_keys"].split('++')
    print(answer_keys)
    question['user_response'] = answer_keys
    
    flash("this is a test message")#oups...this isn't working
    
    return redirect(url_for("show_answer"))

@app.route("/show_answer")
def show_answer():
    
    #get our trusty game object back
    game = Game.current_game
    question = game.current_question
    user_response = question["user_response"]
    
    #scorekeeping
    score = game.determine_score(user_response)
    question["score"] = score
    game.total_score = game.total_score + score 
    
    
    ###!!!!!will add logic for marathon and timed game
        
    return render_template("show_answer.html",
                            game=game,
                            question=question,
                            score=score,
                            game_over = game.game_over)
    
@app.route("/show_answer", methods=['POST'])
def show_answer_post():
    
    #get our trusty game object back
    game = Game.current_game
    
    if game.game_over:
        return redirect(url_for("game_summary"))
    else:
        return redirect(url_for("game_get"))
    
    
@app.route("/game_summary")
def game_summary():
    return render_template("game_summary.html",
                            game=Game.current_game)
                            
                            
@app.route("/game_summary", methods=['POST'])
def game_summary_post():
    return redirect(url_for("home"))
    
@app.route("/test_jquery", methods=['GET', 'POST'])
def test_jquery():
    
    if request.method == "POST":
        answer_keys = request.form["answer_keys"]
        print('ordered list ', answer_keys)
        return "Thank You"
    
    return render_template("test_jquery1.html")