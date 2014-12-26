# hw8.py
# Name: Weikun Liang
# Andrew ID: weikunl
# Section: G
# Collaborators: Zhongyuan Ying (zying), Peng Wen (pwen)

from Tkinter import *
import random

# Controller
def mousePressed(canvas,event):
    margin, cellSize = canvas.data.margin, canvas.data.cellSize
    # moves the whole board down 
    offset = canvas.data.offset
    if(canvas.data.gameType == 3):
        if(canvas.data.isPaused):
            # checks if the user clicked in any of the cells
            for row in xrange(canvas.data.rows):
                for col in xrange(canvas.data.cols):
                    if(event.x > margin+col*cellSize and
                       event.y > offset + margin+row*cellSize
                       and event.x < margin+(col+1)*cellSize and
                       event.y< offset + margin+(row+1)*cellSize):
                        # if there isn't a wall and there is nothing
                        # present at that cell, add a wall
                        if(canvas.data.isWall[row][col] == False and
                           canvas.data.snakeBoard[row][col] == 0):
                            canvas.data.snakeBoard[row][col] = -5
                            canvas.data.isWall[row][col] = True
                        # if there is a wall delete that wall
                        elif(canvas.data.isWall and
                             canvas.data.snakeBoard[row][col] == -5):
                            canvas.data.snakeBoard[row][col] = 0
                            canvas.data.isWall[row][col] = False
        redrawAllSnake(canvas)

# the key events for tetris
def keyOne(canvas, event):
    if (event.keysym == "Left"):
        moveFallingPiece(canvas, 0, -1)
    elif(event.keysym == "Right"):
        moveFallingPiece(canvas, 0, 1)
    elif(event.keysym == "Up"):
        rotateFallingPiece(canvas)
    elif(event.keysym == "Down"):
        moveFallingPiece(canvas, 1, 0)
    elif(event.keysym == "r"):
        init1(canvas)
        isGameOver = False
    redrawAll(canvas)

# the key events for the snakes
def keyTwo(canvas, event):
        if (event.char == "q"): gameOver(canvas)
        elif (event.char == "r"):
            init2(canvas)
        elif (event.char == "d"):
            canvas.data.inDebugMode = not canvas.data.inDebugMode
        if (canvas.data.isGameOverSnake == False):
            if (event.keysym == "Up"):
                moveSnake(canvas,-1, 0)
            elif (event.keysym == "Down"):
                moveSnake(canvas,+1, 0)
            elif (event.keysym == "Left"):
                moveSnake(canvas,0,-1)
            elif (event.keysym == "Right"):
                moveSnake(canvas,0,+1)
        redrawAllSnake(canvas)
        canvas.data.ignoreNextTimerEvent = True
        # adds the pause function for more snake
        if(canvas.data.gameType==3):
            if(event.keysym == "p"):
                canvas.data.isPaused = not canvas.data.isPaused

# the overall keypress function
def keyPressed(canvas,event):
    if(event.keysym == "1"):
        canvas.data.gameType=1
        init1(canvas)
    if(event.keysym == "2"):
        canvas.data.gameType=2
        init2(canvas)
    if(event.keysym == "3"):
        canvas.data.gameType=3
        init2(canvas)
    if(canvas.data.gameType == 1):
        keyOne(canvas, event)
    if(canvas.data.gameType==2 or canvas.data.gameType==3):
        keyTwo(canvas, event)

# the do timer fired for the tetris game       
def doTimeFired(canvas):
    if(moveFallingPiece(canvas,+1,0) == False):
        placeFallingPiece(canvas)
        removeFullRows(canvas)
        newFallingPiece(canvas)
        if(fallingPieceIsLegal(canvas) == False):
            canvas.data.isGameOver = True
    redrawAll(canvas)
    
