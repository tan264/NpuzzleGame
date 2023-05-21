import pygame, sys, random
from pygame.locals import *
import threading
from a_star import guide
from tkinter import messagebox

# Khai báo các hằng số
BOARDWIDTH = 3  
BOARDHEIGHT = 3 
TILESIZE = 80 # Kích thước mỗi ô
WINDOWWIDTH = 640 # Độ rộng cửa sổ game
WINDOWHEIGHT = 480 # Độ cao cửa sổ game
FPS = 30
BLANK = 0 # Tượng trưng cho ô trống(0)
LEVEL = 80 # Số lần tráo. VD: ở đây sẽ tráo 80 lần.

# Thiết đặt các màu sẽ dùng
#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)

# Thiết đặt màu cho các đối tượng sẽ hiển thị
BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

# Toạ độ của bảng game
XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, GUIDE_SURF, GUIDE_RECT, ABOUT_SURF, ABOUT_RECT, MOVES
    MOVES = 0
    # Thiết đặt các đối tượng trên giao diện
    pygame.init()
    img = pygame.image.load('res/icon.png')
    pygame.display.set_icon(img)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    
    GUIDE_SURF, GUIDE_RECT = makeText('Guide',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 150)
    RESET_SURF, RESET_RECT = makeText('Reset',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 120)
    NEW_SURF,   NEW_RECT   = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    ABOUT_SURF, ABOUT_RECT = makeText('About', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

    mainBoard, solutionSeq = generateNewPuzzle(LEVEL)
    SOLVEDBOARD = getStartingBoard() # bảng đích
    allMoves = [] # lưu danh sách các bước di chuyển mà người dùng thực hiện

    while True: # vòng lặp chính của trò chơi
        slideTo = None # hướng di chuyển
        msg = 'Click tile or press arrow keys to slide.' # đoạn text sẽ xuất hiện phía trái trên cùng của màn hình
        if mainBoard == SOLVEDBOARD: # kiểm tra đã được giải hay chưa
            msg = 'Solved!'

        drawBoard(mainBoard, msg)

        checkForQuit()
        for event in pygame.event.get(): # bắt các sự kiện gây ra từ người dùng
            if event.type == MOUSEBUTTONUP: # nếu người dùng dùng chuột click
                
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1]) # bắt toạ độ người dùng click

                if (spotx, spoty) == (None, None): # nếu toạ độ không nằm trong các ô thì có thể là nhấn vào các text bên phải màn hình
                    if RESET_RECT.collidepoint(event.pos): # nhấn vào nút Reset
                        MOVES = 0
                        resetAnimation(mainBoard, allMoves) 
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos): # nhấn vào nút New game
                        MOVES = 0
                        mainBoard, solutionSeq = generateNewPuzzle(LEVEL) 
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos): # nhấn vào nút Solve  
                        if (mainBoard == SOLVEDBOARD):
                            continue
                        MOVES = 0
                        resetAnimation(mainBoard, solutionSeq + allMoves)                   
                        allMoves = []
                    elif GUIDE_RECT.collidepoint(event.pos): # nhấn vào nút Guide
                        if (mainBoard == SOLVEDBOARD):
                            continue
                        x = threading.Thread(target=guide, args=(mainBoard,))
                        x.start()
                    elif ABOUT_RECT.collidepoint(event.pos): # nhấn vào nút About           
                        showAboutDialog()                     
                else: # nếu toạ độ là các ô
                    MOVES += 1
                    blanky, blankx = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

            elif event.type == KEYUP: # nếu người dùng dùng phím điều hướng
                MOVES += 1
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN

        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8) # hiển thị animation
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo) # thêm cách thức di chuyển vào allMoves
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # bắt sự kiện thoát ứng dụng(ấn X)
        terminate() # dừng ứng dụng
    for event in pygame.event.get(KEYUP): # bắt các sự kiện bởi người dùng
        if event.key == K_ESCAPE:
            terminate() # nếu là phím Esc thì cũng thoát ứng dụng
        pygame.event.post(event) # Nếu không phải nút Esc thì post lại sự kiện để thực thi logic theo sự kiện đó


