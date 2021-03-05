"""
This contains the code for solving puzzles
using the `Constraint = bitarray` 
representation (but still the naive BFS method)

time python typeshift/talk2.py awful bread climb empty hello knock light music north
"""

from __future__ import annotations

from typing import List, Set, Optional, NamedTuple, Iterable
import itertools
from collections import deque, defaultdict
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

    def minimal_solution(self) -> List[str]:
        candidates = self.brute_force()

        empty = bitarray([False] * len(candidates))
        w2b = {
            w: one_hot(len(candidates), i)
            for i, w in enumerate(candidates)
        }

        def back_to_words(guessed: bitarray) -> List[str]:
            return [candidates[i] for i, bit in enumerate(guessed) if bit]

        class QItem(NamedTuple):
            guessed: bitarray
            unsatisfied: Constraints
            max_word: int

        q = deque([QItem(empty, self.constraints, -1)])

        while q:
            guessed, unsatisfied, max_word = q.popleft()
            print(back_to_words(guessed), len(q))

            for i, word in enumerate(candidates):
                if i > max_word and guessed & w2b[word] == empty:
                    new_unsatisfied = apply(word, unsatisfied)
                    new_guessed = guessed | w2b[word]

                    if all(constraint == no_constraint for constraint in new_unsatisfied):
                        return back_to_words(new_guessed)


                    q.append(QItem(new_guessed, new_unsatisfied, i))


        return []

bylen = defaultdict(list)
for word in words:
    bylen[len(word)].append(word)

def random_game(word_length: int, num_words: int) -> List[str]:
    return sorted(random.sample(bylen[word_length], num_words))

# game = random_game(word_length=5, num_words=5)

def solve2(game: List[str]) -> List[str]:
    puzz = Spec.from_words(game)
    return puzz.minimal_solution()

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        game = ['awful', 'bread', 'climb', 'empty', 'hello', 'knock', 'light', 'music', 'often', 'range', 'staff', 'throw', 'young']
    else:
        game = sys.argv[1:]

    #game = ['cameo', 'heels', 'ovens', 'rapid', 'trade', 'wards']
    # game = game[:max_words]
    # print(game)
    puzz = Spec.from_words(game)
    print(puzz.minimal_solution())
