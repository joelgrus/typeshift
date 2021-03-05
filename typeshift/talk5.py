"""
contains code for finding the most "satisfying" games;
that is, for a given (word_length, num_words) combination,
the "parsimonious" game with the most valid words in it
"""

from __future__ import annotations

from typing import List, Set, Optional, NamedTuple, Iterable
import itertools
from collections import deque, defaultdict
import heapq
import random
from string import ascii_lowercase

from bitarray import bitarray

from typeshift.words import common_words as words

Constraint = bitarray
Constraints = List[Constraint]

no_constraint = bitarray([False] * 26)

def one_hot(n: int, i: int) -> bitarray:
    oh = bitarray([False] * n)
    oh[i] = True
    return oh

c2b = {
    c: one_hot(26, i)
    for i, c in enumerate(ascii_lowercase)
}

def constraint2chars(constraint: Constraint) -> List[str]:
    return [c for c, b in zip(ascii_lowercase, constraint) if b]

def chars2constraint(chars: Iterable[str]) -> Constraint:
    constraint = no_constraint
    for c in chars:
        constraint = constraint | c2b[c]
    return constraint

def apply(word: str, constraints: Constraints) -> Constraints:
    return [
        constraint & ~c2b[c]
        for c, constraint in zip(word, constraints)
    ]

class Spec(NamedTuple):
    constraints: Constraints
    valid_words: Set[str] = set(words)

    def __repr__(self) -> str:
        return str(self.constraints)

    def num_constraints(self) -> int:
        return sum(c.count() for c in self.constraints)

    def brute_force(self) -> List[str]:
        charses =[constraint2chars(constraint) for constraint in self.constraints]
        return [
            word 
            for chars in itertools.product(*charses)
            if (word := ''.join(chars)) in self.valid_words
        ]

    @staticmethod
    def from_words(seed_words: List[str], valid_words: Set[str] = set(words)) -> Spec:
        constraints = [chars2constraint(chars) for chars in zip(*seed_words)]
        return Spec(constraints, valid_words)

def most_satisfying(word_length: int, num_words: int = 3) -> List[str]:
    puzzle_words = [w for w in words if len(w) == word_length]
    best, best_size = (), -1

    for game in itertools.combinations(puzzle_words, num_words):
        spec = Spec.from_words(game)
        if spec.num_constraints() == word_length * num_words:
            size = len(spec.brute_force())
            if size > best_size:
                print(game, size)
                best, best_size = game, size

    return list(best)


    # last, pine, rock