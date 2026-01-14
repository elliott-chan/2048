"""Simple Monte-Carlo Game AI compatible with the current Game2048 API.

Given a board (list of lists), GameAI returns a board after the best first move (before the
random new tile is added) and a boolean indicating whether a valid move was found.

This implementation performs `searches_per_move` random playouts of up to `search_length`
moves for each candidate first move and selects the move with the best average resulting score.
"""

import copy
import random
from game_logic import Game2048


def _apply_move(board, direction):
    """Apply a direction move to a fresh Game2048 initialized with `board`.
    Returns (game_instance, moved_bool).
    """
    g = Game2048(size=len(board))
    g.board = copy.deepcopy(board)
    g.score = 0
    moved = getattr(g, f"move_{direction}")()
    return g, moved


def _any_move_possible(game):
    """Check whether any move is possible from the current game state.
    This is done by trying moves on copies so the real game is not mutated.
    """
    for d in ("up", "down", "left", "right"):
        gtest = Game2048(size=game.size)
        gtest.board = copy.deepcopy(game.board)
        if getattr(gtest, f"move_{d}")():
            return True
    return False


def _simulate_random_playout(game, max_moves):
    """From a starting Game2048 instance `game`, play up to `max_moves` random valid moves.
    Returns the total score gained during the playout (i.e., final_score - start_score).
    """
    sim = Game2048(size=game.size)
    sim.board = copy.deepcopy(game.board)
    sim.score = game.score
    moves_done = 0

    while moves_done < max_moves:
        # pick a random direction and try to move
        direction = random.choice(("up", "down", "left", "right"))
        moved = getattr(sim, f"move_{direction}")()
        if not moved:
            # if no move was possible in any direction -> game over
            if not _any_move_possible(sim):
                break
            # else try another random direction
            continue
        # after a successful move, the real game would add a random tile
        sim.add_random_tile()
        moves_done += 1

    return sim.score - game.score


def GameAI(board, searches_per_move=50, search_length=10):
    """Main entry point used by the rest of the project.

    Args:
        board: list[list[int|None]] current board state
        searches_per_move: number of random playouts to run for each candidate first move
        search_length: max moves to play in each playout

    Returns:
        (suggested_board, valid) where suggested_board is the board AFTER the chosen
        first move (but BEFORE the automatic random tile is added), and `valid` is True
        if a move was found.
    """
    best_board = None
    best_score = -float("inf")

    for direction in ("up", "down", "left", "right"):
        g, moved = _apply_move(board, direction)
        if not moved:
            continue

        # After the first move, real game would add a random tile before further play
        # We'll run playouts starting from that state (so copy and add a random tile).
        total_gain = 0.0
        for _ in range(max(1, searches_per_move)):
            sim = Game2048(size=g.size)
            sim.board = copy.deepcopy(g.board)
            sim.score = g.score
            sim.add_random_tile()
            gain = _simulate_random_playout(sim, search_length)
            total_gain += gain

        avg_gain = total_gain / max(1, searches_per_move)
        # Use the immediate merge score (g.score) plus expected future gains
        estimated = g.score + avg_gain

        if estimated > best_score:
            best_score = estimated
            best_board = copy.deepcopy(g.board)  # board after the first move, before random tile

    if best_board is None:
        return board, False

    return best_board, True
