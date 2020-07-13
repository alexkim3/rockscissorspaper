from pathlib import Path
from pyglet import sprite
from pyglet import app
from pyglet import image
from pyglet.window import Window
from pyglet.window import mouse
from pyglet.window import key
from pyglet import graphics
from pyglet import gl
from pyglet import text
import random


ROCK = 0
PAPER = 1
SCISSORS = 2
#these values can be changed to modify the game
window = Window(1100, 600)
#transform player's options
o_rock_pos = (950, 350)
o_paper_pos = (950, 250)
o_scissors_pos = (950, 150)
#transform big choice
players_choice_pos = (650, 200)
comps_choice_pos = (150, 200)
questionmark_pos = (50, 250)

its_a_tie = 0 # if the game is evaluated as "its a tie", the value turns 1
#image properties
play_image_size = (265, 215)
choice_image_size = (94, 76)

#global labels
gameover_screen = text.Label("x win!", font_size = 24)
tie_label = text.Label(f"It's a tie!", font_size = 20, x = 550, y = 250, anchor_x="center")
chose_one = text.Label(f"click \non one:", font_size = 20, x = 1050, y = 470, width = 100,
                                align="center", anchor_x = "right", anchor_y="center", multiline=True)

@window.event
def on_draw():
    window.clear()
    game.draw()
    game.restart_draw()
    #pc_start.draw()
    chose_one.draw()
    if its_a_tie == 1:
         tie_label.draw()

@window.event
def on_mouse_press(x, y, b, mod):
    #x = user.click_record[0]
    #y = user.click_record[1]
    game.user_switch(x, y)

@window.event
def on_key_press(symbol, modyfiers):
    global round_no, score
    if game.round_no > 3:
        if symbol == key.SPACE:
            game.round_no = 1
            game.score = [0, 0]
            game.restart_draw()

#create a bounding box area of the image and evaluate if user clicked in the bounding box area
def bounding_box(v1, v2, v_pos, v_size):
        x_pos_BB = range(v_pos[0], v_pos[0]+v_size[0])
        y_pos_BB = range(v_pos[1], v_pos[1]+v_size[1])
        if v1 in x_pos_BB and v2 in y_pos_BB:
            return (x_pos_BB, y_pos_BB)



class Game():
    def __init__(self):
        #score information
        self.round_no = 1 # the round will always begin from number 1
        self.score = [0, 0]
        #self.click_record = [0, 0]
        self.player = User()
        self.player2 = PC()

    def user_switch(self, x, y):
        if game.round_no < 4:
            player_choice = self.player.play(x, y)
            player2_choice = self.player2.play()
            self.evaluate(player_choice, player2_choice)

    def restart_draw(self):
        if self.round_no == 4:
            if self.score[0] > self.score[1]:
                self.gameover_screen = text.Label(f"Computer wins!\nPress space to restart", font_size = 24, x = 550, y = 30, anchor_x = "center")
                self.gameover_screen.draw()
            elif self.score[1] > self.score[0]:
                self.gameover_screen = text.Label(f"You win!\nPress space to restart", font_size = 24, x = 550, y = 30, anchor_x = "center")
                self.gameover_screen.draw()
    #score and round information screen from the beginning of the game
    def draw(self):
        #global player_score_screen, pc_score_screen, round_screen
        self.player.user_draw()
        text.Label(f"Player's\nscore: {str(self.score[1])}",
                                    font_size = 30, x = 800, y = 520, width = 300,
                                    align="center", anchor_x = "center", anchor_y="center", multiline=True).draw()
        text.Label(f"Computer's\nscore: {str(self.score[0])}",
                                    font_size = 30, x = 280, y = 520, width = 300,
                                    align="center", anchor_x = "center", anchor_y="center", multiline=True).draw()
        if self.round_no >= 3: # if the round is higher than 3, stop the number at 3 (dont rise the number to 4)
            self.round_screen = text.Label(f"round: 3", font_size = 40, x = 550, y = 80, anchor_x="center").draw()
        else:
            self.round_screen = text.Label(f"round: {self.round_no}", font_size = 40, x = 550, y = 80, anchor_x="center").draw()

    #this function takes a player's and computer's choice and based of evaluate adds score to player, computer or nobody
    def evaluate(self, player, computer):


        win_list = [
          (ROCK, SCISSORS),
          (SCISSORS, PAPER),
          (PAPER, ROCK)
        ]

            #player wins
        if (player, computer) in win_list:
            self.score[1] = self.score[1] + 1 #adds score number
            its_a_tie = 0
            self.round_no = self.round_no + 1 #adds round number
            #computer wins
        elif (computer, player) in win_list:
            self.score[0] = self.score[0] + 1
            its_a_tie = 0
            self.round_no = self.round_no + 1
            #its a tie
        elif player == computer:
            its_a_tie = 1