def timerFired(canvas):
    if(canvas.data.gameType==1):
        if(canvas.data.isGameOver==False): doTimeFired(canvas)
    if(canvas.data.gameType==2):
        if(canvas.data.isGameOverSnake == False):
            ignoreThisTimerEvent = canvas.data.ignoreNextTimerEvent
            canvas.data.ignoreNextTimerEvent = False
            if(ignoreThisTimerEvent == False):
                moveSnake(canvas, canvas.data.snakeDrow, canvas.data.snakeDcol)
        redrawAllSnake(canvas)
    if(canvas.data.gameType==3):
        if(canvas.data.isGameOverSnake == False and
           canvas.data.isPaused == False):
            ignoreThisTimerEvent = canvas.data.ignoreNextTimerEvent
            canvas.data.ignoreNextTimerEvent = False
            if(ignoreThisTimerEvent == False):
                moveSnake(canvas, canvas.data.snakeDrow, canvas.data.snakeDcol)
        redrawAllSnake(canvas)
    # increases the speed when the user reaches the next level
    if(canvas.data.scoreSnake >= 3 and canvas.data.gameType == 3): delay = 150
    else: delay = 300 # milliseconds
    canvas.after(delay, lambda: timerFired(canvas))

# View
def drawCell(canvas, row, col, color):
    # adds some space to the left of the board
    c = (row + 2) * canvas.data.squareSize
    # adds some space to the top of the board
    r = (col + 2) * canvas.data.squareSize
    # draws the cells
    canvas.create_rectangle(r, c, r + canvas.data.squareSize,
                            c + canvas.data.squareSize, fill = "black")
    canvas.create_rectangle(r+canvas.data.border, c+canvas.data.border,
                            r + canvas.data.squareSize-canvas.data.border,
                            c + canvas.data.squareSize-canvas.data.border,
                            fill = color)

def drawBoard(canvas):
    # creates the orange background
    canvas.create_rectangle(0, 0, canvas.data.width, canvas.data.height,
                            width = 0, fill = "orange")
    # draws each of the cells
    for row in  xrange(len(canvas.data.board)):
        for col in xrange(len(canvas.data.board[0])):
            drawCell(canvas, row, col, canvas.data.board[row][col])

def drawGame(canvas):
    drawBoard(canvas)
    drawFallingPiece(canvas)
    
def redrawAll(canvas):
    if(canvas.data.isGameOver == False):
        canvas.delete(ALL)
        drawGame(canvas)
    else:
        # displays the game over text when the game's over
        canvas.create_text(canvas.data.width/2, 20,text="Game Over",
                           font="Helvetica 26 bold underline")
    drawScore(canvas)
    
def drawFallingPiece(canvas):
    # draws the falling piece if its value in its 2-d list is True
    for row in xrange(len(canvas.data.fallingPiece)):
        for col in xrange(len(canvas.data.fallingPiece[0])):
            if(canvas.data.fallingPiece[row][col] == True):
                drawCell(canvas, row + canvas.data.fallingPieceRow,
                         col + canvas.data.fallingPieceCol,
                         canvas.data.fallingPieceColor)

def drawScore(canvas):
    # displays the score
    canvas.create_text(canvas.data.width/2, canvas.data.height-20,
                       text="Score = " + str(canvas.data.score),
                       font="Helvetica 26 bold underline")

# Snake View
def redrawAllSnake(canvas):
    canvas.delete(ALL)
    drawSnakeBoard(canvas)
    textFont = "Helvetica", 32, "bold"
    if(canvas.data.isGameOverSnake == True):
        # displays the game over text
        canvas.create_text(100, 100, text="Game Over!", font=(textFont))
        if(canvas.data.gameType == 3):
            # displays the highscores if they are not zero
            if(canvas.data.highScore1 != 0):
                canvas.create_text(150, 150,
                text="High Score = "+str(canvas.data.highScore1), font=textFont)
            if(canvas.data.highScore2 != 0):
                canvas.create_text(150, 200,
                text="High Score = "+str(canvas.data.highScore2), font=textFont)
            if(canvas.data.highScore3 != 0):
                canvas.create_text(150, 250,
                text="High Score = "+str(canvas.data.highScore3), font=textFont)
    # displays the score
    if(canvas.data.gameType == 3):    
        canvas.create_text(canvas.data.width/2,20,
                           text="Score = "+str(canvas.data.scoreSnake),
                           font=textFont)

