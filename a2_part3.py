import random
from typing import Optional

import a2_game_tree
import a2_adversarial_wordle as aw


class ExploringGuesser(aw.Guesser):
    """A Guesser player that sometimes plays greedily and sometimes plays randomly.

    Representation Invariants:
        - 0.0 <= self._exploration_probability <= 1.0
    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    #   - _exploration_probability:
    #       The probability that this player ignores its game tree and makes a random move.
    _game_tree: Optional[a2_game_tree.GameTree]
    _exploration_probability: float

    def __init__(self, game_tree: a2_game_tree.GameTree, exploration_probability: float) -> None:
        """Initialize this player."""
        self._game_tree = game_tree
        self._exploration_probability = exploration_probability

    def make_move(self, game: aw.AdversarialWordle) -> str:
        """Make a move given the current game.

        Preconditions:
            - game.is_guesser_turn()
        """


def run_learning_algorithm(
        word_set_file: str,
        max_guesses: int,
        exploration_probabilities: list[float],
        show_stats: bool = True) -> a2_game_tree.GameTree:
    """Play a sequence of AdversarialWordle games using an ExploringGuesser and RandomAdversary.

    This algorithm first initializes an empty GameTree. All ExploringGuessers will use this
    SAME GameTree object, which will be mutated over the course of the algorithm!
    Return this object.

    There are len(exploration_probabilities) games played, where at game i (starting at 0):
        - The Guesser is an ExploringGuesser (using the game tree) whose exploration probability
            is equal to exploration_probabilities[i].
        - The Adversary is a RandomAdversary.
        - AFTER the game, the move sequence from the game is inserted into the game tree,
          with a guesser win probability of 1.0 if the Guesser won the game, and 0.0 otherwise.

    Preconditions:
        - word_set_file and max_guesses satisfy the preconditions of aw.run_game
        - all(0.0 <= p <= 1.0 for p in exploration_probabilities)
        - exploration_probabilities != []

    """


def part3_runner() -> a2_game_tree.GameTree:
    """Run example for Part 3.

    """
    word_set_file = 'data/words/official_wordle_100.txt'
    max_guesses = 3

    probabilities = [0.5] * 1000

    return run_learning_algorithm(word_set_file, max_guesses, probabilities, show_stats=True)


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'max-nested-blocks': 4,
    #     'extra-imports': ['random', 'a2_adversarial_wordle', 'a2_game_tree'],
    #     'allowed-io': ['run_learning_algorithm']
    # })

    part3_runner()
