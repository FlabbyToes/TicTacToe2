"""
Name: Alex Hu
UTEID: ah59643

On my honor, Alex Hu, this programming assignment is my own work
and I have not provided this code to any other student.

Complete the following:

0. What is your email in case I have issues while trying to install, run, and
use your program.

ahuliangbo@gmail.com

1. What is the purpose of your program?

My programs purpose is to be fun. My program was originally going to be a 3d tic tac toe.
After 5 minutes of careful thought, I realized 3d tic tac toe is horrendously unbalanced
because the person who goes first always wins. Then miraculously, when doomscolling
through Instagram reels, I came across a reel of a tic tac toe device that played
an altered version of tic tac toe where each player can only have 3 marks on the board at a time.
So I decided to code that instead. I think this version is also unbalanced since I have only beaten the bot twice
and both were from the bot playing unoptimally because one specific board sequence causes it to do so (bot starts
position 1, player plays 5, bot plays 2, player plays 3, bot goes to position 4, player wins on 7, no other corner
start does this).

2. List the major features of your program:

The game has 2 buttons for 1 player and 2 player, clicking either will start a new game with the number of players.
1 player button will start a game with a bot where the bot goes first. Each player can only
have 3 marks on the board at a time. After 3 turns, the players next move will replace their oldest mark.
The mark being replaced will start blinking. In 2 player mode, only the player who is currently moving has
the blinking mark, but in 1 player mode, the bot's mark also blinks during the player's move, because the bot
moves too fast. The program will diplay in the bottom corners who is currently moving, and who won the game.
The game ends when someone gets 3 in a row. I also made a text version that plays after you close the GUI,
I based the GUI version off the text version.

3. What 3rd party modules must be installed for the program to work?
   (Must be clear and explicit here or we won't be able to test your program.)
   
   If it is required to install 3rd party modules include the EXACT pip command.
   
None.

4. List the things your learned while doing this program. Python features,
   techniques, third party modules, etc.

I learned more about OOP with python, a lot more GUI stuff with tkinter, and game bot algorithms.
tkinter Canvas, import sys, Canvas.after(), minimax alpha beta pruning and monte carlo algorithms,
mouse click event, getting the mouse x and y.
I used minimax algorithm for my bot and I watched this video:https://www.youtube.com/watch?v=trKjYdBASyQ
and adapted their code to mine.


5. What was the most difficult thing you had to overcome or learn
   to get this program to work?

The GUI stuff was tedious

6. What features would you add next?
Make the GUI prettier, player can choose to go first over bot, print instructions button.

"""""
import sys
import random
from tkinter import *
from tkinter import ttk

PADX, PADY, SCALE = 72, 25, 150