# sets the highscores at the end of a game     
def addHighScore(canvas, score):
    if (score > canvas.data.highScore1):
        canvas.data.highScore3 = canvas.data.highScore2
        canvas.data.highScore2 = canvas.data.highScore1
        canvas.data.highScore1 = score
    elif(score > canvas.data.highScore2):
        canvas.data.highScore3 = canvas.data.highScore2
        canvas.data.highScore2 = score
    elif(score > canvas.data.highScore3):
        canvas.data.highScore3 = score

# draws the snake board
def drawSnakeBoard(canvas):
    for row in xrange(len(canvas.data.snakeBoard)):
        for col in xrange(len(canvas.data.snakeBoard[0])):
            drawSnakeCell(canvas, canvas.data.snakeBoard, row, col)

# draws the snake, food, poison, and cell based on whether the game is on
# pause or not
def draw(canvas, row, col, left, top, margin, cellSize, offset):
    snakeBoard = canvas.data.snakeBoard
    color1, color2, color3, color4 = "blue", "green", "white", "red"
    # if the game is paused, sets the colors to a lighter color
    if(canvas.data.isPaused and canvas.data.gameType == 3):
        color1 , color2 = "light blue", "light green"
        color3, color4 = "gray", "pink"
    canvas.create_rectangle(left, offset + top, left + cellSize,
                            offset + top+ cellSize, fill = color3)
    if(snakeBoard[row][col] > 0):
        canvas.create_oval(left, offset + top, left + cellSize,
                            offset + top+ cellSize, fill = color1)
    if(snakeBoard[row][col] == -1):
        canvas.create_oval(left, offset + top, left + cellSize,
                            offset + top+ cellSize, fill = color2)
    if(snakeBoard[row][col] == -2):
        canvas.create_oval(left, offset + top, left + cellSize,
                            offset + top+ cellSize, fill = color4)
    if(snakeBoard[row][col] == -5):
        canvas.create_rectangle(left, offset + top, left + cellSize,
                            offset + top+ cellSize, fill = "brown")

def drawSnakeCell(canvas, snakeBoard, row, col):
    margin, cellSize = canvas.data.margin, canvas.data.cellSize
    left, top = margin + cellSize*col, margin + cellSize*row
    offset = canvas.data.offset
    # moves the snake board down(to add space to diaplay the score)
    # if the user is playing more snake
    if(canvas.data.gameType == 3): offset = 50
    else: offset = 0
    draw(canvas, row, col, left, top, margin, cellSize, offset)
    # dispays the bakground numbers for debugging
    if (canvas.data.inDebugMode == True):
        canvas.create_text(left+cellSize/2,offset +
                           margin + cellSize*row+cellSize/2,
                            text=str(canvas.data.snakeBoard[row][col]),
                            font=("Helvatica", 14, "bold"))

def loadSnakeBoard(canvas):
    # creates the snake board
    canvas.data.snakeBoard = []
    for row in xrange(canvas.data.rows):
        canvas.data.snakeBoard += [[0]*canvas.data.cols]
    canvas.data.snakeBoard[canvas.data.rows/2][canvas.data.cols/2] = 1
    findSnakeHead(canvas)
    placeFood(canvas)
    canvas.data.ignoreNextTimerEvent = False

def printInstructions():
    print "Snake!"
    print "Use the arrow keys to move the snake."
    print "Eat food to grow."
    print "Stay on the board!"
    print "And don't crash into yourself!"
    print "And don't crash into yourself!"
    print "Press 'd' for debug mode."
    print "Press 'r' to restart."
    
def findSnakeHead(canvas):
    headRow, headCol = 0, 0
    # find the largest value in the board
    for row in xrange(len(canvas.data.snakeBoard)):
        for col in xrange(len(canvas.data.snakeBoard[0])):
            if(canvas.data.snakeBoard[row][col] >
               canvas.data.snakeBoard[headRow][headCol]):
                headRow = row
                headCol = col
    canvas.data.headRow = headRow
    canvas.data.headCol = headCol

