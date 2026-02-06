import copy
import math
import random
import tkinter as tk
import tkinter.ttk as ttk

numReqForBirth = [3]
numReqForLife = [2,3]
board = [[]]
#Width of board on screen
WIDTH = 400
isPlaying = True


def createCells():
    """Make squares for board to represent empty and used cells"""
    size = WIDTH / boardSize.get()
    for y in range(boardSize.get()):
        for x in range(boardSize.get()):
            cells[y][x] = tkBoard.create_rectangle(
                x*size+1, y*size+1,
                (x+1)*size-1, (y+1)*size-1,
                fill="#9edede", outline=""
            )

def initialiseEmptyBoard():
    """Initialise the board as empty"""
    global board
    board = [[0] * boardSize.get() for i in range(boardSize.get())]
    drawBoard()

def initialiseRandomBoard():
    """Initialise the board with a random configuration based on numOfSeeds"""
    global board
    board= [[0] * boardSize.get() for i in range(boardSize.get())]
    for seed in range(numOfSeeds.get()):
        randX = random.randint(0,boardSize.get()-1)
        randY = random.randint(0,boardSize.get()-1)
        while board[randX][randY] == 1:
            randX = random.randint(0,boardSize.get()-1)
            randY = random.randint(0,boardSize.get()-1)
        board[randX][randY] = 1
    drawBoard()


def initialiseWindow():
    """Create Tkinter window"""
    window = tk.Tk()
    window.geometry("610x420")
    screen = tk.Frame(window)
    screen.grid()
    return screen 

def countNeighbours(x,y):
    """
    Count the number of alive cells adjacent to cell.
    Args:
        x: x coordinate of cell being checked
        y: y coordinate of cell being checked

    Returns:
        int: number of neighbours
    """
    
    count = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if i == 0 and j == 0:
                continue
            nx = (i + x) %boardSize.get()
            ny = (y + j) % boardSize.get() 
            count +=  board[nx][ny] 
    return count

def updateBoard():
    """
    Simlate one round of the game of life
    Returns:
        new board configuration
    """
    nextBoard = copy.deepcopy(board)
    for i in range(boardSize.get()):
        for j in range(boardSize.get()):
            numOfNeighbours = countNeighbours(i,j)
            if board[i][j] == 0 and numOfNeighbours in numReqForBirth:
                nextBoard[i][j] = 1
            elif board[i][j] == 1 and numOfNeighbours not in numReqForLife:
                nextBoard[i][j] = 0

    return nextBoard

def play():
    """play the game"""
    if isPlaying:
        global board
        board = updateBoard()
        drawBoard()
        screen.after(1010 -simSpeed.get(), play)

def start():
    """start the game"""
    global isPlaying
    isPlaying = True
    play()

def stop():
    """stop the game"""
    global isPlaying
    isPlaying= False


def onClick(event):
    """Draw square when mouse clicked on board"""
    size = WIDTH/boardSize.get()
    squareX = math.floor(event.x/size)
    squareY = math.floor(event.y/size)

    if board[squareY][squareX] == 1:
        board[squareY][squareX] = 0
    else:
        board[squareY][squareX] = 1
    drawBoard()

  
def drawBoard():
    """Set each cells colour"""

    for j in range(boardSize.get()):
        for i in range(boardSize.get()):
            color = "#234578" if board[j][i] == 1 else "#9edede"
            tkBoard.itemconfig(cells[j][i], fill=color)

def updateWidthScale(s):
    global isPlaying, cells
    isPlaying = False
    tkBoard.delete("all")
    cells = [[None]*boardSize.get() for i in range(boardSize.get())]
    createCells()
    initialiseEmptyBoard()

    seedsScale.configure(to = int(s)**2)

def updateMinBirth(s):
    global numReqForBirth
    maxBirthScale.configure(from_=s)
    numReqForBirth = [i for i in range(minBirth.get(), maxBirth.get()+1)]
def updateMaxBirth(s):
    global numReqForBirth
    minBirthScale.configure(to=s)
    numReqForBirth = [i for i in range(minBirth.get(), maxBirth.get()+1)]
def updateMinSurvive(s):
    global numReqForLife
    maxSurviveScale.configure(from_=s)
    numReqForLife= [i for i in range(minSurvive.get(), maxSurvive.get()+1)]
