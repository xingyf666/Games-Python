from tkinter import *
from tkinter.messagebox import *
import random

WIDTH = 600
HEIGHT = 600
#图像块的边长
IMAGE_WIDTH = WIDTH // 3
IMAGE_HEIGHT = HEIGHT // 3
#游戏内行列数
ROWS = 3
COLS = 3
#移动步数
steps = 0
#保存所有图像块的列表
board = [[0, 1, 2], \
         [3, 4, 5], \
         [6, 7, 8]]

root = Tk('拼图2020')
root.title('拼图--2020-8-16')
#载入外部事先生成的9个小图像块
Pics = []
for i in range(9):
    filename = 'split//crop_' + str(i) + '.png'
    Pics.append(PhotoImage(file=filename))

class Square:
    def __init__(self, orderID):
        self.orderID = orderID

    def draw(self, canvas, board_pos):
        img = Pics[self.orderID]
        canvas.create_image(board_pos, image=img)

def init_board():
    #打乱图像块
    L = list(range(9))
    random.shuffle(L)
    #填充拼图板
    for i in range(ROWS):
        for j in range(COLS):
            idx = i * ROWS + j
            orderID = L[idx]
            if orderID is 8:
                board[i][j] = None   #8号块不显示
            else:
                board[i][j] = Square(orderID)

def drawBoard(canvas):
    #绘制黑框
    canvas.create_polygon((0, 0, WIDTH, 0, WIDTH, HEIGHT, 0, HEIGHT), width=1, outline='Black')
    #绘制所有图像块
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] is not None:
                board[i][j].draw(canvas, (IMAGE_WIDTH*(j+0.5), IMAGE_HEIGHT*(i+0.5)))

def mouseclick(pos):
    global steps
    #将单击位置换算成拼图板上的棋盘坐标
    r = int(pos.y // IMAGE_HEIGHT)
    c = int(pos.x // IMAGE_WIDTH)
    if r < 3 and c < 3:
        if board[r][c] is None:
            return
        else:
            current_square = board[r][c]
            if r - 1 >= 0 and board[r-1][c] is None:
                board[r][c] = None
                board[r-1][c] = current_square
                steps += 1
            elif c + 1 <= 2 and board[r][c+1] is None:
                board[r][c] = None
                board[r][c+1] = current_square
                steps += 1
            elif r + 1 <= 2 and board[r+1][c] is None:
                board[r][c] = None
                board[r+1][c] = current_square
                steps += 1
            elif c - 1 >= 0 and board[r][c-1] is None:
                board[r][c] = None
                board[r][c-1] = current_square
                steps += 1
            #print(board)
            label1['text'] = '步数：' + str(steps)
            cv.delete('all')  #清除画布上的内容
            drawBoard(cv)

    if win():
        showinfo(title='恭喜！', message='你成功了！')

def win():
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] is not None and board[i][j].orderID != i*ROWS+j:
                return False
    return True

def play_game():
    global steps
    steps = 0
    init_board()

def callBack2():
    print('重新开始')
    play_game()
    cv.delete('all')
    drawBoard(cv)

cv = Canvas(root, bg='green', width=WIDTH, height=HEIGHT)
b1 = Button(root, text='重新开始', command=callBack2, width=20)
label1 = Label(root, text='步数：'+str(steps), fg='red', width=20)
label1.pack()

cv.bind('<Button-1>', mouseclick)
cv.find
cv.pack()
b1.pack()
play_game()
drawBoard(cv)
root.mainloop()
