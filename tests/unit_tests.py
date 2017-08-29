import os
import unittest
import datetime

# Configure your app to use the testing configuration
if not "CONFIG_PATH" in os.environ:
    os.environ["CONFIG_PATH"] = "compare.config.TestingConfig"

from compare.game import Game

class GameTest(unittest.TestCase):

    def test_determine_score(self):
        
        game = Game.create_new_game()
        
        answer = [1,2,3,4]
        answer_key = [1,2,3,4]
        
        self.assertEqual(game.determine_score(answer,answer_key),3)
    
if __name__ == "__main__":
    unittest.main()