class Player():
    image_dir = Path(__file__).parent / "images"
    options_all = graphics.Batch()
    def __init__(self):
        pass


class PC(Player):
    def __init__(self):
        self.image_pc_rock = image.load(self.image_dir / "choice_pc-01.png")
        self.image_pc_paper = image.load(self.image_dir / "choice_pc-02.png")
        self.image_pc_scissors = image.load(self.image_dir / "choice_pc-03.png")
        self.image_questionmark = image.load(self.image_dir / "questionmark.png")
        self.pc_start = sprite.Sprite(self.image_pc_rock, comps_choice_pos[0], comps_choice_pos[1], batch = self.options_all)
        self.questionmark = sprite.Sprite(self.image_questionmark, questionmark_pos[0], questionmark_pos[1], batch = self.options_all)
        self.pc_options = [self.image_pc_rock, self.image_pc_paper, self.image_pc_scissors]

        # computer chose randomly from rock/paper/scissors
    def play(self):
        pc_option = random.choice([ROCK, PAPER, SCISSORS])
        self.pc_start = sprite.Sprite(self.pc_options[pc_option], x = 150, y = 200, batch = self.options_all)
        return pc_option

    #def pc_draw():


class User(Player):
    def __init__(self):
        self.image_option_player_rock = image.load(self.image_dir / "small_choice_player-01.png")
        self.image_option_player_paper = image.load(self.image_dir / "small_choice_player-02.png")
        self.image_option_player_scissors = image.load(self.image_dir / "small_choice_player-03.png")
        self.image_player_rock = image.load(self.image_dir / "choice_player-01.png")
        self.image_player_paper = image.load(self.image_dir / "choice_player-02.png")
        self.image_player_scissors = image.load(self.image_dir / "choice_player-03.png")
        self.option_player_rock = sprite.Sprite(self.image_option_player_rock, o_rock_pos[0], o_rock_pos[1], batch = self.options_all)
        self.option_player_paper = sprite.Sprite(self.image_option_player_paper, o_paper_pos[0], o_paper_pos[1], batch = self.options_all)
        self.option_player_scissors = sprite.Sprite(self.image_option_player_scissors, o_scissors_pos[0], o_scissors_pos[1], batch = self.options_all)
        self.chosen_image = self.image_player_rock
        self.images = [self.image_player_rock, self.image_player_paper, self.image_player_scissors]

    def user_draw(self):
        self.player_start = sprite.Sprite(self.chosen_image, players_choice_pos[0], players_choice_pos[1], batch = self.options_all)
        self.options_all.draw()

    def play(self, x, y):
        if bounding_box(x, y, o_rock_pos, choice_image_size):
            self.choice = ROCK
        elif bounding_box(x, y, o_paper_pos, choice_image_size):
            self.choice = PAPER
        elif bounding_box(x, y, o_scissors_pos, choice_image_size):
            self.choice = SCISSORS
        else:
            pass # nothing changes if clicked outside the bounding boxes
        self.chosen_image = self.images[self.choice]
        return self.choice


game = Game()
app.run()
