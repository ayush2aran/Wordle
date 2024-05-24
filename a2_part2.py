import random
from typing import Optional

import a2_game_tree
import a2_adversarial_wordle as aw


def generate_complete_game_tree(root_move: str | tuple[str, ...], game_state: aw.AdversarialWordle,
                                d: int) -> a2_game_tree.GameTree:
    """Generate a complete game tree of depth d for all valid moves from the current game_state.

    For the returned GameTree:
        - Its root move is root_move.
        - It contains all possible move sequences of length <= d from game_state.
        - If d == 0, a size-one GameTree is returned.

    Note that some paths down the tree may have length < d, because they result in a game state
    with a winner in fewer than d moves. Concretely, if game_state.get_winner() is not None,
    then return just a size-one GameTree containing the root move.

    Preconditions:
        - d >= 0
        - root_move == a2_game_tree.GAME_START_MOVE or root_move is a valid move
        - if root_move == a2_game_tree.GAME_START_MOVE, then game_state is in the initial game state
        - if isinstance(root_move, str) and root_move != a2_game_tree.GAME_START_MOVE,\
            then (game_state.guesses[-1] == root_move) and (not game_state.is_guesser_turn())
        - if isinstance(root_move, tuple),\
            then (game_state.statuses[-1] == root_move) and game_state.is_guesser_turn()


    >>> example_game = aw.AdversarialWordle({'hello', 'words', 'world'}, 3)
    >>> tree0 = generate_complete_game_tree(a2_game_tree.GAME_START_MOVE, example_game, 0)
    >>> len(tree0)
    1
    >>> tree1 = generate_complete_game_tree(a2_game_tree.GAME_START_MOVE, example_game, 1)
    >>> len(tree1)
    4
    >>> sorted([subtree.move for subtree in tree1.get_subtrees()])
    ['hello', 'words', 'world']

    """
    if d == 0 or game_state.get_winner() is not None:
        return a2_game_tree.GameTree(root_move)

    tree = a2_game_tree.GameTree(root_move)

    if isinstance(root_move, str):
        possible_answers = game_state.get_possible_answers()


class GreedyTreeGuesser(aw.Guesser):
    """An Adversarial Wordle Guesser that plays greedily based on a given GameTree.

    Description of its strategy not explained here
    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    _game_tree: Optional[a2_game_tree.GameTree]

    def __init__(self, game_tree: a2_game_tree.GameTree) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree.move == a2_game_tree.GAME_START_MOVE
        """
        self._game_tree = game_tree

    def make_move(self, game: aw.AdversarialWordle) -> str:
        """Make a move given the current game.

        Preconditions:
            - game.is_guesser_turn()
        """


class GreedyTreeAdversary(aw.Adversary):
    """An Adversarial Wordle Adversary that plays greedily based on a given GameTree.

    Description of its strategy not explained here
    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    _game_tree: Optional[a2_game_tree.GameTree]

    def __init__(self, game_tree: a2_game_tree.GameTree) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree.move == a2_game_tree.GAME_START_MOVE
        """
        self._game_tree = game_tree

    def make_move(self, game: aw.AdversarialWordle) -> tuple[str, ...]:
        """Make a move given the current game.

        Preconditions:
            - not game.is_guesser_turn()
        """


def part2_runner(word_set_file: str, max_guesses: int, depth: int, num_games: int, guesser_greedy: bool) -> None:
    """Create a complete game tree with the given depth, and run num_games games using the following game configuration.

    If guesser_greedy is True, the Guesser player is the GreedyTreeGuesser and the Adversary is a RandomAdversary.
    If guesser_greedy is False, the Guesser player is a RandomGuesser and the Adversary is a GreedyTreeAdversary.

    In either case, the "Greedy Tree" player uses the complete game tree with the given depth.

    word_set_file and max_guesses have the same meaning as in aw.run_games.

    Preconditions:
        - word_set_file and max_guesses satisfy the preconditions of aw.run_games
        - depth >= 0
        - num_games >= 1

    """


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'max-nested-blocks': 4,
    #     'extra-imports': ['random', 'a2_adversarial_wordle', 'a2_game_tree'],
    #     'allowed-io': ['part2_runner']
    # })

    # Sample call to part2_runner
    # part2_runner(
    #     word_set_file='data/words/official_wordle_25.txt',
    #     max_guesses=3,
    #     depth=6,  # A complete game tree for 3 rounds
    #     num_games=100,
    #     guesser_greedy=False
    # )