def removeTail(canvas):
    # subtracts one from each value
    for row in xrange(len(canvas.data.snakeBoard)):
        for col in xrange(len(canvas.data.snakeBoard[0])):
            if(canvas.data.snakeBoard[row][col] > 0):
                canvas.data.snakeBoard[row][col] -= 1
 
def check(canvas):
    # checks if we should place poison on the board
    if(canvas.data.scoreSnake == 3 and canvas.data.placePoison == True
       and canvas.data.gameType == 3):
        placePoison(canvas)
        canvas.data.placePoison = False
     
def checkWall(canvas):
    # add wall points if there is a wall and the user ate food
    if(hasWall):
        canvas.data.wallPoint += 1
        if(canvas.data.wallPoint == 20):
            canvas.data.scoreSnake += 1
            canvas.data.wallPoint = 0

# when the snake eats food
def eat(canvas, snakeBoard, newHeadRow, newHeadCol):
    hRow, hCol = canvas.data.headRow, canvas.data.headCol
    snakeBoard[newHeadRow][newHeadCol] = snakeBoard[hRow][hCol]+1
    hRow, hCol = newHeadRow, newHeadCol
    canvas.data.scoreSnake += 1
    canvas.data.snakeBoard = snakeBoard
    canvas.data.headRow, canvas.data.headCol = hRow, hCol
    checkWall(canvas)
    placeFood(canvas)

# moves the snake
def moveSnake(canvas, drow, dcol):
    hRow, hCol = canvas.data.headRow, canvas.data.headCol
    newHeadRow, newHeadCol = hRow + drow, hCol + dcol
    snakeBoard = canvas.data.snakeBoard
    canvas.data.snakeDrow, canvas.data.snakeDcol = drow, dcol
    check(canvas)
    # checks for game over
    if(newHeadRow<0 or newHeadCol<0 or newHeadRow>=len(snakeBoard)
       or newHeadCol>=len(snakeBoard[0])): gameOver(canvas)
    elif(snakeBoard[newHeadRow][newHeadCol] > 0): gameOver(canvas)
    elif(snakeBoard[newHeadRow][newHeadCol] == -1):
        eat(canvas, snakeBoard, newHeadRow, newHeadCol)
    elif(snakeBoard[newHeadRow][newHeadCol] == -2): gameOver(canvas)
    else: 
        snakeBoard[newHeadRow][newHeadCol] = snakeBoard[hRow][hCol]+1
        hRow, hCol = newHeadRow, newHeadCol
        removeTail(canvas)
        if(canvas.data.scoreSnake < 0): gameOver(canvas)
        canvas.data.snakeBoard = snakeBoard
        canvas.data.headRow, canvas.data.headCol = hRow, hCol

# check if there is a wall present on the board    
def hasWall(canvas):
    count = 0
    for row in xrange(len(canvas.data.isWall)):
        for col in xrange(len(canvas.data.isWall[0])):
            if(canvas.data.isWall[row][col] == True):
                count += 1
    return (count > 0)

# game over for snake    
def gameOver(canvas):
    canvas.data.isGameOverSnake = True
    addHighScore(canvas, canvas.data.scoreSnake)
    canvas.data.placePoison = True

# places food in a random location on the board   
def placeFood(canvas):
    randRow = random.randint(0,len(canvas.data.snakeBoard)-1)
    randCol = random.randint(0, len(canvas.data.snakeBoard[0])-1)
    while(canvas.data.snakeBoard[randRow][randCol] > 0 and
          canvas.data.snakeBoard[randRow][randCol] == -2):
        randRow = random.randint(0,len(canvas.data.snakeBoard)-1)
        randCol = random.randint(0, len(canvas.data.snakeBoard[0])-1)
    canvas.data.snakeBoard[randRow][randCol] = -1

