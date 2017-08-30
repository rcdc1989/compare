import yaml
import random

class Game(object):
    current_game = None
    
    @classmethod
    def create_new_game(cls):
        cls.current_game = Game()
        return cls.current_game
        
    def __init__(self):
        # questions_file = open('compare/questions.yaml', 'r')
        # self.questions = yaml.load(questions_file.read())
        
        self.current_question = None
        self.current_index = 0
        self.game_type = None
        self.question_limit = None
        
        self.time_limit = None
        self.start_time = None
        
        self.strikes = None
        self.game_over = False
        self.total_score = 0
        
    def next_question(self):
        self.current_question = self.questions[self.current_index]
        
        #check if we have questions left
        if self.current_index < len(self.questions):
            self.current_index += 1
        else:
            self.game_over = True
            
        return self.current_question

    def select_questions(self, 
                         categories=None,
                         question_limit=None):
                             
        questions_file = open('compare/questions.yaml', 'r')
        self.questions = yaml.load(questions_file.read())
        #randomize order
        random.shuffle(self.questions)
        
        # if we are in a question limit game, choose 5 questions
        if question_limit:
                self.questions = self.questions[:question_limit-1]
        
    def determine_score(self, user_response, answer_key):
        #consider refatoring to only take the user response
        #get the answer key from the current question
        
        i = 0
        correct_positions = 0
        score = [0,1,2,3,3]
        
        for item in user_response:
    
            if item == answer_key[i]:
                correct_positions += 1
            i += 1
        
        return score[correct_positions]
    
    def shuffle_answers(self):
        pass

