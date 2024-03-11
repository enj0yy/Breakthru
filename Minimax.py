def make_best_move_minimax(game, depth):
    best_score = -float("inf")
    best_move = None

    moves = game.get_possible_moves(game.board, game.computer)
    for move in moves:
        new_board = game.make_move(game.board, move)
        score = minimax(game,new_board, True, 0, depth)
        if score > best_score:
            best_score = score
            best_move = move

    if best_move is not None:
        (start_row, start_col), (end_row, end_col) = best_move
        game.move_piece(start_row, start_col, end_row, end_col)

    return best_move


def minimax(game, board, is_maximizing, current_depth, depth):
    game.minimax_calls += 1

    if game.check_winner(board) is not None or current_depth == depth:
        return game.get_score(board) - current_depth

    if is_maximizing:
        best_score = -float("inf")      
        for move in game.get_possible_moves(board, game.computer):
            new_board = game.make_move(board, move)
            score = minimax(game, new_board, False, current_depth + 1, depth)
            best_score = max(best_score, score)
        return best_score

    else:      
        best_score = float("inf")
        for move in game.get_possible_moves(board, game.player):
            new_board = game.make_move(board, move)
            score = minimax(game, new_board, True, current_depth + 1, depth)
            best_score = min(best_score, score)
        return best_score
