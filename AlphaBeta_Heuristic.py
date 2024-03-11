def make_best_move_minimax_alpha_beta_heuristic(game, depth):
    best_score = -float("inf")
    best_move = None
    alpha = -float("inf")
    beta = float("inf")

    for move in game.get_possible_moves(game.board, game.computer):
        new_board = game.make_move(game.board, move)
        score = minimax_alpha_beta_heuristic(game, new_board, False, 0, depth, alpha, beta, set())
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, best_score)
        if beta <= alpha:
            break

    if best_move is not None:
        print("Score: ", best_score)
        (start_row, start_col), (end_row, end_col) = best_move
        game.move_piece(start_row, start_col, end_row, end_col)

    return best_move


def minimax_alpha_beta_heuristic(game, board, is_maximizing, current_depth, depth, alpha, beta, visited_states):
    game.minimax_calls_alpha_beta += 1

    if game.check_winner(board) is not None:
        return game.get_score(board) - current_depth
    elif current_depth == depth:
        return (evaluate_dangerous_zone(game, board, game.computer)*0.4) + (evaluate_heuristic_piece_count_missing(game, board, game.computer) * 0.5) + (evaluate_heuristic_flag_win(game, board, game.computer) * 0.1)
    
    state_key = tuple(map(tuple, board))
    if state_key in visited_states:
        return (evaluate_dangerous_zone(game, board, game.computer)*0.4) + (evaluate_heuristic_piece_count_missing(game, board, game.computer) * 0.5) + (evaluate_heuristic_flag_win(game, board, game.computer) * 0.1)

    visited_states.add(state_key)

    if is_maximizing:
        best_score = -float("inf")
        for move in game.get_possible_moves(board, game.computer):
            new_board = game.make_move(board, move)
            score = minimax_alpha_beta_heuristic(game, new_board, False, current_depth + 1, depth, alpha, beta, visited_states)
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score

    else:
        best_score = float("inf")
        for move in game.get_possible_moves(board, game.player):
            new_board = game.make_move(board, move)
            score = minimax_alpha_beta_heuristic(game, new_board, True, current_depth + 1, depth, alpha, beta, visited_states)
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score


def evaluate_dangerous_zone(game, board, computer):
    # Avalia a quantidade de inimigos próximos à bandeira

    flagpos = [0, 0]
    enemies = 0
    allies = 0

    for row in range(game.lado):
        for col in range(game.lado):
            if board[row][col] == "N":
                flagpos[0] = row
                flagpos[1] = col
                break

    # Direita
    if board[flagpos[0]][flagpos[1] + 1] == "Cinza":
        enemies += 1
    elif board[flagpos[0]][flagpos[1] + 1] == "Amarelo":
        allies += 1

    # Esquerda
    if board[flagpos[0]][flagpos[1] - 1] == "Cinza":
        enemies += 1
    elif board[flagpos[0]][flagpos[1] - 1] == "Amarelo":
        allies += 1

    # Cima
    if board[flagpos[0] + 1][flagpos[1]] == "Cinza":
        enemies += 1
    elif board[flagpos[0] + 1][flagpos[1]] == "Amarelo":
        allies += 1

    # Baixo
    if board[flagpos[0] - 1][flagpos[1]] == "Cinza":
        enemies += 1
    elif board[flagpos[0] - 1][flagpos[1]] == "Amarelo":
        allies += 1

    # Diagonal superior direita
    if board[flagpos[0] + 1][flagpos[1] + 1] == "Cinza":
        enemies += 1
    elif board[flagpos[0] + 1][flagpos[1] + 1] == "Amarelo":
        allies += 1

    # Diagonal superior esquerda
    if board[flagpos[0] + 1][flagpos[1] - 1] == "Cinza":
        enemies += 1
    elif board[flagpos[0] + 1][flagpos[1] - 1] == "Amarelo":
        allies += 1

    # Diagonal inferior direita
    if board[flagpos[0] - 1][flagpos[1] + 1] == "Cinza":
        enemies += 1
    elif board[flagpos[0] - 1][flagpos[1] + 1] == "Amarelo":
        allies += 1

    # Diagonal inferior esquerda
    if board[flagpos[0] - 1][flagpos[1] - 1] == "Cinza":
        enemies += 1
    elif board[flagpos[0] - 1][flagpos[1] - 1] == "Amarelo":
        allies += 1
    
    if computer == "Cinza":
        return enemies - allies
    elif computer == "Amarelo":
        return allies - enemies


def evaluate_heuristic_piece_count_missing(game, board, computer):
        # Conta as peças do jogador e do computador, normaliza, e retorna a diferença entre elas
        amarelos = 0
        cinzas = 0

        for row in range(game.lado):
            for col in range(game.lado):
                if (board[row][col] == "Amarelo" or board[row][col] == "N"):
                    amarelos += 1
                elif board[row][col] == "Cinza":
                    cinzas += 1

        amarelos = amarelos / game.amarelo_count
        cinzas = cinzas / game.cinza_count

        if computer == "Amarelo":  
            return amarelos - cinzas
        elif computer == "Cinza":
            return cinzas - amarelos
        
def evaluate_heuristic_flag_win(game, board, computer):
    # Mede distancia da flag até o perimetro mais proximo e diminui da distancia total(3)
    flagpos = [0, 0]
    for row in range(game.lado):
        for col in range(game.lado):
            if board[row][col] == "N":
                flagpos[0] = row
                flagpos[1] = col
                break

    min_distance = +float("inf")

    for lado in range(game.lado):
        distance = abs(flagpos[0] - 0) + abs(flagpos[1] - lado)
        min_distance = min(min_distance, distance);

        distance = abs(flagpos[0] - 6) + abs(flagpos[1] - lado)
        min_distance = min(min_distance, distance);

        distance = abs(flagpos[0] - lado) + abs(flagpos[1] - 0)
        min_distance = min(min_distance, distance);

        distance = abs(flagpos[0] - lado) + abs(flagpos[1] - 6)
        min_distance = min(min_distance, distance);

    if computer == "Amarelo":
        return 3 - min_distance
    elif computer == "Cinza":
        return min_distance - 3