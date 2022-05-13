import board


import numpy as np
import logging

#from gamestate import GameState
from montecarlotreesearchnode import MonteCarloTreeSearchNode


class MonteCarloTreeSearch:
    # Note that there's no training / testing here.
    # Only get the best move to make according to simulation, regardless of how deep the actual game tree is.
    # Note that, at number_of_simulation = inf, MCTS --> Minimax.
    @staticmethod
    def get_best_move(game_state: board, number_of_simulation=100):
        root = MonteCarloTreeSearchNode(game_state, None)
        for i in range(number_of_simulation):
            logging.debug(f'\nIteration number: {i + 1}')
            leaf_node = root.select(c=np.sqrt(2))  # @Todo: Move this c to be a parameter of MCTS
            winner = leaf_node.rollout()
            leaf_node.backpropagate(winner)

        MonteCarloTreeSearch.__print_tree(root)

        # When finally choosing an action, we shouldn't be exploring.
        return root.select_child_with_random().action

    @staticmethod
    def __print_tree(root: MonteCarloTreeSearchNode):
        logging.debug('\n Printing the current tree:')
        queue = [root]
        while queue:
            popped_node = queue.pop()
            logging.debug(popped_node)
            for child_node in popped_node.children:
                queue.append(child_node)
        logging.debug('\n')
