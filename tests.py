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

    def test_board(self):
        self.my_board = Board()
        moves = [
            ['e4', 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'],
            ['e5', 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2'],
            ['Nf3', 'rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 0 2'],
            ['d6', 'rnbqkbnr/ppp2ppp/3p4/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 3'],
            ['Bc4', 'rnbqkbnr/ppp2ppp/3p4/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 0 3'],
            ['Nf6', 'rnbqkb1r/ppp2ppp/3p1n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4'],
            ['O-O', 'rnbqkb1r/ppp2ppp/3p1n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQ1RK1 b kq - 0 4']
        ]
        for move in moves:
            self.my_board.move_algebraic(move[0])
            fen = self.my_board.get_fen()
            self.assertEqual(fen, move[1],
                'erro no movimento %s \n esperado: %s \n recebido: %s' % (move[0], move[1], fen))

    def test_get_fen(self):
        #test castling
        self.my_board = Board('rn1qkbnr/ppp2ppp/3p4/4p3/2B1P1b1/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4')
        self.my_board.move_algebraic('Rg1')
        self.assertEqual(self.my_board.get_fen(), 'rn1qkbnr/ppp2ppp/3p4/4p3/2B1P1b1/5N2/PPPP1PPP/RNBQK1R1 b Qkq - 0 4')
        #test helper
        self.my_board = Board('8/8/4kr2/3p4/8/1N1K1N2/8/8 w - - 0 1')
        self.my_board.move_algebraic('Nbd4+')
        self.assertEqual(self.my_board.get_fen(), '8/8/4kr2/3p4/3N4/3K1N2/8/8 b - - 0 1')
        #test enpassant
        self.my_board = Board('r1bqkbnr/p1pp1ppp/n7/1p1PpP2/8/8/PPP1P1PP/RNBQKBNR w KQkq e6 0 5')
        self.my_board.move_algebraic('dxe6')
        self.assertEqual(self.my_board.get_fen(), 'r1bqkbnr/p1pp1ppp/n3P3/1p3P2/8/8/PPP1P1PP/RNBQKBNR b KQkq - 0 5')
