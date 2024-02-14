import tkinter as tk
from turtle import RawTurtle, TurtleScreen
import randomcolor
import pandas

WINDOW_SIZE = '725x530'
BG_PIC = 'blank_states_img.gif'
GUESSED_STATES = []
left_count = 50
DB = pandas.read_csv('50_states.csv')
DB = DB.to_dict()


# Create window.
root = tk.Tk()
root.configure(bg='white')
root.geometry(WINDOW_SIZE)
# Playground for Turtle()
canvas = tk.Canvas(master=root, width=725, height=491, bg='white', highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=5)
play_screen = TurtleScreen(canvas)
play_screen.bgpic(BG_PIC)
# Every turtle as US state.


class States():
    def __init__(self):
        pass

    def create_new_state(self, state_name, x, y):
        self.tinker = RawTurtle(play_screen)
        self.tinker.shape('circle')
        self.tinker.shapesize(0.2, 0.2)
        self.tinker.penup()
        self.tinker.speed('fastest')
        self.tinker.color(randomcolor.RandomColor().generate())
        self.tinker.goto(x, y)
        self.tinker.write(state_name, font=('monospace', 8, 'bold'))
# Placeholder with hint text.


class HintEntry(tk.Entry):
    def __init__(self, master=None, color='grey', placeholder='Write your guess...'):
        super().__init__(master, width=25, background='white',
                         relief='flat', highlightcolor='black', highlightthickness=1, fg='black')
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        self.grid(row=1, column=0,padx=15, pady=9, sticky='w')
        self.bind('<FocusIn>', self.focus_in)
        self.bind('<FocusOut>', self.focus_out)
        self.put_placeholder()
    # Gets user input.
    def user_input(self):
        return self.get()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
    # Clears the entry.
    def focus_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def focus_out(self, *args):
        if not self.get():
            self.put_placeholder()


entry = HintEntry(master=root)
# By onclicking the button this function gets the user input and checks has the user written it before.
# If it's first time it creates an object of State and writes the state name.


def check_the_state():
    global left_count
    user_guess = entry.get()
    user_guess = user_guess.title()
    entry.delete(0, tk.END)
    if user_guess not in GUESSED_STATES:
        GUESSED_STATES.append(user_guess)
        for state in range(50):
            if user_guess == DB['state'][state]:
                x_pos = DB['x'][state]
                y_pos = DB['y'][state]
                States().create_new_state(state_name=user_guess, x=x_pos, y=y_pos)
                left_count -= 1
                score_label.config(text=left_count)

# By onclicking the Exit button this function destroys the root.


def end_the_game():
    root.destroy()


score_label = tk.Label(text=left_count)
score_label.grid(row=1, column=1, sticky='w', ipadx=4, ipady=4)
# Opens all unguessed states.


def check_all():
    global left_count
    for state in range(50):
        if DB['state'][state] not in GUESSED_STATES:
            x_pos = DB['x'][state]
            y_pos = DB['y'][state]
            States().create_new_state(state_name=DB['state'][state], x=x_pos, y=y_pos)
            left_count -= 1
            score_label.config(text=left_count)


check_btn = tk.Button(master=root, command=check_the_state, text='Check',
                      highlightthickness=0, background='green', width=10)
check_btn.grid(row=1, column=2, sticky='w')

show_all = tk.Button(master=root, text='Show All',
                     highlightthickness=0, background='grey', width=10, command=check_all)
show_all.grid(row=1, column=3, sticky='w')

hint_btn = tk.Button(master=root, command=end_the_game, text='Exit',
                     highlightthickness=0, background='red', width=10)
hint_btn.grid(row=1, column=4, sticky='w')

root.mainloop()
