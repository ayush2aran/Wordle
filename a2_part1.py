import csv
import random
from typing import Optional

import a2_game_tree
import a2_adversarial_wordle as aw  # aw is a short-form to save some typing


################################################################################
# Part 1 - Loading Adversarial Wordle game datasets
################################################################################
def load_game_tree(games_file: str) -> a2_game_tree.GameTree:
    """Return a new game tree based on games_file.

    Preconditions:
        - games_file refers to a csv file in the format described on the assignment handout

    """
    ans = a2_game_tree.GameTree()
    with open(games_file) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            cnt = 0
            for mv in row:
                if mv[0] == 'N' or mv[0] == 'Y' or mv[0] == '?':
                    row[cnt] = tuple(mv)
                cnt += 1
            ans.insert_move_sequence(row)
    return ans


###############################################################################
# Part 1 - Tree-based Random AIs
###############################################################################
class RandomTreeGuesser(aw.Guesser):
    """An Adversarial Wordle Guesser that plays randomly based on a given GameTree.

    This player uses a game tree to make moves, descending into the tree as the game is played.
    On its turn:

        1. First it updates its game tree to its subtree corresponding to the move made by
           its opponent. If no subtree is found, its game tree is set to None.
        2. Then, if its game tree is not None, it picks its next move randomly from among
           the subtrees of its game tree, and then reassigns its game tree to that subtree.
           But if its game tree is None or has no subtrees, the player behaves like aw.RandomGuesser,
           and then sets its game tree to None.
    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player behaves like aw.RandomGuesser.
    _game_tree: Optional[a2_game_tree.GameTree]

    def __init__(self, game_tree: Optional[a2_game_tree.GameTree]) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree.move == a2_game_tree.GAME_START_MOVE
        """
        self._game_tree = game_tree

    def make_move(self, game: aw.AdversarialWordle) -> str:
        """Return a guess given the current game.

        Preconditions:
        - game.is_guesser_turn()
        """
        if game.guesses:
            if self._game_tree is not None:
                subtrees = self._game_tree.get_subtrees()
                if len(subtrees) > 0:
                    for st in subtrees:
                        if st.move == game.statuses[-1]:
                            self._game_tree = st
                else:
                    self._game_tree = None

        if self._game_tree is not None and len(self._game_tree.get_subtrees()) > 0:
            subtree = random.choice(self._game_tree.get_subtrees())
            self._game_tree = subtree
            return self._game_tree.move
        else:
            guess = random.choice(game.get_possible_answers())
            self._game_tree = None
            return guess


class RandomTreeAdversary(aw.Adversary):
    """An Adversarial Wordle Adversary that plays randomly based on a given GameTree.

    This uses the analogous strategy as RandomTreeGuesser, except its moves are statuses rather than guesses.
    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player behaves like aw.RandomAdversary.
    _game_tree: Optional[a2_game_tree.GameTree]

    def __init__(self, game_tree: Optional[a2_game_tree.GameTree]) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree.move == a2_game_tree.GAME_START_MOVE
        """
        self._game_tree = game_tree

    def make_move(self, game: aw.AdversarialWordle) -> tuple[str, ...]:
        """Return a status given the current game.

        Preconditions:
        - not game.is_guesser_turn()
        """
        if self._game_tree is not None:
            subtrees = self._game_tree.get_subtrees()
            if len(subtrees) > 0:
                for st in subtrees:
                    if st.move == game.guesses[-1]:
                        self._game_tree = st
            else:
                self._game_tree = None

        if self._game_tree is not None and len(self._game_tree.get_subtrees()) > 0:
            subtree = random.choice(self._game_tree.get_subtrees())
            self._game_tree = subtree
            return self._game_tree.move
        else:
            possible_answers = game.get_possible_answers()
            current_guess = game.guesses[-1]

            if len(possible_answers) > 1:
                possible_answers.remove(current_guess)

            ans = random.choice(possible_answers)
            self._game_tree = None
            return game.get_status_for_answer(ans)


###############################################################################
# Part 1 - Runner
###############################################################################
def part1_runner(games_file: str, word_set_file: str, max_guesses: int,
                 num_games: int, adversary_random: bool) -> None:
    """Create a game tree from the given file, and run num_games games with the configuration described below.

    The Guesser is a RandomTreeGuesser whose game tree is the one generated from games_file.
    The Adversary is a RandomAdversary if adversary_random is True, otherwise it is a RandomTreeAdversary
    using the SAME game tree as the Guesser.

    Each game uses the word set contained in word_set_file and has max_guesses as the maximum number of guesses.

    Preconditions:
        - games_file refers to a csv file in the format described on the assignment handout
        - word_set_file and max_guesses satisfy the preconditions of aw.run_games
        - num_games >= 1

    """
    # create the game tree from the given file
    game_tree = load_game_tree(games_file)

    # create the guesser using the game tree
    guesser = RandomTreeGuesser(game_tree)

    # create the adversary using either a random tree or a random guesser
    if adversary_random:
        adversary = aw.RandomAdversary()
    else:
        adversary = RandomTreeAdversary(game_tree)

    # run the games using aw.run_games
    aw.run_games(
        num_games=num_games,
        guesser=guesser,
        adversary=adversary,
        word_set_file=word_set_file,
        max_guesses=max_guesses,
    )


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'extra-imports': ['a2_adversarial_wordle', 'a2_game_tree', 'random', 'csv'],
    #     'allowed-io': ['load_game_tree']
    # })

    # Sample call to part1_runner
    part1_runner(
        games_file='data/games/small_sample.csv',
        word_set_file='data/words/official_wordle.txt',
        max_guesses=4,
        num_games=100,
        adversary_random=True  # Try changing to False
    )
