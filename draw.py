import pygame, os
from board import board as b
pygame.init()

class Window(object):
    def __init__(self):
        board_x = 50
        board_y = 40
        self.win = pygame.display.set_mode((740, 710))
        self.db = Draw_Board(board_x, board_y, self.win)
        self.dp = Draw_Pieces(board_x, board_y, self.win)
        self.dc = Draw_Cursor(board_x, board_y, self.win)
        pygame.display.set_caption('Chess by Mates')
        counter_font = pygame.font.SysFont('arial', 20, True)

    def redraw(self,cursors):
        self.win.fill((0, 0, 0))
        self.db.draw()
        self.dp.draw_all()
        self.dc.draw_all(cursors)
        pygame.display.update()

class Draw_Board(object):
    square_size = 80
    board_size = square_size * b.board_size

    def __init__(self, x, y, win):

        self.x, self.y = x, y
        self.win = win

    def draw(self):
        count = 1
        for row in range(b.board_size):
            for column in range(b.board_size):
                color = (200, 200, 200) if count % 2 else (55, 55, 55)
                pygame.draw.rect(self.win, color,(row * self.square_size + self.x,
                                                  column * self.square_size + self.y,
                                                  self.square_size, self.square_size))
                count += 1
            count += 1

class Draw_Cursor(Draw_Board):
    def __init__(self, x, y, win):
        self.x, self.y = x, y
        self.win = win

    def draw(self, cursor):
        if cursor.kind == 'main':
            if cursor.selected:
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)
        else:
            color = (255,255,0)
        position = (cursor.column * self.square_size + 2 + self.x,
                    cursor.row * self.square_size + 2 + self.y,
                    self.square_size - 5, self.square_size - 5)
        pygame.draw.rect(self.win, color, position, 2)

    def draw_positions(self,pos_moves):
        for move in pos_moves:
            color = (0,255,255) if move[2] == 'free' else (255,0,0)
            position = (move[1] * self.square_size + 2 + self.x,
                        move[0] * self.square_size + 2 + self.y,
                        self.square_size - 5, self.square_size - 5)
            pygame.draw.rect(self.win, color, position, 2)

    def draw_all(self, cursors):
        for cursor in cursors:
            if cursor.kind == 'position':
                self.draw_positions(cursor.possible_moves)
            self.draw(cursor)

class Draw_Pieces(Draw_Board):
    def __init__(self, x, y, win):
        self.x, self.y = x, y
        self.win = win

    def draw_piece(self,piece):
        piece_img = piece.img[0] if piece.side == 'w' else piece.img[1]
        img_load = pygame.image.load(os.path.join('img',piece_img))
        resize = piece.size
        img = pygame.transform.scale(img_load, resize)
        self.win.blit(img,(self.x + self.square_size * piece.column + ((80-resize[0])//2),
                           self.y + self.square_size * piece.row + ((80-resize[1])//2)))

    def draw_all(self):
        for line in b.board:
            for square in line:
                if square:
                    self.draw_piece(square)

window = Window()