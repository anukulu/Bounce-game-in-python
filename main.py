from tkinter import *
import time
import random

#creating the window
tk = Tk()
tk.title('Bounce Game')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

#creating the ball class
class Ball:
    def __init__(self, canvas, paddle, color):
        self.paddle = paddle
        self.canvas = canvas
        self.color = color
        self.id = self.canvas.create_oval(10, 10, 25, 25, fill=self.color)
        self.canvas.move(self.id, 245, 100)
        self.starts = [-3,-2, -1, 1, 2, 3]
        random.shuffle(self.starts)
        self.x_velocity = self.starts[0]
        self.y_velocity = -1
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.score = 0
        self.text_file = open('highscore.txt')
        self.highscore = self.text_file.read()
        self.realhighscore = self.highscore.split()
        self.text = self.canvas.create_text(0,0, text = ('Score : ' + str(self.score)), fill='Black', font =('Times', 15), anchor =NW)
        self.text2 = self.canvas.create_text(370, 0, text=('HighScore : ' + str(self.highscore)), fill='Black', font=('Times', 15), anchor = NW)
        self.text_file.close()
    def draw(self, colr):
        self.colr = colr
        self.color = random.choice(self.colr)
        self.canvas.itemconfig(self.id, fill=self.color, outline='Black')
        self.canvas.move(self.id, self.x_velocity, self.y_velocity)
        pos = self.canvas.coords(self.id)
        if pos[1] < 0:
            self.y_velocity = 3
        if pos[3] > self.canvas_height:
            self.y_velocity = -3
        if pos[0] < 0:
            self.x_velocity = 3
        if pos[2] > self.canvas_width:
            self.x_velocity = -3
        if self.hit_paddle(pos) == True:
            self.y_velocity = -self.y_velocity - abs(self.paddle.x_velocity)

    def hit_paddle(self,pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:
                self.x_velocity = self.x_velocity + self.paddle.x_velocity
                self.score = self.score+1
                self.canvas.itemconfig(self.text, text=('Score : ' + str(self.score)), font =('Times', 15), anchor =NW)
                if self.score > int(self.realhighscore[0]):
                    self.text_file = open('highscore.txt', 'w')
                    self.text_file.write(str(self.score))
                    self.text_file.close()
                return True
        return False
    def hit_bottom(self):
        pos = self.canvas.coords(self.id)
        if pos[3] >= self.canvas_height:
            return True
        return False
class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.color = color
        self.id = self.canvas.create_rectangle(0, 0, 100, 10, fill = self.color)
        self.canvas.move(self.id, 200, 300)
        self.x_velocity = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress - Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress - Right>', self.turn_right)
    def turn_left(self, event):
        self.x_velocity = 3.2
    def turn_right(self, event):
        self.x_velocity = -3.2
    def draw(self):
        self.canvas.move(self.id, self.x_velocity, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x_velocity = 0
        if pos[2] >= self.canvas_width:
            self.x_velocity = 0

#colors for the objects
colors = ['Red', 'Green', 'Yellow', 'Black', 'Pink', 'Blue']

#making the bat and initializing values for it
bat = Paddle(canvas, colors[1])

#making the ball object and initializing the values for it
ball = Ball(canvas, bat, colors[0])

#delaying the game unitl the mouse button is pressed
def game_start(event):
    while 1:
        if ball.hit_bottom() == False:
            ball.draw(colors)
            bat.draw()
        else:
            canvas.create_text(250,250, text = '!!! GAME OVER !!!', fill='Black', font =('Times', 20))
        tk.update()
        time.sleep(0.01)
while 1:
    tk.update()
    time.sleep(0.01)
    canvas.bind_all('<Button - 1>', game_start)

#tk.mainloop()
