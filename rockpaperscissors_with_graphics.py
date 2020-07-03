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

#players options
options_all = graphics.Batch()
image_dir = Path(__file__).parent / "images"
image_option_player_rock = image.load(image_dir / "small_choice_player-01.png")
image_option_player_paper = image.load(image_dir / "small_choice_player-02.png")
image_option_player_scissors = image.load(image_dir / "small_choice_player-03.png")
option_player_rock = sprite.Sprite(image_option_player_rock, o_rock_pos[0], o_rock_pos[1], batch = options_all)
option_player_paper = sprite.Sprite(image_option_player_paper, o_paper_pos[0], o_paper_pos[1], batch = options_all)
option_player_scissors = sprite.Sprite(image_option_player_scissors, o_scissors_pos[0], o_scissors_pos[1], batch = options_all)

# player choice
image_player_rock = image.load(image_dir / "choice_player-01.png")
image_player_paper = image.load(image_dir / "choice_player-02.png")
image_player_scissors = image.load(image_dir / "choice_player-03.png")
chosen_image = image_player_rock
player_start = sprite.Sprite(chosen_image, players_choice_pos[0], players_choice_pos[1], batch = options_all)

image_pc_rock = image.load(image_dir / "choice_pc-01.png")
image_pc_paper = image.load(image_dir / "choice_pc-02.png")
image_pc_scissors = image.load(image_dir / "choice_pc-03.png")
image_questionmark = image.load(image_dir / "questionmark.png")
pc_start = sprite.Sprite(image_pc_rock, comps_choice_pos[0], comps_choice_pos[1])
questionmark = sprite.Sprite(image_questionmark, questionmark_pos[0], questionmark_pos[1], batch = options_all)
pc_options = [image_pc_rock, image_pc_paper, image_pc_scissors]

#global labels
gameover_screen = text.Label("x win!", font_size = 24)
tie_label = text.Label(f"It's a tie!", font_size = 20, x = 550, y = 250, anchor_x="center")
chose_one = text.Label(f"click \non one:", font_size = 20, x = 1050, y = 470, width = 100,
                                align="center", anchor_x = "right", anchor_y="center", multiline=True)

@window.event
def on_draw():
    global its_a_tie, options_all
    window.clear()
    options_all.draw()
    game.draw()
    game.restart()
    player_start.draw()
    pc_start.draw()
    chose_one.draw()
    if its_a_tie == 1:
         tie_label.draw()


@window.event
def on_mouse_press(x, y, b, mod):
    global chosen_image, score, player_start
    game.click_record[0] = x
    game.click_record[1] = y
    #options change
    if game.round_no < 4:
        if bounding_box(x, y, o_rock_pos, choice_image_size):
            chosen_image = image_player_rock
            player_start = sprite.Sprite(chosen_image, x = 650, y = 200)
            game.evaluate(image_player_rock, computer_chose())
        elif bounding_box(x, y, o_paper_pos, choice_image_size):
            chosen_image = image_player_paper
            player_start = sprite.Sprite(chosen_image, x = 650, y = 200)
            game.evaluate(image_player_paper, computer_chose())
        elif bounding_box(x, y, o_scissors_pos, choice_image_size):
            chosen_image = image_player_scissors
            player_start = sprite.Sprite(chosen_image, x = 650, y = 200)
            game.evaluate(image_player_scissors, computer_chose())
        else:
            pass # nothing changes if clicked outside the bounding boxes



@window.event
def on_key_press(symbol, modyfiers):
    global round_no, score
    if game.round_no > 3:
        if symbol == key.SPACE:
            game.round_no = 1
            game.score = [0, 0]
            game.restart()

#create a bounding box area of the image and evaluate if user clicked in the bounding box area
def bounding_box(v1, v2, v_pos, v_size):
        x_pos_BB = range(v_pos[0], v_pos[0]+v_size[0])
        y_pos_BB = range(v_pos[1], v_pos[1]+v_size[1])
        if v1 in x_pos_BB and v2 in y_pos_BB:
            return (x_pos_BB, y_pos_BB)

# computer chose randomly from rock/paper/scissors
def computer_chose():
    global pc_choice, pc_start
    pc_option = random.choice(pc_options)
    pc_start = sprite.Sprite(pc_option, x = 150, y = 200)
    return pc_option

class Game():
    def __init__(self):
        #score information
        self.round_no = 1 # the round will always begin from number 1
        self.score = [0, 0]
        self.click_record = [0, 0]

    def restart(self):
        #round
        if self.round_no > 3: # if the round is higher than 3, stop the number at 3 (dont rise the number to 4)
            self.round_screen = text.Label(f"round: 3", font_size = 40, x = 550, y = 80, anchor_x="center")
            if self.score[0] > self.score[1]:
                self.gameover_screen = text.Label(f"Computer wins!\nPress space to restart", font_size = 24, x = 550, y = 30, anchor_x = "center")
                self.gameover_screen.draw()
            elif self.score[1] > self.score[0]:
                self.gameover_screen = text.Label(f"You win!\nPress space to restart", font_size = 24, x = 550, y = 30, anchor_x = "center")
                self.gameover_screen.draw()
    #score and round information screen from the beginning of the game
    def draw(self):
        #global player_score_screen, pc_score_screen, round_screen
        text.Label(f"Player's\nscore: {str(self.score[1])}",
                                    font_size = 30, x = 800, y = 520, width = 300,
                                    align="center", anchor_x = "center", anchor_y="center", multiline=True).draw()
        text.Label(f"Computer's\nscore: {str(self.score[0])}",
                                    font_size = 30, x = 280, y = 520, width = 300,
                                    align="center", anchor_x = "center", anchor_y="center", multiline=True).draw()
        self.round_screen = text.Label(f"round: {self.round_no}", font_size = 40, x = 550, y = 80, anchor_x="center").draw()

    #this function takes a player's and computer's choice and based of evaluate adds score to player, computer or nobody
    def evaluate(self, player, computer):
        #global player_score_screen, pc_score_screen, round_no, round_screen, score, its_a_tie
        win_list = [
          (image_player_rock, image_pc_scissors),
          (image_player_scissors, image_pc_paper),
          (image_player_paper, image_pc_rock)
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

game = Game()
app.run()
