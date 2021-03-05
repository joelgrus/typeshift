"""
This contains the code for finding maximal 
"parsimonious" games -- that is, games with
no excess characters.

python typeshift/talk4.py 4 10000
"""

from __future__ import annotations

from typing import List, Set, Optional, NamedTuple, Iterable
import itertools
from collections import deque, defaultdict
import heapq
import random
from string import ascii_lowercase

import multiprocessing

from bitarray import bitarray

from typeshift.words import common_words as words
# from typeshift.words import words

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


def maximal_puzzle(word_length: int) -> List[str]:
    best = []

    puzzle_words = [w for w in words if len(w) == word_length]
    no_words = bitarray([False for _ in puzzle_words])

    w2b = {
        w: one_hot(len(puzzle_words), i)
        for i, w in enumerate(puzzle_words)
    }

    class StackItem(NamedTuple):
        words: bitarray
        used_chars: Constraints
        max_word: int

    stack = [StackItem(no_words, [no_constraint] * word_length, -1)]

    while stack:
        pwords, used_chars, max_word = stack.pop()

        if pwords.count() > len(best):
            best = [puzzle_words[i] for i, b in enumerate(pwords) if b]
            print(len(best), best)

        for i in range(max_word + 1, len(puzzle_words)):
            word = puzzle_words[i]
            is_excess = any(
                (c2b[c] & constraint).any()
                for c, constraint in zip(word, used_chars)
            )

            if not is_excess:
                new_words = pwords | w2b[word]
                new_used_chars = [constraint | c2b[c] for c, constraint in zip(word, used_chars)]
                stack.append(StackItem(new_words, new_used_chars, i))

    return best


def all_puzzles(word_length: int, puzzle_size: int) -> List[str]:
    best = []

    puzzle_words = [w for w in words if len(w) == word_length]
    no_words = bitarray([False for _ in puzzle_words])

    w2b = {
        w: one_hot(len(puzzle_words), i)
        for i, w in enumerate(puzzle_words)
    }

    class StackItem(NamedTuple):
        words: bitarray
        used_chars: Constraints
        max_word: int

    stack = [StackItem(no_words, [no_constraint] * word_length, -1)]

    while stack:
        pwords, used_chars, max_word = stack.pop()

        if pwords.count() == puzzle_size:
            print([puzzle_words[i] for i, b in enumerate(pwords) if b])
            continue

        for i in range(max_word + 1, len(puzzle_words)):
            word = puzzle_words[i]
            is_excess = any(
                (c2b[c] & constraint).any()
                for c, constraint in zip(word, used_chars)
            )

            if not is_excess:
                new_words = pwords | w2b[word]
                new_used_chars = [constraint | c2b[c] for c, constraint in zip(word, used_chars)]
                stack.append(StackItem(new_words, new_used_chars, i))

    return best


def maximal_puzzle2(word_length: int) -> List[str]:
    best = []

    puzzle_words = [w for w in words if len(w) == word_length]
    no_words = bitarray([False for _ in puzzle_words])
    all_words = bitarray([True for _ in puzzle_words])

    def valid(word: str, constraints: Constraints) -> bool:
        """
        Here the word is valid if it doesn't match any of the constraints
        """
        return not any(
            (c2b[c] & constraint).any()
            for c, constraint in zip(word, constraints)
        )

    w2b = {
        w: one_hot(len(puzzle_words), i)
        for i, w in enumerate(puzzle_words)
    }

    class StackItem(NamedTuple):
        words: bitarray
        used_chars: Constraints
        remaining_words: bitarray
        max_word: int

    q = deque([StackItem(no_words, [no_constraint] * word_length, all_words, -1)])

    while q:
        pwords, used_chars, remaining_words, max_word = q.popleft()
        print([puzzle_words[i] for i, b in enumerate(pwords) if b], remaining_words.count())

        if pwords.count() >= len(best):
            best = [puzzle_words[i] for i, b in enumerate(pwords) if b]
            print(len(best), best)

        for i in range(len(remaining_words)):
            if remaining_words[i]:
                word = puzzle_words[i]

                if valid(word, used_chars):
                    new_words = pwords | w2b[word]
                    new_used_chars = [constraint | c2b[c] for c, constraint in zip(word, used_chars)]
                    new_remaining_words = bitarray([ 
                        b and j > max_word and valid(puzzle_words[j], new_used_chars)
                        for j, b in enumerate(remaining_words) 
                    ])

                    stack.append(StackItem(new_words, new_used_chars, new_remaining_words, i))

    return best    


def greedy_puzzle(word_length: int) -> List[str]:
    puzzle_words = [w for w in words if len(w) == word_length]
    random.shuffle(puzzle_words)

    used_letters = [set() for _ in range(word_length)]
    game = []

    for word in puzzle_words:
        if not any(c in used for c, used in zip(word, used_letters)):
            game.append(word)
            used_letters = [used | {c}
                            for c, used in zip(word, used_letters)]

    return sorted(game)


if __name__ == "__main__":
    import sys
    word_length = int(sys.argv[1])
    niter = int(sys.argv[2])

    best = max((greedy_puzzle(word_length) for _ in range(niter)), key=len)
    print(len(best), best)



