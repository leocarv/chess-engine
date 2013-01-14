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

    def test_get_fen(self):
        self.my_board = Board()
        moves = [
            ['e4', 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'],
            ['e5', 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2'],
            ['Nf3', 'rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 0 2'],
            ['d6', 'rnbqkbnr/ppp2ppp/3p4/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 3'],
            ['Ke2', 'rnbqkbnr/ppp2ppp/3p4/4p3/4P3/5N2/PPPPKPPP/RNBQ1B1R b kq - 0 3'],
            ['Bg4', 'rn1qkbnr/ppp2ppp/3p4/4p3/4P1b1/5N2/PPPPKPPP/RNBQ1B1R w kq - 0 4'],
            ['Nc3', 'rn1qkbnr/ppp2ppp/3p4/4p3/4P1b1/2N2N2/PPPPKPPP/R1BQ1B1R b kq - 0 4'],
            ['Qf6', 'rn2kbnr/ppp2ppp/3p1q2/4p3/4P1b1/2N2N2/PPPPKPPP/R1BQ1B1R w kq - 0 5']
        ]
        for move in moves:
            self.my_board.move_algebraic(move[0])
            fen = self.my_board.get_fen()
            self.assertEqual(fen, move[1],
                'erro no movimento %s \n esperado: %s \n recebido: %s' % (move[0], move[1], fen))

    def test_en_passant(self):
        self.my_board = Board('rnbqkb1r/ppp1ppp1/5n1p/2Pp4/8/4P3/PP1P1PPP/RNBQKBNR w KQkq d6 0 4')
        self.my_board.move_algebraic('cxd6')
        print self.my_board.to_ascii_art()

    def test_helper(self):
        self.my_board = Board('8/8/4kr2/3p4/8/1N1K1N2/8/8 w - - 0 1')
        self.my_board.move_algebraic('Nbd4+')
        print self.my_board.to_ascii_art()

    def test_castling(self):
        self.my_board = Board('rn1qkbnr/ppp2ppp/3p4/4p3/2B1P1b1/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4')
        self.my_board.move_algebraic('Rg1')
        self.assertEqual(self.my_board.get_fen(),
                'rn1qkbnr/ppp2ppp/3p4/4p3/2B1P1b1/5N2/PPPP1PPP/RNBQK1R1 b Qkq - 0 4')
