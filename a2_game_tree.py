from __future__ import annotations
from typing import Optional

# Comment out this line when not using check_contracts
from python_ta.contracts import check_contracts

GAME_START_MOVE = '*'


@check_contracts
class GameTree:
    """A decision tree for Adversarial Wordle moves.

    Each node in the tree stores an Adversarial Wordle move.

    Instance Attributes:
        - move: the current move (guess or status), or '*' if this tree represents the start of a game

    Representation Invariants:
        - self.move == GAME_START_MOVE or self.move is a valid Adversarial Wordle move
        - all(key == self._subtrees[key].move for key in self._subtrees)
        - GAME_START_MOVE not in self._subtrees  # since it can only appear at the very top of a game tree
    """
    move: str | tuple[str, ...]  # The vertical bar | means "or"

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the game trees after a possible
    #      move by the current player.
    _subtrees: dict[str | tuple[str, ...], GameTree]

    def __init__(self, move: str | tuple[str, ...] = GAME_START_MOVE) -> None:
        """Initialize a new game tree.

        Note that this initializer uses optional arguments.

        >>> game = GameTree()
        >>> game.move == GAME_START_MOVE
        True
        """
        self.move = move
        self._subtrees = {}

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return list(self._subtrees.values())

    def find_subtree_by_move(self, move: str | tuple[str, ...]) -> Optional[GameTree]:
        """Return the subtree corresponding to the given move.

        Return None if no subtree corresponds to that move.
        """
        if move in self._subtrees:
            return self._subtrees[move]
        else:
            return None

    def is_guesser_turn(self) -> bool:
        """Return whether the NEXT move should be made by the Guesser."""
        return self.move == GAME_START_MOVE or isinstance(self.move, tuple)

    def __len__(self) -> int:
        """Return the number of items in this tree."""
        # Note: no "empty tree" base case is necessary here.
        # Instead, the only implicit base case is when there are no subtrees (sum returns 0).
        return 1 + sum(subtree.__len__() for subtree in self._subtrees.values())

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.

        You MAY change the implementation of this method (e.g. to display different instance attributes)
        as you work on this assignment.

        Preconditions:
            - depth >= 0
        """
        if self.is_guesser_turn():
            turn_desc = "Guesser's move"
        else:
            turn_desc = "Adversary's move"
        move_desc = f'{self.move} -> {turn_desc}\n'
        str_so_far = '  ' * depth + move_desc
        for subtree in self._subtrees.values():
            str_so_far += subtree._str_indented(depth + 1)
        return str_so_far

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees[subtree.move] = subtree

    ############################################################################
    # Part 1: Loading and "Replaying" Adversarial Wordle games
    ############################################################################
    def insert_move_sequence(self, moves: list[str | tuple[str, ...]]) -> None:
        """Insert the given sequence of moves into this tree.

        The inserted moves form a chain of descendants, where:
            - moves[0] is a child of this tree's root
            - moves[1] is a child of moves[0]
            - moves[2] is a child of moves[1]
            - etc.

        Do not create duplicate moves that share the same parent; for example, if moves[0] is
        already a child of this tree's root, you should recurse into that existing subtree rather
        than create a new subtree with moves[0].
        But if moves[0] is not a child of this tree's root, create a new subtree for it
        and add it to the existing collection of subtrees.

        Preconditions:
        - moves alternates between str and tuple[str, ...] elements
        - moves == [] or isinstance(moves[0], str) if self.move == aw.GAME_START_MOVE or isinstance(self.move, tuple)
        - moves == [] or isinstance(moves[0], tuple) if self.move != aw.GAME_START_MOVE and isinstance(self.move, str)

        """
        if len(moves) == 0:
            return
        curr_move = moves[0]
        curr_subtree = None

        for val in self._subtrees:
            if val == curr_move:
                curr_subtree = self._subtrees[val]
                break

        if curr_subtree is not None:
            curr_subtree.insert_move_sequence(moves[1:])
        else:
            new_subtree = GameTree(curr_move)
            self._subtrees[curr_move] = new_subtree
            new_subtree.insert_move_sequence(moves[1:])

    ############################################################################
    # Part 2: Complete Game Trees and Win Probabilities
    ############################################################################
    def _update_guesser_win_probability(self) -> None:
        """Recalculate the guesser win probability of this tree.


        Using the following definition for the guesser win probability of self:
            - if self is a leaf, don't change the guesser win probability
              (leave the current value alone)
            - if self is not a leaf and self.is_guesser_turn() is True, the guesser win probability
              is equal to the MAXIMUM of the guesser win probabilities of its subtrees
            - if self is not a leaf and self.is_guesser_move is False, the guesser win probability
              is equal to the AVERAGE of the guesser win probabilities of its subtrees
        """


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120
    # })
