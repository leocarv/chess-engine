from django.test import TestCase
from game.models import Game


class ModelTest(TestCase):

    def setUp(self):
        #Cria um registro de cada tipo
        self.game = Game.objects.create(
            white_player=1,
            black_player=1,
            fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

    def test_game(self):
        tst_game = Game.objects.get(pk=self.game.id)
