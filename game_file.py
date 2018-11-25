from tkinter import Tk, Canvas, Label, Button, Entry, colorchooser, font

class Game():
    def __init__(self):
        self.tk = Tk()
        self.tk.title('Connect 4')
        self.tk.resizable(False, False)
        self.tk.wm_attributes('-topmost', 1)

        self.update()

        self.canvas = Canvas(self.tk, width=600, height=600)
        self.canvas.pack()

        self.update()

        self.screenwidth = self.tk.winfo_screenwidth()
        self.screenheight = self.tk.winfo_screenheight()
        self.x_calc = int(self.screenwidth / 2 - 300)
        self.y_calc = int(self.screenheight / 2 - 300)

        self.tk.geometry('+{}+{}'.format(self.x_calc, self.y_calc))
        self.update()

        self.column = Entry(self.tk, font=('Courier', -15), width=20)
        self.column.place(x=5, y=5)

        self.column.insert(0, 'Enter your move here')

        self.sprites = []
        self.running = True

        self.tk.bind_all('<Return>', self.clear)

        self.update()

    def update(self):
        self.tk.update()
        self.tk.update_idletasks()

    def say(self, *args):
        self.otk = Tk()
        self.otk.title('Message')
        self.otk.resizable(False, False)
        self.otk.wm_attributes('-topmost', 1)

        time = -1
        messages = []
        
        for message in args:
            time += 1
            messages.append(Label(self.otk, text=message, \
                                  font=('Courier', 12)))

        done = Button(self.otk, text='OK', command=self.otk.quit)

        for label in messages:
            label.pack()

        done.pack()

        self.update()

        ww = self.otk.winfo_width()
        wh = self.otk.winfo_height()
        sw = self.otk.winfo_screenwidth()
        sh = self.otk.winfo_screenheight()
        
        x = int(sw / 2 - ww / 2)
        y = int(sh / 2 - wh / 2)

        self.otk.geometry('+{}+{}'.format(x, y))

        self.otk.mainloop()
        self.otk.destroy()

    def clear(self, event):
        self.pl_mv = self.column.get()
        print(self.pl_mv)
        self.column.delete(0, 'end')
        
    def mainloop(self):
        self.timers = []
        
        def forloop():
            for sprite in self.sprites:
                if self.running:
                    sprite.todo()
                    self.update()

                else:
                    for tmr in self.timers:
                        self.tk.after_cancel(tmr)

            self.timers.append(self.tk.after(10, forloop))

        self.timers.append(self.tk.after(10, forloop))

        self.tk.mainloop()
        self.tk.destroy()

class Sprite():
    def __init__(self, game):
        self.game = game
        self.to_do_list = []
        self.x = 0
        self.y = 0

        self.game.sprites.append(self)

    def todo(self):
        self.game.canvas.move(self.id, self.x, self.y)

        for things in self.to_do_list:
            exec(things)

class Chip(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)

        self.player_n = '#000000'
        
        self.game.say('Choose a color for player 1', \
                      'Click "OK" when you\'re done')
        self.player_1 = colorchooser.askcolor()[1]
        
        self.game.say('Choose a color for player 2', \
                      'Click "OK" when you\'re done')
        self.player_2 = colorchooser.askcolor()[1]

        self.turn = 0
        self.players = [self.player_1, self.player_2]
        
        self.id = self.game.canvas.create_oval(10, 10, 40, 40,
                                               fill=self.players[self.turn], \
                                               state='hidden')

    def move(self):
        pass

g = Game()

c = Chip(g)

g.mainloop()
