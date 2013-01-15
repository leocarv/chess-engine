class InvalidMove(Exception):
    pass


class Board(object):

    def __init__(self,
        fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        # se não informar o parametro FEN, monta o tabuleiro na posição inicial
        # inicializa matriz de 64 posições
        self._board = [None] * 64
        # indica com quem está a vez
        self._white_to_move = True
        # indica se o roque está permitido
        self._castle = '-'
        # se enpassant é possível na jogada atual
        self._enpassant = '-'
        # contador de jogadas
        self._halfmove = 0
        # contador de jogada completa
        self._fullmove = 0
        # inicializa a posição
        self.set_fen(fen)

    def __setitem__(self, key, value):
        """
        i, j = key
        i ... 0..7, it means a..h
        j ... 0..7, it means 1..8

        e.g. e4 is (4, 3)
        """
        i, j = key
        self._board[j * 8 + i] = value

    def __getitem__(self, key):
        i, j = key
        return self._board[j * 8 + i]

    def __str__(self):
        return self.to_ascii_art()

    def to_ascii_art(self):
        s = ""
        s += "+" + "---+" * 8 + "\n"
        for j in reversed(range(8)):
            row = "|"
            for i in range(8):
                if self[i, j] is not None:
                    if self[i, j].black():
                        row += "#%s#|" % self[i, j].to_ascii_art()
                    else:
                        row += " %s |" % self[i, j].to_ascii_art()
                else:
                    row += "   |"
            s += row + "\n"
            s += "+" + "---+" * 8 + "\n"
        return s

    def get_fen(self):
        def print_board():
            r = ""
            for j in reversed(range(8)):
                counter = 0
                for i in range(8):
                    if self[i, j] is None:
                        counter += 1
                    else:
                        if counter > 0:
                            r += str(counter)
                        counter = 0
                        r += self[i, j].to_string()
                if counter > 0:
                    r += str(counter)
                if j > 0:
                    r += "/"
            return r

        def print_vez():
            return 'w' if self._white_to_move else 'b'

        def print_castle():
            return self._castle

        def print_enpassant():
            return self._enpassant

        def print_halfmove():
            return str(self._halfmove)

        def print_fullmove():
            return str(self._fullmove)

        s = ' '.join([print_board(), print_vez(), print_castle(),
                print_enpassant(), print_halfmove(), print_fullmove()])
        return s

    def set_fen(self, fen):

        def letter_to_piece(letter):
            black = not letter.isupper()
            letter = letter.lower()
            if letter == "r":
                piece = Rock(self, black=black)
            if letter == "n":
                piece = Knight(self, black=black)
            if letter == "b":
                piece = Bishop(self, black=black)
            if letter == "q":
                piece = Queen(self, black=black)
            if letter == "k":
                piece = King(self, black=black)
            if letter == "p":
                piece = Pawn(self, black=black)
            return piece

        tabuleiro, vez, castle, enpassant, halfmove, fullmove = fen.split(' ')
        indice = 0
        linhas = tabuleiro.split('/')
        for linha in reversed(linhas):
            for letra in linha:
                if not letra.isdigit():
                    peca = letter_to_piece(letra)
                    self._board[indice] = peca
                    indice += 1
                else:
                    for i in range(int(letra)):
                        self._board[indice] = None
                        indice += 1
        self._white_to_move = (vez == 'w')
        self._castle = castle
        self._enpassant = enpassant
        self._halfmove = int(halfmove)
        self._fullmove = int(fullmove)

    def a2i(self, x):
        if x == "a":
            i = 0
        if x == "b":
            i = 1
        if x == "c":
            i = 2
        if x == "d":
            i = 3
        if x == "e":
            i = 4
        if x == "f":
            i = 5
        if x == "g":
            i = 6
        if x == "h":
            i = 7
        return i

    def i2a(self, i):
        return "abcdefgh"[i]

    def moves_from_list(self, moves):
        for move in moves:
            self.move_algebraic(move)

    def move_algebraic(self, move):
        """
        Do one move.

        "move" is given in the Short Algebraic notation.
        """
        """
        if move == "O-O":
            # kingside castling
            if self._white_to_move:
                self.move_coordinate((4, 0), (6, 0))
                self.move_coordinate((7, 0), (5, 0), True)
            else:
                self.move_coordinate((4, 7), (6, 7))
                self.move_coordinate((7, 7), (5, 7), True)
        elif move == "O-O-O":
            # queenside castling
            if self._white_to_move:
                self.move_coordinate((4, 0), (2, 0))
                self.move_coordinate((0, 0), (3, 0), True)
            else:
                self.move_coordinate((4, 7), (2, 7))
                self.move_coordinate((0, 7), (3, 7), True)
        else:
        """
        #=================================================================
        # faz o parser do texto do movimento
        piece, field, capture, check, helper, castle = self.parse_move(move)
        #=================================================================
        # valida movimento! dispara exceção "InvalidMove" se for inválido
        if not self.valid_move(move, piece, field, capture, castle):
            raise InvalidMove(move)
        #=================================================================
        # faz uma pesquina no tabuleiro para encontrar a peça
        possible_pieces = self.find_piece(piece, field)
        # se achar um total de peças diferente de 1 tenta a desambiguação!
        if len(possible_pieces) != 1:
            possible_pieces = self.use_helper(helper, possible_pieces)
        # caso continue a desambiguação, dispara erro
        if len(possible_pieces) != 1:
            raise InvalidMove(move)
        #=================================================================
        # se for peão e andar 2 casas, gera o enpassant move para o fen
        if piece == Pawn and abs(possible_pieces[0][1] - field[1]) == 2:
            self._enpassant = self.i2a(field[0])
            fator = field[1] if self._white_to_move else field[1] + 2
            self._enpassant += str(fator)
        else:
            self._enpassant = '-'
        #=================================================================
        # realiza o movimento ============================================
        self.move_coordinate(possible_pieces[0], field)

    def parse_move(self, move):

        def convert_field(field):
            if len(field) == 2:
                x = field[0]
                y = field[1]
                i = self.a2i(x)
                j = int(y) - 1
                return i, j
            else:
                raise InvalidMove(move)

        if move == "O-O" or move == "O-O-O":
            piece = King
            castle = True
            capture = False
            check = False
            helper = ''
            if move == "O-O":  # kingside castling
                if self._white_to_move:
                    field = (6, 0)
                else:
                    field = (6, 7)
            elif move == "O-O-O":  # queenside castling
                if self._white_to_move:
                    field = (2, 0)
                else:
                    field = (2, 7)
        else:
            castle = False
            # verifica a peça =============================
            if move[0] == "R":
                piece = Rock
            elif move[0] == "N":
                piece = Knight
            elif move[0] == "B":
                piece = Bishop
            elif move[0] == "Q":
                piece = Queen
            elif move[0] == "K":
                piece = King
            else:
                piece = Pawn
            if piece != Pawn:  # remove a letra da peça, peão não tem
                move = move[1:]
            # verifica se é uma captura ===================
            if move.find("x") != -1:
                capture = True
                move = move.replace("x", "")  # remove o x
            else:
                capture = False
            # verifica se é um check =====================
            if move[-1] == "+":
                check = True
                move = move[:-1]              # remove o +
            else:
                check = False
            # verifica se é uma jogada de desambiguação ==
            helper = move[:-2]
            # recupera o campo destino ===================
            move = move[-2:]
            field = convert_field(move)  # converte em coordenada
        return piece, field, capture, check, helper, castle

    def valid_move(self, move, piece, field, capture, castle):
        # se for captura e a casa destino estiver vazia
        # for um peão e a linha de destino for 2 ou 5 caso contrario
        # dispara erro, pois o peão é a unica peça que permite isso
        if capture:
            if self[field] is None:
                if (piece == Pawn) and (field[1] in [2, 5]):
                    if self._enpassant == '-' or not self._enpassant in move:
                        return False
                else:
                    return False
        else:
        # se não for uma captura e a casa destino estiver ocupada
        # por outra pedra, o movimento não é válido
            if self[field] is not None:
                return False

        # validação do castling <<--
        # se o FEN indicar que o castle não é possível a jogada é inválida
        # TODO: Terminar validação
        if castle:
            if move == "O-O":  # kingside castling
                if self._white_to_move:
                    if not 'K' in self._castle:
                        return False
                    if self[0, 5] is not None or self[0, 6] is not None:
                        return False
                else:
                    if not 'k' in self._castle:
                        return False
                    if self[7, 5] is not None or self[7, 6] is not None:
                        return False

            elif move == "O-O-O":  # queenside castling
                if self._white_to_move:
                    if not 'Q' in self._castle:
                        return False
                    if self[0, 3] is not None or self[0, 2] is not None:
                        return False
                else:
                    if not 'q' in self._castle:
                        return False
                    if self[7, 3] is not None or self[7, 2] is not None:
                        return False

        # caso não tenha encontrado nenhuma situação inválida
        # movimento retorna verdadeiro
        return True

    def find_piece(self, piece, field):
        """
        Finds the piece "piece" that can go to the field "field".
        """
        candidates = []
        # first find all pieces of the type "piece" on the board:
        for i in range(8):
            for j in range(8):
                if isinstance(self[i, j], piece) and \
                        (self[i, j].white() == self._white_to_move):
                            candidates += [(i, j)]
        # try each of them:
        candidates = [x for x in candidates if self[x].can_move(x, field)]
        return candidates

    def use_helper(self, helper, candidates):
        if (helper != "") and (helper in "abcdefgh"):
            i = self.a2i(helper)
            return [x for x in candidates if x[0] == i]
        if (helper != "") and (helper in "12345678"):
            j = int(helper) - 1
            return [x for x in candidates if x[1] == j]
        return candidates

    def move_coordinate(self, old, new, castling=False):
        """
        Do one move. "old" and "new" are coordinates.

        Example:
        > b.move_coordinate((0, 0), (4, 0))
        """

        p = self[old]
        if p is None:
            raise InvalidMove()

        if not castling:
            if not (self._white_to_move == (not p.black())):
                raise InvalidMove()

        # faz o movimento de fato!
        self[old] = None
        self[new] = p

        # en passant:
        if isinstance(p, Pawn):
            if self._white_to_move:
                b = self[new[0], 4]
                if (new[1] == 5) and isinstance(b, Pawn) and b.black():
                    self[new[0], 4] = None
            else:
                b = self[new[0], 3]
                if (new[1] == 2) and isinstance(b, Pawn) and b.white():
                    self[new[0], 3] = None

        # atualiza castling options =============================
        if isinstance(p, King):  # se mover o REI
            if self._white_to_move:
                self._castle = self._castle.replace('K', "")
                self._castle = self._castle.replace('Q', "")
            else:
                self._castle = self._castle.replace('k', "")
                self._castle = self._castle.replace('q', "")
        if isinstance(p, Rock):  # se mover o Torre
            if self._white_to_move:
                if old == (0, 0):
                    self._castle = self._castle.replace('Q', "")
                if old == (7, 0):
                    self._castle = self._castle.replace('K', "")
            else:
                if old == (0, 7):
                    self._castle = self._castle.replace('q', "")
                if old == (7, 7):
                    self._castle = self._castle.replace('k', "")
        if self._castle == '':
            self._castle = '-'

        # troca a vez ===========================================
        if not castling:
            # Se for uma jogada das pretas, incrementa o fullmove
            if not self._white_to_move:
                self._fullmove += 1
            self._white_to_move = not self._white_to_move


class Piece(object):

    def __init__(self, board, black=False):
        self._board = board
        self._black = black

    def black(self):
        return self._black

    def white(self):
        return not self._black


class Rock(Piece):

    def to_ascii_art(self):
        return "R"

    def to_string(self):
        if self._black:
            return "r"
        else:
            return "R"

    def can_move(self, old, new):
        def r(a, b):
            """
            Returns the integers between a, b, exclusive.

            Example:
            >>> r(3, 7)
            [4, 5, 6]
            >>> r(7, 3)
            [4, 5, 6]
            """
            a, b = sorted([a, b])
            return range(a + 1, b)
        #dx = old[0] - new[0]
        #dy = old[1] - new[1]
        if old[1] == new[1]:
            # x-movement
            # check that no piece is between the old and new position
            for i in r(old[0], new[0]):
                if self._board[i, old[1]] is not None:
                    return False
            return True
        if old[0] == new[0]:
            # y-movement
            # check that no piece is between the old and new position
            for j in r(old[1], new[1]):
                if self._board[old[0], j] is not None:
                    return False
            return True
        return False

    def __str__(self):
        if self._black:
            return "Torre Preta"
        else:
            return "Torre Branca"


class Knight(Piece):

    def to_ascii_art(self):
        return "N"

    def to_string(self):
        if self._black:
            return "n"
        else:
            return "N"

    def can_move(self, old, new):
        d = (old[0] - new[0]) ** 2 + (old[1] - new[1]) ** 2
        return d == 5

    def __str__(self):
        if self._black:
            return "Cavalo Preto"
        else:
            return "Cavalo Branco"


class Bishop(Piece):

    def to_ascii_art(self):
        return "B"

    def to_string(self):
        if self._black:
            return "b"
        else:
            return "B"

    def can_move(self, old, new):
        dx = old[0] - new[0]
        dy = old[1] - new[1]
        return (dx == dy) or (dx == -dy)

    def __str__(self):
        if self._black:
            return "Bispo Preto"
        else:
            return "Bispo Branco"


class Queen(Piece):

    def to_ascii_art(self):
        return "Q"

    def to_string(self):
        if self._black:
            return "q"
        else:
            return "Q"

    def can_move(self, old, new):
        return Bishop(self._board, self._black).can_move(old, new) or \
                Rock(self._board, self._black).can_move(old, new)

    def __str__(self):
        if self._black:
            return "Rainha Preta"
        else:
            return "Rainha Branca"


class King(Piece):

    def to_ascii_art(self):
        return "K"

    def to_string(self):
        if self._black:
            return "k"
        else:
            return "K"

    def can_move(self, old, new):
        dx = old[0] - new[0]
        dy = old[1] - new[1]
        return (dx in [-1, 0, 1]) and (dy in [-1, 0, 1])

    def __str__(self):
        if self._black:
            return "Rei Preto"
        else:
            return "Rei Branco"


class Pawn(Piece):

    def to_ascii_art(self):
        return "p"

    def to_string(self):
        if self._black:
            return "p"
        else:
            return "P"

    def can_move(self, old, new):
        dx = new[0] - old[0]
        dy = new[1] - old[1]
        if dx == 0:
            if self._board[new] is None:
                if self.white():
                    return (dy == 1) or ((dy == 2) and (old[1] == 1))
                else:
                    return (dy == -1) or ((dy == -2) and (old[1] == 6))
        if dx in [-1, 1]:
            if self._board[new] is not None:
                if self.white():
                    return dy == 1
                else:
                    return dy == -1
            else:
                # check for en passant:
                if self.white():
                    b = self._board[new[0], 4]
                    if (new[1] == 5) and isinstance(b, Pawn) and b.black():
                        return True
                else:
                    b = self._board[new[0], 3]
                    if (new[1] == 2) and isinstance(b, Pawn) and b.white():
                        return True
        return False

    def __str__(self):
        if self._black:
            return "Peão Preto"
        else:
            return "Peão Branco"
