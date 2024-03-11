import tkinter as tk
import time
import Minimax
import AlphaBeta
import AlphaBeta_Heuristic
class Breakthru:
    def __init__(self, master, lado, player, computer, begin):
        self.master = master
        self.player = player
        self.computer = computer
        self.lado = lado
        self.turn = begin
        self.selected_piece = None

        self.minimax_calls = 0
        self.minimax_calls_alpha_beta = 0

        self.cinza_count = 12
        self.amarelo_count = 9

        self.board = None
        self.create_board()

    def create_board(self):
        self.buttons = []
        self.board = [[None for _ in range(self.lado)] for _ in range(self.lado)]  # Representação do estado do tabuleiro
        for row in range(self.lado):
            button_row = []
            for col in range(self.lado):
                button = tk.Button(self.master, width=4, height=2, bg="gray100", command=lambda r=row, c=col: self.on_button_click(r, c))
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
        
        # Movimento para cima, baixo, esquerda ou direita
        if (row == new_row and abs(col - new_col) == 1) or (col == new_col and abs(row - new_row) == 1):
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
            button.config(bg="gray100")

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

                    # Gerar um movimento para cima
                    if row > 0 and board[row-1][col] == None:
                        possible_moves.append(((row,col),(row-1, col)))

                    # Gerar um movimento para baixo
                    if row < self.lado-1 and board[row+1][col] == None:
                        possible_moves.append(((row,col),(row+1, col)))

                    # Gerar um movimento para a esquerda
                    if col > 0 and board[row][col-1] == None:
                        possible_moves.append(((row,col),(row, col-1)))

                    # Gerar um movimento para a direita
                    if col < self.lado-1 and board[row][col+1] == None:
                        possible_moves.append(((row,col),(row, col+1)))

                    # Comer Cima esquerda   
                    if (row > 0 and col > 0) and (board[row-1][col-1] != player):               
                        if (player == "Amarelo") and (board[row-1][col-1] == "Cinza"):          
                            possible_moves.append(((row,col),(row-1, col-1)))
                        elif (player == "Cinza") and ((board[row-1][col-1] == "Amarelo") or (board[row-1][col-1] == "N")):
                            possible_moves.append(((row,col),(row-1, col-1)))

                    # Comer Cima direita
                    if (row > 0 and col < self.lado-1) and (board[row-1][col+1] != player):       
                        if (player == "Amarelo") and (board[row-1][col+1] == "Cinza"):
                            possible_moves.append(((row,col),(row-1, col+1)))
                        elif (player == "Cinza") and ((board[row-1][col+1] == "Amarelo") or (board[row-1][col+1] == "N")):
                            possible_moves.append(((row,col),(row-1, col+1)))
                    
                    # Comer Baixo esquerda
                    if (row < self.lado-1 and col > 0) and (board[row+1][col-1] != player):
                        if (player == "Amarelo") and (board[row+1][col-1] == "Cinza"):
                            possible_moves.append(((row,col),(row+1, col-1)))
                        elif (player == "Cinza") and ((board[row+1][col-1] == "Amarelo") or (board[row+1][col-1] == "N")):
                            possible_moves.append(((row,col),(row+1, col-1)))
                    
                    # Comer Baixo direita
                    if (row < self.lado-1 and col < self.lado-1) and (board[row+1][col+1] != player):
                        if (player == "Amarelo") and (board[row+1][col+1] == "Cinza"):
                            possible_moves.append(((row,col),(row+1, col+1)))
                        elif (player == "Cinza") and ((board[row+1][col+1] == "Amarelo") or (board[row+1][col+1] == "N")):
                            possible_moves.append(((row,col),(row+1, col+1)))
                            
        return possible_moves
      
    def make_move(self, board, move):
        new_board = [row[:] for row in board] 
        (start_row, start_col), (end_row, end_col) = move
        new_board[end_row][end_col] = new_board[start_row][start_col]
        new_board[start_row][start_col] = None
        return new_board
        
    def check_winner(self, board):
        # Checar se nao existem mais peças cinzas ou amarelas
        cinza_count = 0
        amarelo_count = 0

        for row in range(self.lado):
            for col in range(self.lado):
                if board[row][col] == "Cinza":
                    cinza_count += 1
                if board[row][col] == "Amarelo" or board[row][col] == "N":
                    amarelo_count += 1

        if cinza_count == 0:
            return "Amarelo"
        if amarelo_count == 0:
            return "Cinza"

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


def game_start(choice, computer, begin, depth):
    window = tk.Tk()
    
    window.title("Breakthru")
    lado = 7
    
    if computer == "1":
        player = "Amarelo"
        computer = "Cinza"
        text = "Computador é o Cinza \nVocê é o Amarelo"
    elif computer == "2":
        player = "Cinza"
        computer = "Amarelo"
        text = "Computador é o Amarelo \nVocê é o Cinza"

    if begin == "1":
        begin = computer
    elif begin == "2":
        begin = player

    game = Breakthru(window, lado, player, computer, begin)
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
                best_move = Minimax.make_best_move_minimax(game, depth)
                print("Minimax calls:", game.minimax_calls)
                print("Best move PC:", best_move)
            if choice == "2":
                best_move = AlphaBeta.make_best_move_minimax_alpha_beta(game, depth)
                print("Minimax calls with Alpha-Beta Pruning: ", game.minimax_calls_alpha_beta)
                print("Best move PC with Alpha-Beta Pruning: ", best_move)
            elif choice == "3":
                best_move = AlphaBeta_Heuristic.make_best_move_minimax_alpha_beta_heuristic(game, depth)
                print("Minimax calls with Alpha-Beta Pruning Heuristic: ", game.minimax_calls_alpha_beta)
                print("Best move PC with Alpha-Beta Pruning  Heuristic: ", best_move)

        window.update()
        winner = game.check_winner(game.board)
        if winner is not None:
            game.disable_buttons()
            if winner == player:
                info_label.config(text="Você ganhou!", font=('Arial', 12, 'bold'))
            else:
                info_label.config(text="Computador ganhou!", font=('Arial', 12, 'bold'))
            window.update()
            time.sleep(2)
            break
        
    window.destroy()

def main():
    print("Bem vindo ao Breakthru!")
    print("Escolha como o computador irá jogar:")
    print("1 - Minimax")
    print("2 - Poda Alpha-Beta")
    print("3 - Poda Alpha-Beta com Heuristicas")

    choice = input("Escolha: ")
    while choice not in ["1", "2", "3"]:
        print("Escolha inválida")
        choice = input("Escolha: ")

    depth = int(input("Escolha a profundidade da árvore de busca (0-n): "))

    computer = input("Escolha quem o computador será: 1 - Cinza, 2 - Amarelo: ")
    while computer not in ["1", "2"]:
        print("Escolha inválida")
        computer = input("Escolha quem o computador será: 1 - Cinza, 2 - Amarelo: ")
    
    begin = input("Escolha começa: 1 - Computador, 2 - Você: ")
    while begin not in ["1", "2"]:
        print("Escolha inválida")
        begin = input("Escolha começa: 1 - Computador, 2 - Você: ")

    print("Bom jogo :)")
    print("-----------------------------------------------------------------------")
    game_start(choice, computer, begin, depth)


if __name__ == "__main__":
    main()