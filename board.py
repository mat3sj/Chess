from pieces import *

class My_Board(object):
    board_size = 8

    def __init__(self):
        self.board = []
        for _i in range(self.board_size):
            line = []
            for _j in range(self.board_size):
                line.append('')
            self.board.append(line)
        self.fill_with_pieces()

    def fill_with_pieces(self):
        side = 'b'
        for row in [0,1,6,7]:
            if row == 6:
                side = 'w'
            if row in [1,6]:
                for column in range(self.board_size):
                    self.board[row][column] = Pawn(row,column,side)
            if row in [0,7]:
                self.board[row][0], self.board[row][7] = Rook(row,0,side), Rook(row,7,side)
                self.board[row][1], self.board[row][6] = Knight(row,1,side), Knight(row,6,side)
                self.board[row][2], self.board[row][5] = Bishop(row,2,side), Bishop(row,5,side)
                self.board[row][3] = Queen(row,3,side)
                self.board[row][4] = King(row,4,side)

    def is_on_board(self, row, column):
        if row >= self.board_size or column >= self.board_size: return False
        if row < 0 or column < 0: return False
        return True

    def line_move(self, row: int, column: int, side: str):
        if not self.is_on_board(row,column):
            return False, False

        square = self.board[row][column]
        if square:
            if square.side == side:
                return False, False
            else:
                return (row, column, 'take'), False
        else:
            return (row, column, 'free'), True

    def possible_moves(self, piece):
        '''Returns a list of possible moves of given piece.
        Each element in the list is a tuple in format: (row, column, take/free)'''
        if piece.name == 'pawn':
            return self.pawn_possible_moves(piece)

        step = 1
        possible_steps = list(piece.possible_steps)
        result = []
        while possible_steps:
            remove_options = []
            for option in possible_steps:
                row, column = piece.row + step * option[0], piece.column + step * option[1]
                line_move = self.line_move(row, column, piece.side)
                if not line_move[0]:
                    remove_options.append(option)
                    continue
                else:
                    result.append(line_move[0])
                if not line_move[1]:
                    remove_options.append(option)
            for option in remove_options:
                possible_steps.pop(possible_steps.index(option))
            step += 1
            if piece.one_step:
                break
        return result

    def pawn_possible_moves(self, pawn):
        side = -1 if pawn.side == 'w' else 1
        result = []

        if self.is_on_board(pawn.row + 1 * side, pawn.row):
            if not self.board[pawn.row + 1 * side][pawn.column]:
                result.append((pawn.row + 1 * side, pawn.column, 'free'))
        if not pawn.moved:
            if not self.board[pawn.row + 2 * side][pawn.column] and not self.board[pawn.row + 1 * side][pawn.column]:
                result.append((pawn.row + 2 * side, pawn.column, 'free'))

        take_moves = [(pawn.row + 1 * side, pawn.column + 1, 'take'),
                      (pawn.row + 1 * side, pawn.column - 1, 'take')]
        for move in take_moves:
            if self.is_on_board(move[0], move[1]):
                if self.board[move[0]][move[1]] and self.board[move[0]][move[1]].side != pawn.side:
                    result.append(move)
        return result

    def piece_move(self,cur_row, cur_column, row, column):
        piece = self.board[cur_row][cur_column]
        # print (main_cursor.row, '   ', main_cursor.column)
        if self.board[row][column]:
            taken_piece = self.board[row][column]
            # todo fix score
            self.board[row][column] = ''
            del taken_piece # todo move it to the side instead
        piece.moved = True
        self.board[row][column] = piece
        piece.row = row
        piece.column = column
        self.board[cur_row][cur_column] = ''

    def is_check(self, piece):
        side = piece.side
        row, column = None, None
        for line in self.board:
            if not row:
                for square in line:
                    if square:
                        if square.side == side and square.name == 'king':
                            row, column = square.row, square.column
                            print(square)
                            break

        for line in self.board:
            for square in line:
                if square:
                    possible_moves = self.possible_moves(square)
                    for move in possible_moves:
                        if move[0] == row and move[1] == column:
                            return True
        return False

    def print_to_terminal(self):
        template_lst = ['']
        for _cell in range(self.board_size):
            template_lst.append('{}')
        template_lst.append('')
        template = '|'.join(template_lst)
        print('-' * self.board_size * 5)
        for line in self.board:
            line_to_print = []
            for cell in line:
                if not cell:
                    line_to_print.append(' ' * 4)
                else:
                    line_to_print.append(cell)
            print(template.format(*line_to_print))
            print('-' * self.board_size * 5)

class My_Cursor(object):
    def __init__(self, row, column, kind):
        self.row = row
        self.column = column
        self.selected = False
        self.kind = kind
        if kind == 'position':
            self.possible_moves = board.possible_moves(board.board[row][column])


board = My_Board()
main_cursor = My_Cursor(2,1,"main")
