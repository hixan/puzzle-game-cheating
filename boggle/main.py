from __future__ import annotations
from typing import List, Dict, Iterable, Tuple
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
                 xy: Tuple[int, int],
                 visited: List[Tuple[int, int]] = None) -> List[str]:
        pass
