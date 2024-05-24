from a2_game_tree import GameTree, GAME_START_MOVE
from a2_adversarial_wordle import CORRECT, WRONG_POSITION, INCORRECT


def build_sample_game_tree() -> GameTree:
    """Create an example game tree."""
    game_tree = GameTree(GAME_START_MOVE)

    game_tree.add_subtree(GameTree('sepal'))
    game_tree.add_subtree(GameTree('tiger'))
    game_tree.add_subtree(GameTree('hello'))

    sub1 = GameTree('reach')
    sub2 = GameTree((WRONG_POSITION, INCORRECT, CORRECT, INCORRECT, WRONG_POSITION))
    sub2.add_subtree(GameTree('brawl'))
    sub2.add_subtree(GameTree('quart'))
    sub1.add_subtree(sub2)
    game_tree.add_subtree(sub1)

    game_tree.add_subtree(GameTree('allow'))
    game_tree.add_subtree(GameTree('music'))

    return game_tree
