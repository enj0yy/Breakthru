import tkinter as tk
import random
import time

class BoardGameGUI:
    def __init__(self, master, lado, player, computer, begin):
        self.master = master
        self.player = player
        self.computer = computer
        self.lado = lado
        self.turn = begin
        self.selected_piece = None
        self.minimax_calls = 0
        self.minimax_calls_alpha_beta = 0
        self.heuristic_value_piece_count = 0
        self.cinza_count = 12
        self.amarelo_count = 9
        self.create_board()

    def create_board(self):
        self.buttons = []
        self.board = [[None for _ in range(self.lado)] for _ in range(self.lado)]  # Representação do estado do tabuleiro
        for row in range(self.lado):
            button_row = []
            for col in range(self.lado):
                button = tk.Button(self.master, width=4, height=2, command=lambda r=row, c=col: self.on_button_click(r, c))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)
        
        for i in range(2,5):
            self.place_piece(0, i, "Cinza")
            self.place_piece(i, 0, "Cinza")
            self.place_piece(i, 6, "Cinza")
            self.place_piece(6, i, "Cinza")

            self.place_piece(2, i, "Amarelo")
            self.place_piece(i, 2, "Amarelo")
            self.place_piece(i, 4, "Amarelo")
            self.place_piece(4, i, "Amarelo")

        self.place_piece(3, 3, "N")

    def on_button_click(self, row, col):
        if (self.board[row][col] is not None):
            if (self.player == "Amarelo") and ((self.board[row][col] == self.player) or (self.board[row][col] == "N")):
                self.selected_piece = (row, col)
                return
            elif self.board[row][col] == self.player:
                self.selected_piece = (row, col)
                return
            
        if (self.selected_piece is not None):
            selected_row, selected_col = self.selected_piece
            self.move_piece(selected_row, selected_col, row, col)
            self.selected_piece = None     

    def check_move(self, row, col, new_row, new_col):
        # Comer na diagonal
        if self.board[new_row][new_col] is not None:
            if abs(row - new_row) == 1 and abs(col - new_col) == 1:
                return True
            return False
        
        # Movimento na horizontal
        if row == new_row:     
            if col > new_col:
                for i in range(col-1, new_col, -1):
                    if self.board[row][i] is not None:
                        return False
            else:
                for i in range(col+1, new_col):
                    if self.board[row][i] is not None:
                        return False
            return True
                    
        # Movimento na vertical            
        elif col == new_col:   
            if row > new_row:
                for i in range(row-1, new_row, -1):
                    if self.board[i][col] is not None:
                        return False
            else:
                for i in range(row+1, new_row):
                    if self.board[i][col] is not None:
                        return False
            return True
        
        return False
    
    def place_piece(self, row, col, piece):
        self.board[row][col] = piece
        button = self.buttons[row][col]
        if piece == "Amarelo":
            button.config(bg="gold1")
        elif piece == "N":
            button.config(bg="goldenrod")
        elif piece == "Cinza":
            button.config(bg="gray60")
        else:
            button.config(bg="SystemButtonFace")

    def move_piece(self, row, col, new_row, new_col):
        if not self.check_move(row, col, new_row, new_col):
            print("Movimento inválido")
            return
        piece = self.board[row][col]

        self.place_piece(row,col,None)              # Remove a peça da posição antiga
        self.place_piece(new_row,new_col,piece)     # Coloca a peça na nova posição

        if self.turn == "Amarelo":
            self.turn = "Cinza"
        else:
            self.turn = "Amarelo"
        
    def get_possible_moves(self, board, player):
        possible_moves = []

        for row in range(self.lado):
            for col in range(self.lado):
                if (player == "Amarelo" and (board[row][col] == player or board[row][col] == "N")) or (player == "Cinza" and board[row][col] == player):

                    # Gerar movimentos para cima até o fim do tabuleiro
                    for i in range(row-1, -1, -1):
                        if board[i][col] == None:
                            possible_moves.append(((row,col),(i, col)))
                        else:
                            break

                    # Gerar movimentos para baixo até o fim do tabuleiro
                    for i in range(row+1, self.lado):
                        if board[i][col] == None:
                            possible_moves.append(((row,col),(i, col)))
                        else:
                            break

                    # Gerar movimentos para a esquerda até o fim do tabuleiro
                    for i in range(col-1, -1, -1):
                        if board[row][i] == None:
                            possible_moves.append(((row,col),(row, i)))
                        else:
                            break

                    # Gerar movimentos para a direita até o fim do tabuleiro
                    for i in range(col+1, self.lado):
                        if board[row][i] == None:
                            possible_moves.append(((row,col),(row, i)))
                        else:
                            break

                    # Cima esquerda   
                    if (row > 0 and col > 0) and (board[row-1][col-1] != player):               
                        if (self.computer == "Amarelo") and (board[row-1][col-1] == "Cinza"):          
                            possible_moves.append(((row,col),(row-1, col-1)))
                        elif (self.computer == "Cinza") and ((board[row-1][col-1] == "Amarelo") or (board[row-1][col-1] == "N")):
                            possible_moves.append(((row,col),(row-1, col-1)))

                    # Cima direita
                    if (row > 0 and col < self.lado-1) and (board[row-1][col+1] != player):       
                        if (self.computer == "Amarelo") and (board[row-1][col+1] == "Cinza"):
                            possible_moves.append(((row,col),(row-1, col+1)))
                        elif (self.computer == "Cinza") and ((board[row-1][col+1] == "Amarelo") or (board[row-1][col+1] == "N")):
                            possible_moves.append(((row,col),(row-1, col+1)))
                    
                    # Baixo esquerda
                    if (row < self.lado-1 and col > 0) and (board[row+1][col-1] != player):
                        if (self.computer == "Amarelo") and (board[row+1][col-1] == "Cinza"):
                            possible_moves.append(((row,col),(row+1, col-1)))
                        elif (self.computer == "Cinza") and ((board[row+1][col-1] == "Amarelo") or (board[row+1][col-1] == "N")):
                            possible_moves.append(((row,col),(row+1, col-1)))
                    
                    # Baixo direita
                    if (row < self.lado-1 and col < self.lado-1) and (board[row+1][col+1] != player):
                        if (self.computer == "Amarelo") and (board[row+1][col+1] == "Cinza"):
                            possible_moves.append(((row,col),(row+1, col+1)))
                        elif (self.computer == "Cinza") and ((board[row+1][col+1] == "Amarelo") or (board[row+1][col+1] == "N")):
                            possible_moves.append(((row,col),(row+1, col+1)))
                            
        return possible_moves

    def make_best_move_minimax(self):
        best_score = -float("inf")
        best_move = None

        for move in self.get_possible_moves(self.board, self.computer):
            new_board = self.make_move(self.board, move)
            score = self.minimax(new_board, False, 0, 3)
            if score > best_score:
                best_score = score
                best_move = move

        if best_move is not None:
            (start_row, start_col), (end_row, end_col) = best_move
            self.move_piece(start_row, start_col, end_row, end_col)
            
        return best_move
    
    def minimax(self, board, is_maximizing, current_depth, depth):
        self.minimax_calls += 1

        if self.check_winner(board) is not None or current_depth == depth:
            return self.get_score(board) - current_depth

        if is_maximizing:
            best_score = -float("inf")
            for move in self.get_possible_moves(board, self.computer):
                new_board = self.make_move(board, move)
                score = self.minimax(new_board, False, current_depth+1, depth)
                best_score = max(best_score, score)
            return best_score

        else:
            best_score = float("inf")
            for move in self.get_possible_moves(board, self.player):
                new_board = self.make_move(board, move)
                score = self.minimax(new_board, True, current_depth+1, depth)
                best_score = min(best_score, score)
            return best_score


    def make_best_move_minimax_alpha_beta_missing_piece(self):
        best_score = -float("inf")
        best_move = None
        alpha = -float("inf")
        beta = float("inf")

        for move in self.get_possible_moves(self.board, self.computer):
            new_board = self.make_move(self.board, move)
            score = self.minimax_alpha_beta_missing_piece(new_board, False, 0, 6, alpha, beta, set())
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        if best_move is not None:
            (start_row, start_col), (end_row, end_col) = best_move
            self.move_piece(start_row, start_col, end_row, end_col)
            
        return best_move
    
    def minimax_alpha_beta_missing_piece(self, board, is_maximizing, current_depth, depth, alpha, beta, visited_states):
        self.minimax_calls_alpha_beta += 1

        if self.check_winner(board) is not None:
            return self.get_score(board) - current_depth
        elif current_depth == depth:
            return self.evaluate_heuristic_piece_count_missing(board, self.player)


        state_key = tuple(map(tuple, board))
        if state_key in visited_states:
            return 0
        
        visited_states.add(state_key)  

        if is_maximizing:
            best_score = -float("inf")
            for move in self.get_possible_moves(board, self.computer):
                new_board = self.make_move(board, move)
                score = self.minimax_alpha_beta_missing_piece(new_board, False, current_depth+1, depth, alpha, beta, visited_states)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score

        else:
            best_score = float("inf")
            for move in self.get_possible_moves(board, self.player):
                new_board = self.make_move(board, move)
                score = self.minimax_alpha_beta_missing_piece(new_board, True, current_depth+1, depth, alpha, beta, visited_states)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score
        
    def evaluate_heuristic_piece_count_missing(self, board, player):
        player_count = 0
        for row in range(self.lado):
            for col in range(self.lado):
                if player == "Amarelo" and (board[row][col] == player or board[row][col] == "N"):
                    player_count += 1
                elif player == "Cinza" and board[row][col] == player:
                    player_count += 1

        if player == 'Amarelo':  
            return self.amarelo_count - player_count
        else:
            return self.cinza_count - player_count
        
    def make_best_move_minimax_alpha_beta_manhattan_distance(self):
        best_score = -float("inf")
        best_move = None
        alpha = -float("inf")
        beta = float("inf")

        for move in self.get_possible_moves(self.board, self.computer):
            new_board = self.make_move(self.board, move)
            score = self.minimax_alpha_beta_manhattan_distance(new_board, False, 0, 6, alpha, beta, set())
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        if best_move is not None:
            (start_row, start_col), (end_row, end_col) = best_move
            self.move_piece(start_row, start_col, end_row, end_col)

    def minimax_alpha_beta_manhattan_distance(self, board, is_maximizing, current_depth, depth, alpha, beta, visited_states):
        self.minimax_calls_alpha_beta += 1

        if self.check_winner(board) is not None:
            return self.get_score(board) - current_depth
        elif current_depth == depth:
            return self.evaluate_manhattan_distance(board, self.player)

        state_key = tuple(map(tuple, board))
        if state_key in visited_states:
            return 0
        
        visited_states.add(state_key)  

        if is_maximizing:
            best_score = -float("inf")
            for move in self.get_possible_moves(board, self.computer):
                new_board = self.make_move(board, move)
                score = self.minimax_alpha_beta_manhattan_distance(new_board, False, current_depth+1, depth, alpha, beta, visited_states)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score

        else:
            best_score = float("inf")
            for move in self.get_possible_moves(board, self.player):
                new_board = self.make_move(board, move)
                score = self.minimax_alpha_beta_manhattan_distance(new_board, True, current_depth+1, depth, alpha, beta, visited_states)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score

    def evaluate_manhattan_distance(self, board, computer):
        flagpos = ()
        menor_distancia = float("inf")
        for row in range(self.lado):
            for col in range(self.lado):
                if board[row][col] == "N":
                    flagpos = (row, col)
                    break

        if computer == "Cinza":
            for row in range(self.lado):
                for col in range(self.lado):
                    if board[row][col] == computer:
                        distance = self.calculate_manhattan_distance(row, col, flagpos[0], flagpos[1])
                        if menor_distancia > distance:
                            menor_distancia = distance
            return abs(6 - menor_distancia)
        
        elif computer == "Amarelo":
            # andar pelo perimetro do tabuleiro e calcular a distancia de cada ate a bandeira
            for lado in range(self.lado):
                distance = self.calculate_manhattan_distance(flagpos[0], flagpos[1], 0, lado)
                if menor_distancia > distance:
                    menor_distancia = distance
                distance = self.calculate_manhattan_distance(flagpos[0], flagpos[1], 6, lado)
                if menor_distancia > distance:
                    menor_distancia = distance
                distance = self.calculate_manhattan_distance(flagpos[0], flagpos[1], lado, 0)
                if menor_distancia > distance:
                    menor_distancia = distance
                distance = self.calculate_manhattan_distance(flagpos[0], flagpos[1], lado, 6)
                if menor_distancia > distance:
                    menor_distancia = distance
            return abs(6 - menor_distancia)
                
                    
                    
    def calculate_manhattan_distance(self, row, col, flag_row, flag_col):
        return abs(row - flag_row) + abs(col - flag_col)  
      
    def make_move(self, board, move):
        new_board = [row[:] for row in board] 
        (start_row, start_col), (end_row, end_col) = move
        new_board[end_row][end_col] = new_board[start_row][start_col]
        new_board[start_row][start_col] = None
        return new_board
        
    def check_winner(self, board):
        # Checar se o Amarelo chegou no perimetro (Navio fugiu)
        for lado in range(self.lado):
            if board[0][lado] == "N":
                return "Amarelo"
            if board[6][lado] == "N":
                return "Amarelo"
            if board[lado][0] == "N":
                return "Amarelo"
            if board[lado][6] == "N":
                return "Amarelo"
            
        # Checar se nao tem N no tabuleiro (Navio capturado)
        for row in range(self.lado):
            for col in range(self.lado):
                if board[row][col] == "N":
                    return None
                
        return "Cinza"
    
    def get_score(self, board):
        winner = self.check_winner(board)
        if winner == self.computer:
            return 100
        if winner == self.player:
            return -100
        return 0
    
    def disable_buttons(self):
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")
    
    def enable_buttons(self):
        for row in range(self.lado):
            for col in range(self.lado):
                self.buttons[row][col].config(state="normal")


