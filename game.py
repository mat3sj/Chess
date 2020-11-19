import pygame
from draw import window as win
import board as b

pygame.init()

run = True
key_loop = 0
pressed_key = False
move_count = 1
sides = ('w', 'b')
m_cursor = b.My_Cursor(7,3,'main')
cursors = [m_cursor]
board_size = b.board.board_size

win.redraw(cursors)
while run:
    keys = pygame.key.get_pressed()
    pygame.time.delay(40)

    if key_loop > 0:
        key_loop += 1
    if key_loop > 3:
        key_loop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if keys[pygame.K_p]:
        b.board.print_to_terminal()

    # main cursor movement
    if not m_cursor.selected:
        if keys[pygame.K_RIGHT] and not key_loop:
            pressed_key, key_loop = True, 1
            if m_cursor.column < board_size - 1:
                m_cursor.column += 1
        if keys[pygame.K_LEFT] and not key_loop:
            pressed_key, key_loop = True, 1
            if m_cursor.column > 0:
                m_cursor.column -= 1
        if keys[pygame.K_UP] and not key_loop:
            pressed_key, key_loop = True, 1
            if m_cursor.row > 0:
                m_cursor.row -= 1
        if keys[pygame.K_DOWN] and not key_loop:
            pressed_key, key_loop = True, 1
            if m_cursor.row < board_size - 1:
                m_cursor.row += 1

    # cursor movement when piece is selected
    else:
        if keys[pygame.K_RIGHT] and not key_loop:
            pressed_key, key_loop = True, 1
            if pos_cursor.column < board_size - 1:
                pos_cursor.column += 1
        if keys[pygame.K_LEFT] and not key_loop:
            pressed_key, key_loop = True, 1
            if pos_cursor.column > 0:
                pos_cursor.column -= 1
        if keys[pygame.K_UP] and not key_loop:
            pressed_key, key_loop = True, 1
            if pos_cursor.row > 0:
                pos_cursor.row -= 1
        if keys[pygame.K_DOWN] and not key_loop:
            pressed_key, key_loop = True, 1
            if pos_cursor.row < board_size - 1:
                pos_cursor.row += 1

    # selection
    cur_square = b.board.board[m_cursor.row][m_cursor.column]
    if cur_square and not key_loop:
        if cur_square.side == sides[move_count % 2 - 1]:
            if keys[pygame.K_KP_ENTER] or keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                pressed_key, key_loop = True, 1
                if m_cursor.selected:
                    for move in pos_cursor.possible_moves:
                        if pos_cursor.row == move[0] and pos_cursor.column == move[1]:
                            b.board.piece_move(m_cursor.row, m_cursor.column,
                                               pos_cursor.row, pos_cursor.column)
                            move_count += 1
                            m_cursor.selected = False
                            cursors.pop()
                            del pos_cursor
                            break
                    try:
                        if pos_cursor.row == m_cursor.row and pos_cursor.column == m_cursor.column:
                            m_cursor.selected = False
                            cursors.pop()
                            del pos_cursor
                    except:
                        pass
                else:
                    m_cursor.selected = True
                    print(b.board.is_check(b.board.board[m_cursor.row][m_cursor.column]))
                    pos_cursor = b.My_Cursor(m_cursor.row, m_cursor.column, 'position')
                    cursors.append(pos_cursor)

    if pressed_key:
        win.redraw(cursors)
        pressed_key = False

pygame.quit()
