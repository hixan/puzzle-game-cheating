from .main import common_ancestors, WordTree, Board
from itertools import permutations, chain


class TestBoard:

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

    def test_traverse_simple(self):
        board = Board('''
        a b
        c d
        ''')
        chars = 'B', 'C', 'D'
        truth_visited = set(map(
            lambda x: 'A' + ''.join(x),
            chain.from_iterable(permutations(chars, i) for i in range(1, 4))))
        truth_visited.add('A')
        visited_count = 0
        visited = set()
        for w in board.traverse(0, 0, legal_words=self.AlwaysIn()):
            visited.add(w)
            print(w)
            visited_count += 1
        # in this inscance there are no repeated letters meaning there should
        # be no repeated words
        assert visited_count == len(truth_visited)
        assert visited == truth_visited

    class AlwaysIn(WordTree):
        def __init__(self):
            super(TestBoard.AlwaysIn, self).__init__([], min_len=1)
            self.children = {v: self for v in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}

        def __contains__(self, word):
            return True


class TestGraphStructure:
    examples = ['AALII', 'AALIIS', 'AALS', 'AARDVARK', 'AARDVARKS']

    def test_common_ancestors_multiple(self):
        assert common_ancestors(self.examples) == 'AA'

    def test_common_ancestors_none(self):
        assert common_ancestors(['AB', 'D']) == ''

    def test_common_ancestors_double(self):
        assert common_ancestors(self.examples[:2])

    def test_graph_puddle(self):
        ''' tests equality as well as basic inserting (shallower than shallow)
        '''
        wt = WordTree(['A', 'B'], min_len=1)
        truth = WordTree([])
        truth.children = {
            'A': WordTree([], min_len=1),
            'B': WordTree([], min_len=1)
        }
        assert wt == truth

    def test_graph_shallow(self):
        wt = WordTree(['AA', 'AB', 'BA'], min_len=1)
        truth = WordTree([], min_len=1)
        truth.children = {
            'A': WordTree(['A', 'B'], min_len=1),
            'B': WordTree(['A'], min_len=1)
        }
        assert wt == truth

    def test_graph_in(self):
        words = ['ABC', 'ABD', 'DEF', 'GH']
        wt = WordTree(words, min_len=3)
        for word in words[:-1]:
            for i in range(1, len(word)):
                assert word[:i] in wt

        assert 'G' not in wt
        assert 'GH' not in wt
        assert 'H' not in wt
        assert 'ADB' not in wt
        assert '' not in wt
