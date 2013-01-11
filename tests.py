from django.test import TestCase
from game.models import Game
from chess import Board


class ModelTest(TestCase):

    def setUp(self):
        #Cria um registro de cada tipo
        self.game = Game.objects.create(
            white_player=1,
            black_player=1,
            fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

    def test_create_game(self):
        tst_game = Game.objects.get(pk=self.game.id)
        self.assertEqual(tst_game.fen,
                'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')


class GameTest(TestCase):

    def setUp(self):
        self.my_board = Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

    def test_complete_game(self):
        self.my_board.move_algebraic('e4')
        self.assertEqual(self.my_board.get_fen(), 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1')