# places poison in a random location on the board
# except infront of its head
def placePoison(canvas):
    findSnakeHead(canvas)
    randRow = random.randint(0,len(canvas.data.snakeBoard)-1)
    randCol = random.randint(0, len(canvas.data.snakeBoard[0])-1)
    while(canvas.data.snakeBoard[randRow][randCol] > 0 and
          canvas.data.snakeBoard[randRow][randCol] == -1 and
          randRow != canvas.data.headRow+canvas.data.snakeDrow and
          randCol != canvas.data.headCol+canvas.data.snakeDcol):
        randRow = random.randint(0,len(canvas.data.snakeBoard)-1)
        randCol = random.randint(0, len(canvas.data.snakeBoard[0])-1)
    canvas.data.snakeBoard[randRow][randCol] = -2
    
# Model
# makes a new falling piece
def newFallingPiece(canvas):
    col = len(canvas.data.fallingPiece[0])
    piece = random.randint(0,len(canvas.data.tetrisPieces)-1)
    canvas.data.fallingPiece = canvas.data.tetrisPieces[piece]
    canvas.data.fallingPieceColor = canvas.data.tetrisPieceColors[piece]
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceCol = canvas.data.cols/2 - col/2

def moveFallingPiece(canvas, drow, dcol):
    canvas.data.fallingPieceCol += dcol
    canvas.data.fallingPieceRow += drow
    if(fallingPieceIsLegal(canvas) == False):
        canvas.data.fallingPieceCol -= dcol
        canvas.data.fallingPieceRow -= drow
        return False
    return True

# checks if the faaling piece is legal
def fallingPieceIsLegal(canvas):
    r = canvas.data.fallingPieceRow
    c = canvas.data.fallingPieceCol
    if(r < 0 or c < 0 or r > canvas.data.rows - len(canvas.data.fallingPiece)
       or c > canvas.data.cols- len(canvas.data.fallingPiece[0])):
        return False
    for row in xrange(len(canvas.data.fallingPiece)):
        for col in xrange(len(canvas.data.fallingPiece[0])):
            if(canvas.data.fallingPiece[row][col] == True):
                if(canvas.data.board[row + r][col + c]!= "blue"
                   or row+r<0 or col+c<0
                   or row+r >= canvas.data.rows or col+c >= canvas.data.cols):
                    return False
    return True

# rotates it counterclockwise
def rotateFallingPiece(canvas):
    fallingPiece = canvas.data.fallingPiece
    pieceRow = canvas.data.fallingPieceRow
    pieceCol = canvas.data.fallingPieceCol
    numRow = len(canvas.data.fallingPiece)
    numCol = len(canvas.data.fallingPiece[0])
    newRow, newCol = numCol, numRow
    (oldCenterRow, oldCenterCol) = fallingPieceCenter(canvas)
    newPiece = []
    for r in xrange(newRow):
        newPiece += [[0]* newCol]
    for row in xrange(newCol):
        for col in xrange(newRow-1, -1, -1):
            newPiece[newRow-1-col][row] = fallingPiece[row][col]
    canvas.data.fallingPiece = newPiece
    (newCenterRow, newCenterCol) = fallingPieceCenter(canvas)
    if(fallingPieceIsLegal(canvas)==False):
        canvas.data.fallingPiece = fallingPiece

# finds the center of the falling piece
def fallingPieceCenter(canvas):
    row = canvas.data.fallingPieceRow + (len(canvas.data.fallingPiece))/2
    col = canvas.data.fallingPieceCol + (len(canvas.data.fallingPiece[0]))/2
    return (row, col)

def placeFallingPiece(canvas):
    r = canvas.data.fallingPieceRow
    c = canvas.data.fallingPieceCol
    color = canvas.data.fallingPieceColor
    for row in xrange(len(canvas.data.fallingPiece)):
        for col in xrange(len(canvas.data.fallingPiece[0])):
            if(canvas.data.fallingPiece[row][col] == True):
                canvas.data.board[row + r][col + c] = color