def game_start(choice):
    window = tk.Tk()
    
    window.title("Breakthru")
    lado = 7
    
    if random.choice([1, 2]) == 1:
        player = "Cinza"
        computer = "Amarelo"
        text = "Computador é o Amarelo \nVocê é o Cinza"
    else:
        player = "Amarelo"
        computer = "Cinza"
        text = "Computador é o Cinza \nVocê é o Amarelo"

    begin = random.choice([player, computer])
    game = BoardGameGUI(window, lado, player, computer, begin)
    game.disable_buttons()

    info_label = tk.Label(window, text=text)
    info_label.grid(row=7, columnspan=7)
    window.eval('tk::PlaceWindow . center')
    window.update()
    time.sleep(2)

    winner = None
    while winner is None:
        window.update()
        
        if game.turn == player:
            info_label.config(text="Sua vez (" + player + ")")
            game.enable_buttons()
        else:
            info_label.config(text="Vez do computador (" + game.computer + ")")
            game.disable_buttons()
            window.update()
            
            if choice == "1":
                best_move = game.make_best_move_minimax()
                print("Minimax calls:", game.minimax_calls)
                print("Best move PC:", best_move)
            elif choice == "2":
                best_move = game.make_best_move_minimax_alpha_beta_missing_piece()
                print("Minimax calls with Alpha-Beta Pruning: ", game.minimax_calls_alpha_beta)
                print("Best move PC with Alpha-Beta Pruning: ", best_move)
            elif choice == "3":
                best_move = game.make_best_move_minimax_alpha_beta_manhattan_distance()
                print("Minimax calls with Alpha-Beta Pruning: ", game.minimax_calls_alpha_beta)
                print("Best move PC with Alpha-Beta Pruning: ", best_move)

        window.update()
        winner = game.check_winner(game.board)
        if winner is not None:
            game.disable_buttons()
            if winner == player:
                info_label.config(text="Você ganhou!")
            else:
                info_label.config(text="Computador ganhou!")
            window.update()
            time.sleep(2)
            break
        
    window.destroy()