class Game:
    def __init__(self):
        self.__players = 0
        self.__board = [[ Mark(' ', 0) for i in range(3)] for j in range(3)]
        self.__turn = 0
        self.__winner = ' '
        self.__label = Label()

    def bot_turn(self, canvas):
        """
        Bot moves, if game is won, do nothing
        """
        if self.__winner != ' ':
            return
        bot_move(self.__board, self.__turn)
        self.__turn += 1
        self.update(canvas)
    def not_playing(self):
        """
        If __players == 0, not playing a game
        """
        return self.__players == 0
        
    def player_turn(self, mark, canvas, position):
        """
        Player moves, if move is invalid or game is won, do nothing
        """
        if self.__winner != ' ':
            return False
        position -= 1
        if self.__board[int(position/3)][int(position%3)].get_char() == ' ':
            self.__board[int(position/3)][int(position%3)].make_move(mark)
            age_board(self.__board, mark)
            self.__turn += 1
            self.update(canvas)
            return True
            
    def flash(self, mark, canvas, position, blink):
        """
        Blinks mark that is going to be removed
        """
        if self.__winner != ' ':
            return
        pos = position -1
        if (blink == False and self.__board[int(pos/3)][int(pos%3)].get_mark() != 'X'
            and self.__board[int(pos/3)][int(pos%3)].get_mark() != 'X'):
            delete_mark(canvas, position)
        else:
            if mark == 'X':
                draw_x(canvas, position)
            elif mark == 'O':
                draw_o(canvas, position)
        if self.__board[int(pos/3)][int(pos%3)].get_mark() == '@':
            canvas.after(500, lambda: self.flash(mark, canvas, position, not blink))
        elif self.__board[int(pos/3)][int(pos%3)].get_mark() == '#':
            canvas.after(500, lambda: self.flash(mark, canvas, position, not blink))
        #"Update" mark to prevent it from printing again after it is removed
        elif self.__board[int(pos/3)][int(pos%3)].get_mark() == 'X':
            delete_mark(canvas, position)
            draw_x(canvas, position)
        elif self.__board[int(pos/3)][int(pos%3)].get_mark() == 'O':
            delete_mark(canvas, position)
            draw_o(canvas, position)
        elif self.__board[int(pos/3)][int(pos%3)].get_mark() == ' ':
            delete_mark(canvas, position)
            
    def next_move(self, position, canvas):
        """
        Processes next move
        """
        if self.__turn%2 == 0:
            if self.__players == 2:
                self.player_turn('X', canvas, position)
        else:
            moved = self.player_turn('O', canvas, position)
            if self.__players == 1 and moved:
                self.bot_turn(canvas)
        
    def new_game(self, num_players, canvas):
        """
        Resets board for new game
        """
        self.__board = [[ Mark(' ', 0) for i in range(3)] for j in range(3)]
        self.__players = num_players
        self.__turn = 0
        self.__winner = ' '
        self.__label.destroy()
        self.update(canvas)
        
    def update(self, canvas):
        """
        Redraws current board
        """
        #print_board(self.__board)
        for i in range(3):
            for j in range(3):
                position = i*3 + j + 1
                delete_mark(canvas, position)
                if self.__board[i][j].get_mark() == 'X':
                    draw_x(canvas, position)
                elif self.__board[i][j].get_mark() == 'O':
                    draw_o(canvas, position)
                elif self.__board[i][j].get_mark() == '#':
                    if self.__turn%2 == 0 or self.__players ==1:
                        self.flash('X', canvas, position, True)
                    else:
                        draw_x(canvas, position)
                elif self.__board[i][j].get_mark() == '@':
                    if self.__turn%2 == 1:
                        self.flash('O', canvas, position, True)
                    else:
                        draw_o(canvas, position)
                        
        self.__winner = game_over(self.__board)
        self.__label.destroy()
        if self.__winner == 'X':
            if self.__players == 1:
                self.__label = Label(canvas, font='Courier 16', text='Bot wins',
                          borderwidth=0, relief='solid', bg = "white")
            else:
                self.__label = Label(canvas, font='Courier 16', text='X wins',
                          borderwidth=0, relief='solid', bg = "white")
            canvas.create_window(25, 500, window=self.__label, anchor="nw")
        elif self.__winner == 'O':
            self.__label = Label(canvas, font='Courier 16', text='O wins',
                          borderwidth=0, relief='solid', bg = "white")
            canvas.create_window(500, 500, window=self.__label, anchor="nw")
        elif self.__turn%2 == 0:
            if self.__players == 1:
                #wont print anyway
                self.__label = Label(canvas, font='Courier 12', text=' ',
                          borderwidth=0, relief='solid', bg = "white")
            elif self.__players == 2:
                self.__label = Label(canvas, font='Courier 12', text='X move',
                          borderwidth=0, relief='solid', bg = "white")
            canvas.create_window(25, 500, window=self.__label, anchor="nw")
        elif self.__turn %2 == 1:
            if self.__players == 1:
                self.__label = Label(canvas, font='Courier 12', text='Player: O',
                          borderwidth=0, relief='solid', bg = "white")
                canvas.create_window(455, 500, window=self.__label, anchor="nw")
            elif self.__players == 2:
                self.__label = Label(canvas, font='Courier 12', text='O move',
                          borderwidth=0, relief='solid', bg = "white")
                canvas.create_window(500, 500, window=self.__label, anchor="nw")
