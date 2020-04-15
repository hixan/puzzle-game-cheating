from __future__ import annotations
from copy import copy
from typing import List, Dict, Iterable, Tuple, Generator, Set
from itertools import permutations
import numpy as np


def common_ancestors(words: List[str]) -> str:
    ''' common substring from beginning of words '''
    common = ''
    for c in zip(*words):
        if np.all(np.array(c) == c[0]):
            common += c[0]
        else:
            return common
    return common


class WordTree:

    def __init__(self, words: Iterable[str], min_len: int = 3):
        ''' words is a sorted (alphabetically) list of words '''
        self.children: Dict[str, WordTree] = {}
        self.min_len = min_len
        for word in words:
            self.add_word(word)

    def add_word(self, word: str):
        ''' inserts a word into the word tree '''
        if len(word) >= self.min_len:
            if word[0] in self.children:
                self.children[word[0]].add_word(word[1:])
            else:
                self.children[word[0]] = WordTree([word[1:]], min_len=1)

    def __repr__(self):
        rv = ''
        for c in self.children:
            rv += f',{c}[{self.children[c]}]'
        return rv[1:]

    def __eq__(self, other):
        return self.children == other.children

    def __contains__(self, word):
        ''' True if word contained in self.
        DOES NOT DEFINE LEGAL WORDS, also defines all SUBSTRINGS of legal
        words starting at index 0. EG if self == WordTree([ABCD]), is a legal
        word, then AB will also be contained. '''
        if len(word) == 0:
            return False
        if word[0] not in self.children:
            return False
        if len(word) == 1:
            return True
        return word[1:] in self.children[word[0]]


class Board:
    def __init__(self, inpt):
        ''' parses a string which is the state of the boggle board '''
        lines = inpt.strip().split('\n')
        self.board_state = list(
            map(lambda x: x.strip().lower().title().split(' '), lines))

    def __str__(self):
        ''' formats a boggle board nicely '''
        lines: List[str] = []
        for l in self.board_state:
            lines.append(' '.join(map(lambda x: f'{x: <2}', l)).strip())
        return '\n'.join(lines)

    def traverse(self,
                 x: int,
                 y: int,
                 legal_words: WordTree,
                 visited: Set[Tuple[int, int]] = None
                 ) -> Generator[str, None, None]:
        if len(self.board_state[0]) <= x or x < 0 or len(
                self.board_state) <= y or y < 0:
            return  # this coordinate is out of bounds, dont yield anything
        if visited is None:
            visited = set()
        else:
            if (x, y) in visited:
                return  # dont yield anything
        # have now visited this square.
        visited.add((x, y))

        # visit this square
        yield self.board_state[y][x]

        # visit all squares around this square
        for nx, ny in [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y),
                       (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]:
            for option in self.traverse(
                    nx,
                    ny,
                    legal_words.children[self.board_state[y][x]],
                    visited=copy(visited)):
                yield self.board_state[y][x] + option