def updateMaxSurvive(s):
    global maxSurviveScale
    minSurviveScale.configure(to=s)
    numReqForLife= [i for i in range(minSurvive.get(), maxSurvive.get() +1)]

screen = initialiseWindow()
tkBoard = tk.Canvas(screen, bg = "#e8e8e8", width = 400, height = 400)
tkBoard.grid(row = 0, column=0, rowspan=7, columnspan=3, sticky="N")
tkBoard.bind("<Button-1>", onClick)

###### dimensions #######
sliders = ttk.LabelFrame(screen, text = "", labelanchor="n", width = 18)
sliders.grid(row = 0, column = 3)

tk.Label(sliders, text = "WIDTH").grid(column = 0, row = 0)

boardSize = tk. IntVar()
boardSize.set(20)
widthScale = tk.Scale(sliders, from_= 20, to = 50, variable = boardSize, orient="horizontal",
    resolution = 2, length = 78, width = 8, command=updateWidthScale)
widthScale.grid(column =1, row = 0)



######Sliders###########

tk.Label(sliders, text = "NUM OF SEEDS").grid(column = 0, row = 1)
numOfSeeds = tk. IntVar()
numOfSeeds.set(150)
seedsScale = tk.Scale(sliders, from_= 50, to = boardSize.get()**2, variable = numOfSeeds, orient="horizontal",
                       length = 78, width = 6 )
seedsScale.grid(column =1, row = 1)

tk.Label(sliders, text = "MIN FOR BIRTH").grid(column = 0, row = 2)
minBirth = tk. IntVar()
minBirth.set(3)
minBirthScale = tk.Scale(sliders, from_= 1, to = 3, variable = minBirth, orient="horizontal",
     length = 78, width = 6, command=updateMinBirth)
minBirthScale.grid(column =1, row = 2)

tk.Label(sliders, text = "MAX FOR BIRTH").grid(column = 0, row = 3)
maxBirth = tk. IntVar()
maxBirth.set(3)
maxBirthScale = tk.Scale(sliders, from_= 3, to = 8, variable = maxBirth, orient="horizontal",
     length = 78, width = 6, command=updateMaxBirth)
maxBirthScale.grid(column =1, row = 3)

tk.Label(sliders, text = "MIN FOR SURVIVAL").grid(column = 0, row =4)
minSurvive = tk. IntVar()
minSurvive.set(2)
minSurviveScale = tk.Scale(sliders, from_= 1, to = 2, variable = minSurvive, orient="horizontal",
     length = 78, width = 6, command=updateMinSurvive)
minSurviveScale.grid(column =1, row = 4)


tk.Label(sliders, text = "MAX FOR SURVIVAL").grid(column = 0, row = 5)
maxSurvive = tk. IntVar()
maxSurvive.set(3)
maxSurviveScale = tk.Scale(sliders, from_= 2, to = 8, variable = maxSurvive, orient="horizontal",
     length = 78, width = 6, command=updateMaxSurvive)
maxSurviveScale.grid(column =1, row = 5)

tk.Label(sliders, text = "SPEED").grid(column = 0, row = 6)
simSpeed = tk. IntVar()
simSpeed.set(100)
speedScale = tk.Scale(sliders, from_= 0, to = 1000, variable = simSpeed, orient="horizontal",
                       length = 78, width = 6 )
speedScale.grid(column =1, row = 6)

###### Buttons ##########
startButton = tk.Button(screen, text = "START", width = 25, height =2, command = start)
startButton.grid(column = 3, row = 1)
stopButton = tk.Button(screen, text = "STOP", width = 25, height =2, command = stop)
stopButton.grid(column = 3, row = 2)

randomConfigButton = tk.Button(screen, text = "RANDOMISE", width = 25, height =2, command = initialiseRandomBoard)
randomConfigButton.grid(column = 3, row = 3)
clearButton = tk.Button(screen, text = "CLEAR", width = 25, height =2, command = initialiseEmptyBoard)
clearButton.grid(column = 3, row = 4)



###################

cells = [[None]*boardSize.get() for i in range(boardSize.get())]
createCells()
initialiseEmptyBoard()

screen.mainloop()