class Mark:
    def __init__(self, char, age):
        self.__char = char
        self.__death = ' '
        self.__age = age
        
    def make_move(self, char):
        self.__char = char
        if self.__char == 'X':
            self.__death = '#'
        elif self.__char == 'O':
            self.__death = '@'
        elif self.__char == ' ':
            self.__death = ' '
        self.__age = 0
            
    def grow(self, mark):
        if self.__char == mark:
            self.__age += 1
        if self.__age > 3:
            self.__char = ' '
            self.__age = 0
    def shrink(self, mark):
        if self.__char == mark:
            self.__age -= 1
        if self.__age <= 0:
            self.__char = ' '
            self.__age = 0
    
    def get_mark(self):
        if self.__age == 3:
            return self.__death
        return self.__char
    
    def get_char(self):
        return self.__char
    def set_oldest(self):
        self.__age = 3
 

def make_grid(canvas):
    """
    Draws grid lines
    """
    l1 = canvas.create_line(SCALE + PADX, 0 + PADY,
                            SCALE + PADX, SCALE*3 + PADY, fill='black', width=5)
    l2 = canvas.create_line(SCALE*2 + PADX, 0 + PADY,
                            SCALE*2 + PADX, SCALE*3 + PADY, fill='black', width=5)
    l3 = canvas.create_line(0 + PADX, SCALE + PADY,
                            SCALE*3 + PADX,SCALE + PADY, fill='black', width=5)
    l4 = canvas.create_line(0 + PADX,SCALE*2 + PADY,
                            SCALE*3 + PADX,SCALE*2 + PADY, fill='black', width=5)
    
def draw_x(canvas, position):
    """
    Draws X mark
    """
    if position == 0:
        return
    position -= 1
    y = int(position / 3)
    x = position % 3
    l1 = canvas.create_line(x * SCALE + PADX + int(SCALE/10), y * SCALE + PADY + int(SCALE/10),
                            (x+1) * SCALE + PADX - int(SCALE/10), (y+1) * SCALE + PADY - int(SCALE/10),
                            fill='black', width=5)
    l2 = canvas.create_line( (x+1) * SCALE + PADX - int(SCALE/10), y * SCALE + PADY + int(SCALE/10),
                             x * SCALE + PADX+ int(SCALE/10), (y+1) * SCALE + PADY - int(SCALE/10),
                             fill='black', width=5)

def draw_o(canvas, position):
    """
    Draws O mark
    """
    if position == 0:
        return
    position -= 1
    y = int(position / 3)
    x = position % 3
    o = canvas.create_oval(x * SCALE + PADX + int(SCALE/10), y * SCALE + PADY + int(SCALE/10),
                            (x+1) * SCALE + PADX - int(SCALE/10), (y+1) * SCALE + PADY - int(SCALE/10),
                            fill='white', width=5)
def delete_mark(canvas, position):
    """
    Deletes mark by drawing white box
    """
    if position == 0:
        return
    position -= 1
    y = int(position / 3)
    x = position % 3
    d = canvas.create_rectangle(x * SCALE + PADX + int(SCALE/10), y * SCALE + PADY + int(SCALE/10),
                            (x+1) * SCALE + PADX - int(SCALE/10), (y+1) * SCALE + PADY - int(SCALE/10),
                            fill='white', outline='white', width=5)
