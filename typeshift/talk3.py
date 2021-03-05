"""
This contains the code for solving puzzles
using a priority queue to pick at each step
the puzzle with the fewest "excess characters"
"""


from __future__ import annotations

from typing import List, Set, Optional, NamedTuple, Iterable
import itertools
from collections import deque, defaultdict
import heapq
import random
from string import ascii_lowercase

from bitarray import bitarray

from typeshift.words import words

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

        def excess_chars(guessed: bitarray) -> int:
            seen_chars = [no_constraint] * len(self.constraints)
            ec = 0
            for word, included in zip(candidates, guessed):
                if included:
                    for i, c in enumerate(word):
                        ec += sum(seen_chars[i] & c2b[c])
                        seen_chars[i] = seen_chars[i] | c2b[c]
            return ec

        class QItem(NamedTuple):
            excess_chars: int
            negative_num_words: int
            guessed: bitarray
            unsatisfied: Constraints
            max_word: int

        q = [QItem(0, 0, empty, self.constraints, -1)]

        while q:
            ec, nnw, guessed, unsatisfied, max_word = heapq.heappop(q)
            print(ec, nnw, back_to_words(guessed), len(q))

            for i, word in enumerate(candidates):
                if i > max_word and guessed & w2b[word] == empty:
                    new_unsatisfied = apply(word, unsatisfied)
                    new_guessed = guessed | w2b[word]

                    if all(constraint == no_constraint for constraint in new_unsatisfied):
                        return back_to_words(new_guessed)

                    new_ec = excess_chars(new_guessed)

                    qitem = QItem(new_ec, nnw - 1, new_guessed, new_unsatisfied, i)
                    heapq.heappush(q, qitem)

        return []

bylen = defaultdict(list)
for word in words:
    bylen[len(word)].append(word)

def random_game(word_length: int, num_words: int) -> List[str]:
    return sorted(random.sample(bylen[word_length], num_words))

game = random_game(word_length=5, num_words=5)
# game = ['cameo', 'heels', 'ovens', 'rapid', 'trade', 'wards']
# print(game)


def solve3(game: List[str]) -> List[str]:
    puzz = Spec.from_words(game)
    return puzz.minimal_solution()


if __name__ == "__main__":
    import sys
    max_words = int(sys.argv[1]) if len(sys.argv) > 1 else -1

    game = ['cameo', 'heels', 'ovens', 'rapid', 'trade', 'wards']
    game = ['awful', 'bread', 'climb', 'empty', 'hello', 'knock', 'light', 'music', 'often', 'range', 'staff', 'throw', 'young']
    game = game[:max_words]
    print(game)
    puzz = Spec.from_words(game)
    print(puzz.minimal_solution())
