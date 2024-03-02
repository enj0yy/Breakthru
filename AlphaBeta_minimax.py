def make_best_move_minimax_alpha_beta(game, depth):
        best_score = -float("inf")
        best_move = None
        alpha = -float("inf")
        beta = float("inf")

        for move in game.get_possible_moves(game.board, game.computer):
            new_board = game.make_move(game.board, move)
            score = minimax_alpha_beta(game, new_board, False, 0, depth, alpha, beta, set())
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        if best_move is not None:
            (start_row, start_col), (end_row, end_col) = best_move
            game.move_piece(start_row, start_col, end_row, end_col)
            
        return best_move
    
def minimax_alpha_beta(game, board, is_maximizing, current_depth, depth, alpha, beta, visited_states):
        game.minimax_calls_alpha_beta += 1

        if game.check_winner(board) is not None or current_depth == depth:
            return game.get_score(board) - current_depth



        state_key = tuple(map(tuple, board))
        if state_key in visited_states:
            return 0
        
        visited_states.add(state_key)  

        if is_maximizing:
            best_score = -float("inf")
            for move in game.get_possible_moves(board, game.computer):
                new_board = game.make_move(board, move)
                score = minimax_alpha_beta(game, new_board, False, current_depth+1, depth, alpha, beta, visited_states)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score

        else:
            best_score = float("inf")
            for move in game.get_possible_moves(board, game.player):
                new_board = game.make_move(board, move)
                score = minimax_alpha_beta(game, new_board, True, current_depth+1, depth, alpha, beta, visited_states)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score