def create_buttons(canvas):
    """
    Creates 1 player and 2 player buttons to start new game
    Return: buttons
    """
    buttons = []
    for row in range(0, 3):
        button_row = []
        for col in range(0, 3):
            button = Button(canvas, font='Courier 1', text=' ',
                          borderwidth=0, relief='solid', width = int(SCALE//1.125),
                            height = int(SCALE//3.15), background = "white")
            canvas.create_window(row * SCALE + PADX+ int(SCALE/30), col* SCALE + PADY+ int(SCALE/30),
                                 window=button, anchor="nw")
            button_row.append(button)
        buttons.append(button_row)
    return buttons

def getorigin(event, canvas, game):
      global x,y
      x = event.x
      y = event.y
      
      if(game.not_playing()):
          return
      if (PADX > x or x > PADX + 3 * SCALE or PADY > y or y > PADY+3*SCALE):
          return
      xx = int((x - PADX) / SCALE)
      yy = int((y - PADY) / SCALE)
      position = 1 + yy * 3 + xx
      game.next_move(position, canvas)
      
def new_game(canvas, game, num_players):
    game.new_game(num_players, canvas)
    if num_players == 1:
        game.bot_turn(canvas)
    
def make_buttons(canvas, game):
    two_player = Button(canvas, font='Courier 12', text='2 Player',
                          borderwidth=1, relief='solid', width = 12,
                            height = 1, background = "white",
                        command=lambda: new_game(canvas, game, 2))
    canvas.create_window(310, PADY + SCALE*3 + 25, window=two_player, anchor="nw")
    one_player = Button(canvas, font='Courier 12', text='1 Player',
                          borderwidth=1, relief='solid', width = 12,
                            height = 1, background = "white",
                        command=lambda: new_game(canvas, game, 1))
    canvas.create_window(155, PADY + SCALE*3 + 25, window=one_player, anchor="nw")
def main():
    root = Tk()
    
    root.title("Tic-Tac-Toe")
    root.resizable(False, False)
    
    canvas = Canvas(root, bg="white", height=550, width=600)
    canvas.grid(row=0,column=0)
    make_grid(canvas)
    game = Game()
    make_buttons(canvas, game)
    
    root.bind("<Button 1>",lambda event:getorigin(event, canvas, game))
    root.mainloop()
    welcome_and_instructions()
    
    while True:
        num_players = input('\nEnter number of players:')
        while num_players!='1' and num_players!='2':
            num_players = input('\n1 or 2:')
        num_players= int(num_players)
        
        winner = play(num_players)
        
        
        print(winner + ' wins!')
        play_again = input(
            '\nDo you want to play again? Type Y for yes: ')
        if play_again.lower() == 'y':
            continue
        else:
            break
    pass
def play(num_players):
    winner = 0
    board = [[ Mark(' ', 0) for i in range(3)] for j in range(3)]
    turn = 0
    while True:
        print_board(board)
        if turn%2 == 0:
            if num_players==1:
                bot_move(board, turn)
            else:
                player_move('X', board)
        else:
            player_move('O', board)
            
        winner = game_over(board)
        if winner == 'X' or winner == 'O':
            print_board(board)
            return winner
        turn += 1
        
def age_board(board, mark):
    for i in range(3):
        for j in range(3):
            board[i][j].grow(mark)

def deage_board(board, mark):
    for i in range(3):
        for j in range(3):
            board[i][j].shrink(mark)
def undo_move(board, mark, i, j):
    
    deage_board(board, mark)
    if i==-1 or j== -1:
        return
    board[i][j].make_move(mark)
    board[i][j].set_oldest()
            
scores = {
  "X": 1,
  "O": -1,
  "T": 0
}
def get_oldest(board, mark):
    for i in range(3):
        for j in range(3):
            if mark =='X':
                if board[i][j].get_mark() == '#':
                    return i,j
            elif mark =='O':
                if board[i][j].get_mark() == '@':
                    return i,j
    return -1, -1
                
def bot_move(board, turn):
    if(turn == 0):
        x = random.randint(0,2)
        y = random.randint(0,2)
        board[x][y].make_move('X')
        age_board(board, 'X')
        print('Bot X move: ',(x * 3 + y + 1))
        return int(x * 3 + y + 1)
#     if(turn == 2):
#         board[0][0].make_move('X')
#         age_board(board, 'X')
#         return
    bestScore = -sys.maxsize - 1
    for i in range(3):
        for j in range(3):
            if board[i][j].get_char() == ' ':
                x,y = get_oldest(board, 'X')
                board[i][j].make_move('X')
                age_board(board, 'X')
                score = minimax(board, 0, False)
                undo_move(board, 'X', x, y)
                if bestScore < score:
                    bestScore = score
                    bestMove = [i,j]
    print('Bot X move: ',(bestMove[0] * 3 + bestMove[1] + 1))
    board[bestMove[0]][bestMove[1]].make_move('X')
    age_board(board, 'X')
    return int(bestMove[0] * 3 + bestMove[1] + 1)
    
def minimax(board, depth, isMaxxing):
    winner = game_over(board)
    if winner == 'X' or winner == 'O':
        return scores[winner]
    if depth >= 7:
        return scores["T"]
    if isMaxxing:
        bestScore = -sys.maxsize - 1
        for i in range(3):
            for j in range(3):
                if board[i][j].get_char() == ' ':
                    x,y = get_oldest(board, 'X')
                    board[i][j].make_move('X')
                    age_board(board, 'X')
                    score = minimax(board, depth + 1, False)
                    undo_move(board, 'X', x, y)
#                     boardCopy = copy.deepcopy(board)
#                     boardCopy[i][j].make_move('X')
#                     age_board(boardCopy, 'X')
#                     print_board(boardCopy)
#                     score = minimax(boardCopy, depth + 1, False)
                    bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = sys.maxsize
        for i in range(3):
            for j in range(3):
                if board[i][j].get_char() == ' ':
                    x,y = get_oldest(board, 'O')
                    board[i][j].make_move('O')
                    age_board(board, 'O')
                    score = minimax(board, depth + 1, True)
                    undo_move(board, 'O', x, y)
#                     boardCopy = copy.deepcopy(board)
#                     boardCopy[i][j].make_move('X')
#                     age_board(boardCopy, 'X')
#                     print_board(boardCopy)
#                     score = minimax(boardCopy, depth + 1, True)
                    bestScore = min(score, bestScore)
        return bestScore
    
def player_move(mark, board):
    player_move = 0
    while True:
        try:
            player_move = int(input('\nPlayer ' + mark + ' move, 1-9:'))
            if 1 <= player_move <=9:
                pass
            else:
                print('Please enter number 1-9')
                continue
        except:
            print('Please enter number 1-9')
            continue
        player_move -=1
        if board[int(player_move/3)][int(player_move%3)].get_mark() == ' ':
            board[int(player_move/3)][int(player_move%3)].make_move(mark)
            age_board(board, mark)
            return
        else:
            print('That spot is already filled')

def print_board(board):
    print('\n ' + board[0][0].get_mark() + ' | ' + board[0][1].get_mark() + ' | ' + board[0][2].get_mark())
    print('-----------')
    print(' ' + board[1][0].get_mark() + ' | ' + board[1][1].get_mark() + ' | ' + board[1][2].get_mark())
    print('-----------')
    print(' ' + board[2][0].get_mark() + ' | ' + board[2][1].get_mark() + ' | ' + board[2][2].get_mark())
    
    
            
def game_over(board):
    for i in range(3):
        if board[i][0].get_char()==board[i][1].get_char()==board[i][2].get_char()!= ' ':
            return board[i][2].get_char()
    for i in range(3):
        if board[0][i].get_char()==board[1][i].get_char()==board[2][i].get_char()!= ' ':
            return board[2][i].get_char()
    if board[0][0].get_char()==board[1][1].get_char()==board[2][2].get_char()!= ' ':
            return board[0][0].get_char()
    if board[0][2].get_char()==board[1][1].get_char()==board[2][0].get_char()!= ' ':
            return board[2][0].get_char()
    return ' '

def welcome_and_instructions():
    print('Welcome to Tic Tac Toe 2.')
    instructions = input('\nEnter y for instructions, anything else to skip: ')
    if instructions == 'y':
        print('\nYou have to try to make 3 marks in a row before your opponent')
        print('You can only have 3 marks on the board at a time.')
        print('After 3 turns your oldest mark will be replaced by your next move.')
        print('The oldest move for each player is marked # for X and @ for O.')
        print('Each turn you will enter a position 1-9 to place your next mark')
        print('\n 1 | 2 | 3')
        print('-----------')
        print(' 4 | 5 | 6')
        print('-----------')
        print(' 7 | 8 | 9')
    
    
if __name__ == '__main__':
    main()
