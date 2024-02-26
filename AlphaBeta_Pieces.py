def make_best_move_minimax_alpha_beta_missing_piece(game):
        best_score = -float("inf")
        best_move = None
        alpha = -float("inf")
        beta = float("inf")

        for move in game.get_possible_moves(game.board, game.computer):
            new_board = game.make_move(game.board, move)
            score = minimax_alpha_beta_missing_piece(game, new_board, False, 0, 4, alpha, beta, set())
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
    
def minimax_alpha_beta_missing_piece(game, board, is_maximizing, current_depth, depth, alpha, beta, visited_states):
        game.minimax_calls_alpha_beta += 1

        if game.check_winner(board) is not None:
            return game.get_score(board) - current_depth
        elif current_depth == depth:
            return evaluate_heuristic_piece_count_missing(game, board, game.player)


        state_key = tuple(map(tuple, board))
        if state_key in visited_states:
            return 0
        
        visited_states.add(state_key)  

        if is_maximizing:
            best_score = -float("inf")
            for move in game.get_possible_moves(board, game.computer):
                new_board = game.make_move(board, move)
                score = minimax_alpha_beta_missing_piece(game, new_board, False, current_depth+1, depth, alpha, beta, visited_states)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score

        else:
            best_score = float("inf")
            for move in game.get_possible_moves(board, game.player):
                new_board = game.make_move(board, move)
                score = minimax_alpha_beta_missing_piece(game, new_board, True, current_depth+1, depth, alpha, beta, visited_states)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score
        
def evaluate_heuristic_piece_count_missing(game, board, player):
        player_count = 0
        for row in range(game.lado):
            for col in range(game.lado):
                if player == "Amarelo" and (board[row][col] == player or board[row][col] == "N"):
                    player_count += 1
                elif player == "Cinza" and board[row][col] == player:
                    player_count += 1

        if player == 'Amarelo':  
            return game.amarelo_count - player_count
        else:
            return game.cinza_count - player_count