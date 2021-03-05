"""
This contains the code for solving puzzles
using the naive `Constraint = List[str]`
representation

To understand the code imagine the "NEAT WORD GAME" puzzle:

G
W O   E
N E A T
  A M D
    R


time python typeshift/talk1.py awful bread climb empty hello knock light
time python typeshift/talk1.py awful bread climb empty hello knock light music
time python typeshift/talk1.py awful bread climb empty hello knock light music north
"""

from __future__ import annotations

from typing import List, Set, Optional, NamedTuple
import itertools
from collections import deque, defaultdict
import random

from typeshift.words import common_words as words

# A constraint represents the choices for a single position: ['G', 'W', 'N']
Constraint = List[str]

# A 4-letter-word puzzle then has 4 constraints.
Constraints = List[Constraint]


def apply(word: str, constraints: Constraints) -> Constraints:
    """
    Removes all the constraints that are satisfied by the word
    """
    return [
        [ch for ch in constraint if ch != c]
        for c, constraint in zip(word, constraints)
    ]


class Spec(NamedTuple):
    """
    A Spec is the immutable part of a word game
    """
    constraints: Constraints
    valid_words: Set[str] = set(words)

    def __repr__(self) -> str:
        return str(self.constraints)

    def brute_force(self) -> List[str]:
        """
        Use brute force to find all valid words that satisfy the constraints
        """
        return [
            word 
            for chars in itertools.product(*self.constraints)
            if (word := ''.join(chars)) in self.valid_words
        ]

    @staticmethod
    def from_words(seed_words: List[str], valid_words: Set[str] = set(words)) -> Spec:
        """
        Alternate constructor to construct a Spec from "seed words";
        for example: ["neat", "word", "game"]
        """
        constraints = [sorted(set(chars)) for chars in zip(*seed_words)]
        return Spec(constraints, valid_words)

    def minimal_solution(self) -> List[str]:
        """
        Use BFS to find a minimal set of words that "spans" all the constraints.
        """
        # first find *all* the words that are compatible with the constraints
        candidates = self.brute_force()

        class QItem(NamedTuple):
            """
            We will use a queue of partially solved puzzles to do BFS.
            A partially solved puzzle consists of the words that have been guessed
            and the constraints that are still unsatisfied
            """
            guessed: List[str]
            unsatisfied: Constraints

        # seed the queue with the game that hasn't started yet
        q = deque([QItem([], self.constraints)])

        while q:
            # pull the next game off the queue
            guessed, unsatisfied = q.popleft()
            print(guessed, len(q))

            for word in candidates:
                # only add words in alphabetical order to avoid permutations
                if not guessed or word > guessed[-1]:
                    new_unsatisfied = apply(word, unsatisfied)
                    new_guessed = guessed + [word]
                    if not any(new_unsatisfied):
                        return new_guessed

                    q.append(QItem(new_guessed, new_unsatisfied))


        return []


# create a 
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

    if len(sys.argv) == 1:
        game = ['awful', 'bread', 'climb', 'empty', 'hello', 'knock', 'light', 'music', 'often', 'range', 'staff', 'throw', 'young']
    else:
        game = sys.argv[1:]

    #game = ['cameo', 'heels', 'ovens', 'rapid', 'trade', 'wards']
    # game = game[:max_words]
    # print(game)
    puzz = Spec.from_words(game)
    print(puzz.minimal_solution())
