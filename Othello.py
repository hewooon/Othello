from bangtal import *
from enum import Enum

setGameOption(GameOption.INVENTORY_BUTTON,False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON,False)
setGameOption(GameOption.ROOM_TITLE, False)

scene = Scene("Othello","Images/background.png")

def setScore(num):
    temp = 0
    if num==0:
        temp = Object("Images/0.png")
    elif num == 1:
        temp = Object("Images/1.png")
    elif num == 2:
        temp = Object("Images/2.png")
    elif num == 3:
        temp = Object("Images/3.png")
    elif num == 4:
        temp = Object("Images/4.png")
    elif num == 5:
        temp = Object("Images/5.png")
    elif num == 6:
        temp = Object("Images/6.png")
    elif num == 7:
        temp = Object("Images/7.png")
    elif num == 8:
        temp = Object("Images/8.png")
    elif num == 9:
        temp = Object("Images/9.png")
    temp.setScale(2.8)
    return temp


black_score = 2
white_score = 2
black = []
white = []

black.append(setScore(0))
black.append(setScore(2))
white.append(setScore(0))
white.append(setScore(2))

if int(black_score/10) == 0:
    black[0].setImage("Images/blank.png")
if int(white_score/10) == 0:
    white.pop(0)
    white.append(setScore(0))
    white[1].setImage("Images/blank.png")

black[0].locate(scene, 770, 250)  
black[0].show()
black[1].locate(scene, 830, 250)  
black[1].show()

white[0].locate(scene, 1090, 250) 
white[0].show()
white[1].locate(scene, 1150, 250) 
white[1].show()

def updateScore():
    for i in range(2):
        black[i].hide()
        white[i].hide()
    black.clear()
    white.clear()

    black.append(setScore(int(black_score/10)))
    black.append(setScore(int(black_score%10)))
    white.append(setScore(int(white_score/10)))
    white.append(setScore(int(white_score%10)))

    if int(black_score/10) == 0:
        black[0].setImage("Images/blank.png")
    if int(white_score/10) == 0:
        white.pop(0)
        white.append(setScore(0))
        white[1].setImage("Images/blank.png")

    
    black[0].locate(scene, 770, 250)  
    black[0].show()
    black[1].locate(scene, 830, 250)  
    black[1].show()

    white[0].locate(scene, 1090, 250) 
    white[0].show()
    white[1].locate(scene, 1150, 250) 
    white[1].show()




class State(Enum):
    BLANK = 0
    POSSIBLE = 1
    BLACK = 2
    WHITE = 3

class Turn(Enum):
    BLACK = 1
    WHITE = 2
turn = Turn.BLACK

def setState(x,y,s):
    object = board[y][x]
    object.state = s
    if s == State.BLANK:
        object.setImage("Images/blank.png")
    elif s == State.BLACK:
        object.setImage("Images/black.png")
    elif s == State.WHITE:
        object.setImage("Images/white.png")
    elif turn == Turn.BLACK:
        object.setImage("Images/black possible.png")
    else:
        object.setImage("Images/white possible.png")

def stone_onMouseAction(x,y):
    global turn
    object = board[y][x]
    if object.state == State.POSSIBLE:
        if turn == Turn.BLACK:
            setState(x,y,State.BLACK)
            reverse_xy(x,y,0)
            turn = Turn.WHITE
            if not setPossible():
                turn = Turn.BLACK
                if not setPossible():
                    showMessage("게임이 종료되었습니다.")
            
            whiteAI()
            turn = Turn.BLACK
            updateScore()
            if not setPossible():
                turn = Turn.WHITE
                whiteAI()
                turn = Turn.BLACK
                if not setPossible():
                    showMessage("게임이 종료되었습니다.")
#
white_count=0
count_temp=0
best_x=0
best_y=0

