
class Piece(object):
    def __init__(self, row: int, column: int, side: str):
        self.row = row
        self.column = column
        self.side = side
        self.moved = False

    # def possible_moves(self):
    #     step = 1
    #     possible_steps = self.possible_steps
    #     remove_option = []
    #     result = []
    #     while possible_steps:
    #         for option in possible_steps:
    #             row, column = self.row + step * option[0], self.column + step * option[1]
    #             line_move = b.line_move(row, column, self.side)
    #             if not line_move[0]:
    #                 remove_option.append(option)
    #                 continue
    #             else:
    #                 result.append(line_move[0])
    #             if not line_move[1]:
    #                 remove_option.append(option)
    #         for option in remove_option:
    #             possible_steps.pop(possible_steps.index(option))
    #         step += 1
    #         if self.one_step:
    #             break
    #
    #     return result

class Pawn(Piece):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    name = 'pawn'
    worth = 1
    img = ['w_pawn_png_128px.png', 'b_pawn_png_128px.png']
    size = (53, 64)

    def __str__(self):
        return ' ' + str(self.letters[self.column]) + str(8 - self.row) + ' '

    def draw(self, win: object):
        if self.side == 'w':
            picture = pygame.image.load(os.path.join(image_dir, 'w_pawn_png_128px.png'))
        else:
            picture = pygame.image.load(os.path.join(image_dir, 'b_pawn_png_128px.png'))
        picture = pygame.transform.scale(picture, (53, 64))
        win.blit(picture, (square_size * self.x + 13, square_size * self.y + 8))

    def possible_moves(self):
        side = -1 if self.side == 'w' else 1
        result = []
        # possible_steps [[0,1 * side]]
        # if not self.moved: possible_steps.append([0,2*side])

        straight_move = (self.row, self.column + 1 * side)
        if b.is_on_board(self.row + 1 * side, self.row):
            if not b.board[self.row + 1 * side][self.column]:
                result.append([self.row + 1 * side, self.column, 'free'])
        if not self.moved:
            if not b.board[self.row + 2 * side][self.column] and not b.board[self.row + 1 * side][self.column]:
                result.append([self.row + 2 * side, self.column, 'free'])

        take_moves = [[self.row + 1 * side, self.column + 1, 'take'],
                      [self.row + 1 * side, self.column - 1, 'take']]
        for move in take_moves:
            if b.is_on_board(move[0], move[1]):
                if b.board[move[0]][move[1]] and board[move[0]][move[1]].side != self.side:
                    result.append(move)

        return result

class Rook(Piece):
    name = 'rook'
    one_step = 0
    img = ['w_rook_png_128px.png', 'b_rook_png_128px.png']
    size = (58, 64)
    possible_steps = ([1, 0], [-1, 0], [0, 1], [0, -1])

    def __str__(self):
        return self.side + ' ' + 'R' + ' '

    worth = 5

    def draw(self, win):
        if self.side == 'w':
            picture = pygame.image.load(os.path.join(image_dir, 'w_rook_png_128px.png'))
        else:
            picture = pygame.image.load(os.path.join(image_dir, 'b_rook_png_128px.png'))
        picture = pygame.transform.scale(picture, (58, 64))
        win.blit(picture, (square_size * self.x + 11, square_size * self.y + 8))

class Knight(Piece):
    name = 'knight'
    one_step = 1
    img = ['w_knight_png_128px.png', 'b_knight_png_128px.png']
    size = (58, 64)
    possible_steps = ([1, 2], [1, -2], [2, 1], [2, -1], [-1, 2], [-1, -2], [-2, 1], [-2, -1])

    def __str__(self):
        return self.side + ' ' + 'N' + ' '

    worth = 3

    def draw(self, win):
        if self.side == 'w':
            picture = pygame.image.load(os.path.join(image_dir, 'w_knight_png_128px.png'))
        else:
            picture = pygame.image.load(os.path.join(image_dir, 'b_knight_png_128px.png'))
        picture = pygame.transform.scale(picture, (58, 64))
        win.blit(picture, (square_size * self.x + 11, square_size * self.y + 8))

class Bishop(Piece):
    name = 'bishop'
    one_step = 0
    img = ['w_bishop_png_128px.png', 'b_bishop_png_128px.png']
    size = (64, 64)
    possible_steps = ([1, 1], [1, -1], [-1, -1], [-1, 1])

    def __str__(self):
        return self.side + ' ' + 'B' + ' '

    worth = 3

    def draw(self, win):
        if self.side == 'w':
            picture = pygame.image.load(os.path.join(image_dir, 'w_bishop_png_128px.png'))
        else:
            picture = pygame.image.load(os.path.join(image_dir, 'b_bishop_png_128px.png'))
        picture = pygame.transform.scale(picture, (64, 64))
        win.blit(picture, (square_size * self.x + 8, square_size * self.y + 8))

class Queen(Piece):
    name = 'queen'
    one_step = 0
    worth = 10
    img = ['w_queen_png_128px.png', 'b_queen_png_128px.png']
    size = (70, 64)
    possible_steps = ([1, 1], [1, -1], [-1, -1], [-1, 1], [1, 0], [-1, 0], [0, 1], [0, -1])

    def __str__(self):
        return self.side + ' ' + 'Q' + ' '

    def draw(self, win):
        if self.side == 'w':
            picture = pygame.image.load(os.path.join(image_dir, 'w_queen_png_128px.png'))
        else:
            picture = pygame.image.load(os.path.join(image_dir, 'b_queen_png_128px.png'))
        picture = pygame.transform.scale(picture, (70, 64))
        win.blit(picture, (square_size * self.x + 5, square_size * self.y + 8))

class King(Piece):
    name = 'queen'
    one_step = 1
    worth = 1000 # todo find some better solution
    img = ['w_king_png_128px.png', 'b_king_png_128px.png']
    size = (64, 64)
    possible_steps = ([1, 1], [1, -1], [-1, -1], [-1, 1], [1, 0], [-1, 0], [0, 1], [0, -1])

    def __str__(self):
        return self.side + ' ' + 'K' + ' '

    def draw(self, win):
        if self.side == 'w':
            picture = pygame.image.load(os.path.join(image_dir, 'w_king_png_128px.png'))
        else:
            picture = pygame.image.load(os.path.join(image_dir, 'b_king_png_128px.png'))
        picture = pygame.transform.scale(picture, (64, 64))
        win.blit(picture, (square_size * self.x + 8, square_size * self.y + 8))