def removeFullRows(canvas):
    newBoard = []
    count = 0
    for row in xrange(canvas.data.rows):
        newBoard += [["blue"]*canvas.data.cols]
    newRow = canvas.data.rows-1
    for oldRow in xrange(canvas.data.rows-1, 0, -1):
        if(canvas.data.board[oldRow].count("blue") != 0):
            newBoard[newRow] = canvas.data.board[oldRow]
            newRow -= 1
        else: count += 1
    canvas.data.board = newBoard
    canvas.data.score += count**2
    
def loadPiece(canvas):
    iPiece = [ [ True,  True,  True,  True] ]
    jPiece = [ [ True, False, False ],
               [ True, True,  True] ] 
    lPiece = [ [ False, False, True],
               [ True,  True,  True] ]
    oPiece = [ [ True, True],
               [ True, True] ]
    sPiece = [ [ False, True, True],
               [ True,  True, False ] ]
    tPiece = [ [ False, True, False ],
               [ True,  True, True] ]
    zPiece = [ [ True,  True, False ],
               [ False, True, True] ]
    tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan",
                         "green", "orange" ]
    canvas.data.tetrisPieces = tetrisPieces
    canvas.data.tetrisPieceColors = tetrisPieceColors

def init(canvas):
    row = canvas.data.rows
    col = canvas.data.cols
    canvas.data.gameType = 0
    canvas.data.scoreSnake = 0
    canvas.data.margin, canvas.data.cellSize = 5,30
    canvas.data.offset = 30
    if(canvas.data.gameType ==2 or canvas.data.gameType == 3):
        row = min(row, col)
        col = min(row, col)
    canvas.data.rows = row
    canvas.data.cols = col
    canvas.create_text(canvas.data.width/2,canvas.data.height/2,\
                       text="Press 1 to play Tetris\nPress 2 to play Snake\n\
Press 3 to play More Snake",font="Helvetica 27")

def init1(canvas):
    emptyColor = "blue"
    board = []
    for row in xrange(canvas.data.rows):
        board += [[emptyColor]*canvas.data.cols]
    loadPiece(canvas)
    canvas.data.emptyColor, canvas.data.board = emptyColor, board
    canvas.data.border, canvas.data.score = 2, 0
    canvas.data.startLeft, canvas.data.startTop = 20, 20
    canvas.data.fallingPiece = canvas.data.tetrisPieces[2]
    canvas.data.fallingPieceColor = canvas.data.tetrisPieceColors[2]
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceCol = canvas.data.cols/2 - 1
    canvas.data.isGameOver = False
    redrawAll(canvas)

def init2(canvas):  
    canvas.data.headRow, canvas.data.headCol = -1, -1
    canvas.data.snakeDrow,canvas.data.snakeDcol,canvas.data.scoreSnake = 0,-1,0
    printInstructions()
    loadSnakeBoard(canvas)
    canvas.data.inDebugMode, canvas.data.isGameOverSnake = False, False
    canvas.data.isGameOverSolo = False
    canvas.data.isGameOverSnake = False
    canvas.data.isWall = []
    canvas.data.wallPoint = 0
    for row in xrange(canvas.data.rows):
        canvas.data.isWall += [[False]*canvas.data.cols]
    canvas.data.highScore1 = canvas.data.highScore2 = canvas.data.highScore3 = 0
    redrawAllSnake(canvas)

def run(row,col):
    # create the root and the canvas
    root = Tk()
    margin, squareSize = 20, 25
    canvasWidth = margin*5 + col*squareSize
    canvasHeight = margin*5 + row*squareSize
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.resizable(width=0, height=0)
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width, canvas.data.height = canvasWidth, canvasHeight
    canvas.data.rows, canvas.data.cols = row, col
    canvas.data.squareSize, canvas.data.gameType = squareSize, 0
    canvas.data.isPaused, canvas.data.placePoison = False, True
    init(canvas)
    # set up events
    root.bind("<Button-1>", lambda event: mousePressed(canvas, event))
    root.bind("<Key>", lambda event: keyPressed(canvas, event))
    timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS

run(10,15)