def getStartingBoard(): # sinh ma trận ban đầu(=ma trận đích)
    counter = 1
    board = []
    for row in range(BOARDHEIGHT):
        row = []
        for col in range(BOARDWIDTH):
            row.append(counter)
            counter += 1
        board.append(row)

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK
    return board


def getBlankPosition(board): # lấy toạ độ điểm blank
    for row in range(BOARDHEIGHT):
        for col in range(BOARDWIDTH):
            if board[row][col] == BLANK:
                return (row, col)


def makeMove(board, move):
    # Di chuyển theo move được truyền vào
    blanky, blankx = getBlankPosition(board)

    if move == UP:
        board[blanky][blankx], board[blanky + 1][blankx] = board[blanky + 1][blankx], board[blanky][blankx]
    elif move == DOWN:
        board[blanky][blankx], board[blanky - 1][blankx] = board[blanky - 1][blankx], board[blanky][blankx]
    elif move == LEFT:
        board[blanky][blankx], board[blanky][blankx + 1] = board[blanky][blankx + 1], board[blanky][blankx]
    elif move == RIGHT:
        board[blanky][blankx], board[blanky][blankx - 1] = board[blanky][blankx - 1], board[blanky][blankx]


def isValidMove(board, move):
    blanky, blankx = getBlankPosition(board)
    return (move == UP and blanky != len(board) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board[0]) - 1) or \
           (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
    # bắt đầu với đù 4 cách thức di chuyển
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # xoá dần các cách thức chuyển không hợp lệ với board được truyền vào
    if lastMove == UP or not isValidMove(board, DOWN): # Nếu bước di chuyển trước là UP thì bước di chuyển lần này không thể là DOWN hoặc board hiện tại không thể DOWN
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP): # Nếu bước di chuyển trước là DOWN thì bước di chuyển lần này không thể là UP hoặc board hiện tại không thể UP
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT): # Nếu bước di chuyển trước là LEFT thì bước di chuyển lần này không thể là RIGHT hoặc board hiện tại không thể RIGHT
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT): # Nếu bước di chuyển trước là RIGHT thì bước di chuyển lần này không thể là LEFT hoặc board hiện tại không thể LEFT
        validMoves.remove(LEFT)

    # khi validMoves chỉ còn đúng các cách thức di chuyển hợp lệ thì chọn 1 trong số chúng
    return random.choice(validMoves)


def getLeftTopOfTile(tileX, tileY): # Nhận toạ độ ô trong board và trả về toạ độ của đỉnh trái phía trên của ô đó trên màn hình
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y): # Từ toạ độ pixel nhấn trên màn hình trả về toạ độ ô tương ứng trong board
    for tileY in range(len(board)):
        for tileX in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y): # kiểm tra toạ độ pixel truyền vào có nằm trong ô này không
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, adjx=0, adjy=0): # vẽ ô từ toạ độ đỉnh trái phía trên của nó
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left): # thiết lập giao diện cho chữ
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message): # thiết lập giao diện hiển thị board và message và các text
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    movesSurf, movesRect = makeText(str(MOVES), MESSAGECOLOR, BGCOLOR, WINDOWWIDTH - 35, 5)
    DISPLAYSURF.blit(movesSurf, movesRect)
    for tiley in range(len(board)):
        for tilex in range(len(board[0])):
            if board[tiley][tilex]:
                drawTile(tilex, tiley, board[tiley][tilex])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)
    DISPLAYSURF.blit(GUIDE_SURF, GUIDE_RECT)
    DISPLAYSURF.blit(ABOUT_SURF, ABOUT_RECT)

def slideAnimation(board, direction, message, animationSpeed): # hiển thị animation di chuyển ô

    blanky, blankx = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movey][movex], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movey][movex], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movey][movex], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movey][movex], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides): # Tráo bảng ban đầu với numSlides lần
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500) # đợi 500ms trước khi tráo
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(TILESIZE / 3))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves): # Đi ngược lại các cách thức di chuyển trong allMoves
    revAllMoves = allMoves[:] # tạo một bản sao của allMoves
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2))
        makeMove(board, oppositeMove)

def showAboutDialog():
    message = "Contributors:\n\nLương Vĩnh Lợi\nHoàng Đình Trung\nPhạm Duy Phú\nĐặng Hữu Tấn"     
    messagebox.showinfo(title='About', message= message) 

if __name__ == '__main__':
    main()