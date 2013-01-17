chess-engine
============
  * criar metodo que recebe uma casa e indica se a mesma ta sendo atacada
  * terminar validação do castling [1]
  * terminar testes para saber se o motor do jogo está completo

ferramentas
===========
   * ANÁLISE DE BOARD - http://www.chess.com/analysis-board-editor

material:
=========
  * REGRAS - http://pt.wikipedia.org/wiki/Leis_do_xadrez
  * FEN - http://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
  * PGN - http://en.wikipedia.org/wiki/Portable_Game_Notation
  * NOTAÇÃO ALGÉBRICA - http://pt.wikipedia.org/wiki/Nota%C3%A7%C3%A3o_alg%C3%A9brica_de_xadrez
  * CHESS PROG GAMEDEV - http://www.gamedev.net/page/resources/_/technical/artificial-intelligence/chess-programming-part-i-getting-started-r1014


[1] REGRAS DO CASTLING
>> O Rei e a Torre envolvida não tenham sido previamente movidos;
>> Não exista peças entre o Rei e a Torre;
O Rei não pode estar em xeque, passar ou terminar o movimento em uma casa ameaçada pelo tabuleiro. Entretanto, a Torre pode estar sendo ameaçada ou passar por uma casa ameaçada, no caso do roque grande, durante o movimento;
  
FEN INICIAL: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