def whiteAI():
    global white_count, count_temp, best_x, best_y
    white_count = 0
    check = 0
    for x in range(8):
        for y in range(8):
            if board[y][x].state == State.POSSIBLE :
                reverse_xy(x,y,check)
    check = 1
    setState(best_x,best_y,State.WHITE)
    reverse_xy(best_x,best_y,1)

def setPossible_xy_dir(x,y,dx,dy):
    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    else:
        mine = State.WHITE
        other = State.BLACK
    possible = False
    while True:
        x = x + dx
        y = y + dy
        if x < 0 or x > 7 : return False
        if y < 0 or y > 7 : return False
        object = board[y][x]
        if object.state == other:
            possible = True
        elif object.state == mine:
            return possible
        else: return False

def setPossible_xy(x,y):
    object = board[y][x]
    if object.state == State.BLACK: return False
    if object.state == State.WHITE: return False
    setState(x,y,State.BLANK)
    if(setPossible_xy_dir(x,y,0,1)): return True
    if(setPossible_xy_dir(x,y,1,1)): return True
    if(setPossible_xy_dir(x,y,1,0)): return True
    if(setPossible_xy_dir(x,y,1,-1)): return True
    if(setPossible_xy_dir(x,y,0,-1)): return True
    if(setPossible_xy_dir(x,y,-1,-1)): return True
    if(setPossible_xy_dir(x,y,-1,0)): return True
    if(setPossible_xy_dir(x,y,-1,1)): return True
    return False

def reverse_xy_dir(x,y,dx,dy,check):
    global white_count, count_temp, black_score, white_score
    if turn == Turn.BLACK:
        check=-1
        mine = State.BLACK
        other = State.WHITE
        
    else:
        if check == 0:
            mine = State.WHITE
        else:
            mine = State.WHITE
        other = State.BLACK
    possible = False
    while True:
        x = x + dx
        y = y + dy
        if x < 0 or x > 7 : return
        if y < 0 or y > 7 : return
        object = board[y][x]
        if object.state == other:
            possible = True
        elif object.state == mine:
            if possible:
                while True:
                    x = x - dx
                    y = y - dy

                    object = board[y][x]
                    
                    if object.state == other:
                        if turn == Turn.BLACK:
                            setState(x,y,mine)
                            black_score += 1
                            white_score -= 1
                        elif check==0:
                            count_temp+=1
                        elif check==1:
                            setState(x,y,State.WHITE)
                            white_score += 1
                            black_score -= 1
                    else:
                        return

        else: return

def reverse_xy(x,y,check):
    global white_count, count_temp, best_x, best_y, black_score, white_score
    count_temp=0
    if turn == Turn.BLACK:
        black_score += 1
    elif check==1:
        white_score += 1
    reverse_xy_dir(x,y,0,1,check)
    reverse_xy_dir(x,y,1,1,check)
    reverse_xy_dir(x,y,1,0,check)
    reverse_xy_dir(x,y,1,-1,check)
    reverse_xy_dir(x,y,0,-1,check)
    reverse_xy_dir(x,y,-1,-1,check)
    reverse_xy_dir(x,y,-1,0,check)
    reverse_xy_dir(x,y,-1,1,check)
    
    if count_temp >= white_count and turn==Turn.WHITE:

        white_count = count_temp
        best_x = x
        best_y = y

def setPossible():
    possible = False
    for y in range(8):
        for x in range(8):
            if setPossible_xy(x,y):
                setState(x,y,State.POSSIBLE)
                possible = True
    return possible

board = []
for y in range(8):
    board.append([])
    for x in range(8):
        object = Object("Images/blank.png")
        object.locate(scene,40+x*80,40+y*80)
        object.show()
        object.onMouseAction = lambda mx, my, action, ix = x, iy = y:stone_onMouseAction(ix,iy)
        object.state = State.BLANK
        board[y].append(object)

setState(3,3,State.BLACK)
setState(4,4,State.BLACK)
setState(3,4,State.WHITE)
setState(4,3,State.WHITE)

setPossible()

startGame(scene)