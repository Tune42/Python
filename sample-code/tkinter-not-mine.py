import random
from tkinter import *
 
winCount = 0
loseCount = 0
 
root = Tk()
root.title("ROCKPAPERSCISSORS")
 
 
moves = [ 'ROCK',  'PAPER', 'SCISSORS']
move2 = [ 'SCISSORS', 'ROCK', 'PAPER']
 
 
 
l = Label(root, width=35, borderwidth=5)
l.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
 
## picks computers move upon click
def computer_move():
    global computermove
    i = random.randint(0,2)
    computermove = moves[int(i)]
    return computermove
 
## main function triggers text with time delays
 
def button_click(string):
    global playermove
    global computermove
    playermove = string
    computermove = computer_move()
    winner = who_wins()
    l.config(text = string)
    l.after(500, lambda: l.config(text="VS"))
    l.after(1200, lambda: l.config(text=computermove))
    l.after(1700, lambda: l.config(text=winner))
    l.after(2500, lambda: l.config(text=str(winCount) + ' to ' + str(loseCount)))
 
##determines winner and keeps track of wins and loses
   
def who_wins():
    global winner
    global winCount
    global loseCount
    pw = moves.index(playermove)
    cm = move2.index(computermove)
    pt = move2.index(playermove)
    cw = moves.index(computermove)
    if pw == cm:  
        winner = ' YOU WIN '
        winCount = winCount + 1
    elif pt == cm:
        winner = 'TIE'
    elif pt == cw:
        winner = 'you lose...'
        loseCount = loseCount + 1
    return winner
           
   
 
   
   
 
 
button_rock = Button(root, fg='#916b31', text='ROCK', padx=40, pady=20, command=lambda: button_click("ROCK"))
button_paper = Button(root, text='PAPER', padx=40, pady=20, command=lambda: button_click("PAPER"))
button_scissors = Button(root, fg='#adadad', text='SCISSORS', padx=40, pady=20, command=lambda: button_click("SCISSORS"))
 
button_rock.grid(row=1, column=0,)
button_paper.grid(row=1, column=1,)
button_scissors.grid(row=1, column=2,)
 
root.mainloop()