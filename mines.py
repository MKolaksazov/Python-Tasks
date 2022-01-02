from tkinter import *

# wklyuchvane na tenzornite biblioteki za po-lesno inicializirane na masiwa
import numpy as np
import random


mines = 10

buttons = np.zeros([10,10], dtype=int)

mine_sweep = np.zeros([10,10], dtype=int)

lost = False

def mine_randomization():
    #global mines
    # polzvame dva masiva zashtoto ediniq shgte sydyrja butonite, a drugiq - info za minite
    mine_sweep = np.zeros([10,10], dtype=int)
    
    # randomizirane na minite
    for mine in range(mines):
      x = np.random.randint(0,10)
      y = np.random.randint(0,10)
      if mine_sweep[x][y] == 0:
        mine_sweep[x][y] = 1

    return mine_sweep

mine_sweep = mine_randomization().tolist()

def new_game():
    global lost
    
    lost = False

    

    global mines

    mines = int(entry.get())

    label['text'] = str(mines) + ' mines left'

    global mine_sweep

    mine_sweep = mine_randomization().tolist()
    
    for row in range(10):
        for col in range(10):
            buttons[row][col]['text'] = ''
            buttons[row][col].config(bg='#f0f0f0')
            
# otvarqne na praznite poleta do markirano pole
def open_fields(row, col):

    #global mine_sweep
    
    buttons[row][col]['text'] = str(sum_mines(row, col))
    buttons[row][col].config(bg='green', font=('consolas', 10))
    
    if buttons[row][col]['text'] == '0':

        for i in range(-1,2,1):
            if row + i < 0 or row + i > 9:
                break
            for j in range(-1,2,1):
                if col + j < 0 or col + j > 9: 
                    break
                elif buttons[row + i][col + j]['text'] == '' and mine_sweep[row][col] == 0:        
                    open_fields(row + i, col + j)

# kolko mini ima okolo otworenoto pole
def sum_mines(row, col):

    #global mine_sweep
    
    sum_mines = 0
    
    for i in range(-1,2,1):
        for j in range(-1,2,1):
            if row + i >= 0 and row + i <= 9 and col + j >= 0 and col + j <= 9:
                sum_mines += mine_sweep[row + i][col + j]
        
    return sum_mines

# kakwo da stawa kato otvorim prazno pole i nastypim mina
def cell(row, col):

    #global mine_sweep
    global lost
    
    if buttons[row][col]['text'] == '' and mine_sweep[row][col] == 0 and not lost:
        # rekursivna funkcia
        open_fields(row, col) 
    elif buttons[row][col]['text'] == '' and mine_sweep[row][col] == 1 and not lost:
        buttons[row][col].config(bg='red', font=('consolas', 10))
        buttons[row][col]['text'] = '*'
        label['text'] = 'You lost!'
        lost = True

    if check_win():
        label['text'] = 'You win!'

def check_win():
    global mines

    sum_c = 0
    for i in range(10):
        for j in range(10):
            if buttons[i][j]['text'] != '' and mine_sweep[i][j] == 0:
                sum_c += 1

    return 100 - sum_c == mines


# syzdavane elementite na prozoreca
window = Tk()
window.title('minesweeper')

label = Label(text=str(mines)+' mines left', font=('consolas', 20))
label.pack(side='top')

reset_button = Button(text='restart', command=new_game)
reset_button.pack(side='top')

entry = Entry(window) 
entry.pack(side='top')

buttons = buttons.tolist()

# syzdavane na ramka s masiv, vkliuchvasht butonite
frame = Frame(window)
frame.pack()

for row in range(10):
    for col in range(10):
        buttons[row][col] = Button(frame, text='', font=('consolas', 10),
                                   width=2, height=1,
                                   command= lambda row=row, col=col: cell(row, col))
        buttons[row][col].grid(row=row, column=col)

window.mainloop()
