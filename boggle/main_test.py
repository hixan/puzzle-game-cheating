from .main import common_ancestors, WordTree, Board


class TestBoardStrings:

    x1 = '''
    a b c d e
    f g d h x
    b r b qu l
    g k j u b
    x u x a e
    '''
    y1 = [
        ['A', 'B', 'C', 'D', 'E'],
        ['F', 'G', 'D', 'H', 'X'],
        ['B', 'R', 'B', 'Qu', 'L'],
        ['G', 'K', 'J', 'U', 'B'],
        ['X', 'U', 'X', 'A', 'E'],
    ]
    o1 = '''
A  B  C  D  E
F  G  D  H  X
B  R  B  Qu L
G  K  J  U  B
X  U  X  A  E
    '''.strip(' \n')

    def test_format_board(self):
        assert str(Board(self.x1)) == self.o1

    def test_parse_board(self):
        assert Board(self.x1).board_state == self.y1


class TestGraphStructure:
    examples = ['AALII', 'AALIIS', 'AALS', 'AARDVARK', 'AARDVARKS']

    def test_common_ancestors_multiple(self):
        assert common_ancestors(self.examples) == 'AA'

    def test_common_ancestors_none(self):
        assert common_ancestors(['AB', 'D']) == ''

    def test_common_ancestors_double(self):
        assert common_ancestors(self.examples[:2])

    def test_graph_puddle(self):
        ''' tests equality as well as basic inserting (shallower than shallow) '''
        wt = WordTree(['A', 'B'])
        true = WordTree([])
        true.children = {'A': WordTree([]), 'B': WordTree([])}
        assert wt == true

    def test_graph_shallow(self):
        wt = WordTree(['AA', 'AB', 'BA'])
        true = WordTree([])
        true.children = {'A': WordTree(['A', 'B']), 'B': WordTree(['A'])}
        assert wt == true
