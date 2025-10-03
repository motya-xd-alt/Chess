import pygame
import sys

pygame.init()


WIDTH, HEIGHT = 640, 640
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT = (100, 249, 83, 150)
MOVE_HIGHLIGHT = (106, 190, 48, 150)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Шахматы")
clock = pygame.time.Clock()



def load_pieces():
    pieces = {}
    colors = ['w', 'b']
    piece_types = ['p', 'r', 'n', 'b', 'q', 'k']

    for color in colors:
        for piece_type in piece_types:
            key = f"{color}{piece_type}"
            try:
                pieces[key] = pygame.transform.scale(
                    pygame.image.load(f"chess_pieces/{key}.png"),
                    (SQUARE_SIZE, SQUARE_SIZE)
                )
            except:

                surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                if color == 'w':
                    pygame.draw.rect(surf, WHITE, (0, 0, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(surf, BLACK, (0, 0, SQUARE_SIZE, SQUARE_SIZE))
                pieces[key] = surf

    return pieces



def initialize_board():

    board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


    board[0] = ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br']
    board[1] = ['bp' for _ in range(BOARD_SIZE)]


    board[7] = ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
    board[6] = ['wp' for _ in range(BOARD_SIZE)]

    return board



class ChessGame:
    def __init__(self):
        self.board = initialize_board()
        self.pieces = load_pieces()
        self.selected_piece = None
        self.valid_moves = []
        self.turn = 'w'  # Белые ходят первыми
        self.game_over = False
        self.winner = None

    def draw_board(self):

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


                if self.selected_piece and self.selected_piece == (row, col):
                    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight.fill(HIGHLIGHT)
                    screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))


                if (row, col) in self.valid_moves:
                    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight.fill(MOVE_HIGHLIGHT)
                    screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))


                piece = self.board[row][col]
                if piece:
                    screen.blit(self.pieces[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def get_piece_moves(self, row, col):
        piece = self.board[row][col]
        if not piece:
            return []

        color = piece[0]
        piece_type = piece[1]
        moves = []

        # Pawn
        if piece_type == 'p':
            direction = -1 if color == 'w' else 1
            start_row = 6 if color == 'w' else 1

            # Move forward one square
            if 0 <= row + direction < BOARD_SIZE and not self.board[row + direction][col]:
                moves.append((row + direction, col))

                # Move forward two squares from the starting position
                if row == start_row and not self.board[row + 2 * direction][col]:
                    moves.append((row + 2 * direction, col))

            # Taking diagonally
            for dcol in [-1, 1]:
                if 0 <= row + direction < BOARD_SIZE and 0 <= col + dcol < BOARD_SIZE:
                    target = self.board[row + direction][col + dcol]
                    if target and target[0] != color:
                        moves.append((row + direction, col + dcol))

        # Rook
        elif piece_type == 'r':
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dr, dc in directions:
                for i in range(1, BOARD_SIZE):
                    r, c = row + i * dr, col + i * dc
                    if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                        break

                    if not self.board[r][c]:
                        moves.append((r, c))
                    else:
                        if self.board[r][c][0] != color:
                            moves.append((r, c))
                        break


        elif piece_type == 'n':
            knight_moves = [
                (2, 1), (1, 2), (-1, 2), (-2, 1),
                (-2, -1), (-1, -2), (1, -2), (2, -1)
            ]
            for dr, dc in knight_moves:
                r, c = row + dr, col + dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if not self.board[r][c] or self.board[r][c][0] != color:
                        moves.append((r, c))


        elif piece_type == 'b':
            directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
            for dr, dc in directions:
                for i in range(1, BOARD_SIZE):
                    r, c = row + i * dr, col + i * dc
                    if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                        break

                    if not self.board[r][c]:
                        moves.append((r, c))
                    else:
                        if self.board[r][c][0] != color:
                            moves.append((r, c))
                        break


        elif piece_type == 'q':

            directions = [
                (0, 1), (1, 0), (0, -1), (-1, 0),
                (1, 1), (1, -1), (-1, -1), (-1, 1)
            ]
            for dr, dc in directions:
                for i in range(1, BOARD_SIZE):
                    r, c = row + i * dr, col + i * dc
                    if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                        break

                    if not self.board[r][c]:
                        moves.append((r, c))
                    else:
                        if self.board[r][c][0] != color:
                            moves.append((r, c))
                        break


        elif piece_type == 'k':
            king_moves = [
                (0, 1), (1, 1), (1, 0), (1, -1),
                (0, -1), (-1, -1), (-1, 0), (-1, 1)
            ]
            for dr, dc in king_moves:
                r, c = row + dr, col + dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if not self.board[r][c] or self.board[r][c][0] != color:
                        moves.append((r, c))

        return moves

    def select_piece(self, row, col):
        piece = self.board[row][col]


        if not piece or piece[0] != self.turn:
            self.selected_piece = None
            self.valid_moves = []
            return


        self.selected_piece = (row, col)
        self.valid_moves = self.get_piece_moves(row, col)

    def move_piece(self, row, col):
        if not self.selected_piece or (row, col) not in self.valid_moves:
            return False

        start_row, start_col = self.selected_piece
        piece = self.board[start_row][start_col]



        # We make a move
        self.board[row][col] = piece
        self.board[start_row][start_col] = ''


        self.turn = 'b' if self.turn == 'w' else 'w'


        self.selected_piece = None
        self.valid_moves = []

        return True

    def check_game_over(self):

        kings = {'w': False, 'b': False}

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece and piece[1] == 'k':
                    kings[piece[0]] = True

        if not kings['w']:
            self.game_over = True
            self.winner = 'Черные'
        elif not kings['b']:
            self.game_over = True
            self.winner = 'Белые'

    def draw_game_over(self):
        if self.game_over:
            font = pygame.font.SysFont('Arial', 50)
            text = font.render(f'{self.winner} победили!', True, (255, 0, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))


            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            screen.blit(text, text_rect)


            button_font = pygame.font.SysFont('Arial', 30)
            button_text = button_font.render('Новая игра', True, WHITE)
            button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)
            pygame.draw.rect(screen, (50, 50, 50), button_rect)
            pygame.draw.rect(screen, WHITE, button_rect, 2)
            screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2,
                                      button_rect.centery - button_text.get_height() // 2))

            return button_rect
        return None



def main():
    game = ChessGame()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE

                if game.game_over:
                    button_rect = game.draw_game_over()
                    if button_rect and button_rect.collidepoint(x, y):
                        game = ChessGame()  # Новая игра
                else:
                    if game.selected_piece:
                        if (row, col) in game.valid_moves:
                            game.move_piece(row, col)
                            game.check_game_over()
                        else:
                            game.select_piece(row, col)
                    else:
                        game.select_piece(row, col)

        
        screen.fill(BLACK)
        game.draw_board()

        if game.game_over:
            game.draw_game_over()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()