def main():
    startWindow = tk.Tk()
    
    startWindow.title("Breakthru")

    choice = tk.StringVar() 
    choice.set("0")

    def update_choice():  
        if choice.get() != "1" and choice.get() != "2" and choice.get() != "3":
            return
        choice_value = choice.get()
        startWindow.destroy()
        game_start(choice_value)

    startWindow.geometry("240x170")


    heuristic_label = tk.Label(startWindow, font=('Arial', 10, 'bold'), text="Escolha a heurística")
    heuristic_label.grid(padx=10, pady=10,row=8, columnspan=12)

    heuristic_label2 = tk.Label(startWindow, font=('Arial', 10, 'normal'), text="1 - Minimax\n2 - Poda Alpha-Beta: Missing Piece Count Heuristic\n3 - Poda Alpha-Beta: Manhattan Distance Heuristic")
    heuristic_label2.grid(padx=10, pady=5,row=9, columnspan=12)
    
    heuristic_entry = tk.Entry(startWindow, textvariable=choice, width=10, justify='center')
    heuristic_entry.grid(pady=5,row=11, columnspan=12)

    start_button = tk.Button(startWindow, text="Iniciar jogo", command=update_choice, height=1, width=15, font=('Arial', 10, 'normal'))
    start_button.grid(pady=10, row=15, columnspan=12)
    
    
    startWindow.eval('tk::PlaceWindow . center')
    startWindow.mainloop()

    

    

if __name__ == "__main__":
    main()