"""
This contains the code for solving puzzles
using the naive `Constraint = List[str]`
representation
"""

from __future__ import annotations

from typing import List, Set, Optional, NamedTuple
import itertools
from collections import deque, defaultdict
import random

from typeshift.words import words

Constraint = List[str]
Constraints = List[Constraint]

def apply(word: str, constraints: Constraints) -> Constraints:
    return [
        [ch for ch in constraint if ch != c]
        for c, constraint in zip(word, constraints)
    ]

class Spec(NamedTuple):
    constraints: Constraints
    valid_words: Set[str] = set(words)

    def __repr__(self) -> str:
        return str(self.constraints)

    def brute_force(self) -> List[str]:
        return [
            word 
            for chars in itertools.product(*self.constraints)
            if (word := ''.join(chars)) in self.valid_words
        ]

    @staticmethod
    def from_words(seed_words: List[str], valid_words: Set[str] = set(words)) -> Spec:
        constraints = [sorted(set(chars)) for chars in zip(*seed_words)]
        return Spec(constraints, valid_words)

    def minimal_solution(self) -> List[str]:
        candidates = self.brute_force()

        class QItem(NamedTuple):
            guessed: List[str]
            unsatisfied: Constraints

        q = deque([QItem([], self.constraints)])

        while q:
            guessed, unsatisfied = q.popleft()
            print(guessed, len(q))
            if not(any(unsatisfied)):
                return guessed
            for word in candidates:
                if not guessed or word > guessed[-1]:
                    new_unsatisfied = apply(word, unsatisfied)
                    new_guessed = guessed + [word]
                    if not any(new_unsatisfied):
                        return new_guessed

                    q.append(QItem(new_guessed, new_unsatisfied))


        return []

bylen = defaultdict(list)
for word in words:
    bylen[len(word)].append(word)

def random_game(word_length: int, num_words: int) -> List[str]:
    return sorted(random.sample(bylen[word_length], num_words))

game = random_game(word_length=5, num_words=6)
game = ['cameo', 'heels', 'ovens', 'rapid', 'trade', 'wards']

def solve1(game: List[str]) -> List[str]:
    puzz = Spec.from_words(game)
    return puzz.minimal_solution()


# List[Set[str]]


if __name__ == "__main__":
    import sys
    max_words = int(sys.argv[1]) if len(sys.argv) > 1 else -1

    game = ['cameo', 'heels', 'ovens', 'rapid', 'trade', 'wards']
    game = ['awful', 'bread', 'climb', 'empty', 'hello', 'knock', 'light', 'music', 'often', 'range', 'staff', 'throw', 'young']
    game = game[:max_words]
    print(game)
    puzz = Spec.from_words(game)

    print(puzz.minimal_solution())
