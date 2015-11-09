# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos=[WIDTH/2, HEIGHT/2]
    ball_vel=[0,0]
    if direction==True:
        ball_vel[0]=random.randrange(2, 4)
        ball_vel[1]=-random.randrange(1, 3)
    elif direction==False:
        ball_vel[0]=-random.randrange(2, 4)
        ball_vel[1]=-random.randrange(1, 3)

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1=0
    score2=0
    
    #found it easier if they were lists, sorry
    paddle1_pos = [HALF_PAD_WIDTH, 0]  
    paddle2_pos = [WIDTH-HALF_PAD_WIDTH, 0]
    paddle1_vel=[0,0]
    paddle2_vel=[0,0]
    spawn_ball(True)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0]+= ball_vel[0]
    ball_pos[1]+= ball_vel[1]
    if ball_pos[1]< BALL_RADIUS:
        ball_vel[1]= -ball_vel[1]
    elif ball_pos[1]>= (HEIGHT-1)-BALL_RADIUS:
        ball_vel[1]= -ball_vel[1]
        
    # draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel[1]
    if paddle1_pos[1] < 0:
        paddle1_pos = [HALF_PAD_WIDTH,0]
    elif paddle1_pos[1] > HEIGHT - PAD_HEIGHT -1:
        paddle1_pos = [HALF_PAD_WIDTH, HEIGHT - PAD_HEIGHT -1]
        
    paddle2_pos[1] += paddle2_vel[1]
    if paddle2_pos[1] < 0:
        paddle2_pos = [WIDTH - HALF_PAD_WIDTH - 1, 0]
    elif paddle2_pos[1] > HEIGHT - PAD_HEIGHT - 1:
        paddle2_pos = [WIDTH - HALF_PAD_WIDTH - 1, HEIGHT - PAD_HEIGHT - 1]

    # draw paddles
    canvas.draw_line(paddle1_pos, (paddle1_pos[0], paddle1_pos[1]+PAD_HEIGHT), PAD_WIDTH, 'White')
    canvas.draw_line(paddle2_pos, (paddle2_pos[0], paddle2_pos[1]+PAD_HEIGHT), PAD_WIDTH, 'White')
    
    # determine whether paddle and ball collide  
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if ball_pos[1]+ BALL_RADIUS > paddle1_pos[1] and ball_pos[1]+ BALL_RADIUS < paddle1_pos[1] + PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] *= 1.1
        else:
            score2 += 1 
            spawn_ball(RIGHT)
    elif ball_pos[0] >= (WIDTH - PAD_WIDTH)- BALL_RADIUS:
        if ball_pos[1] + BALL_RADIUS > paddle2_pos[1] and ball_pos[1] + BALL_RADIUS < paddle2_pos[1] + PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] *= 1.1
        else:
            score1 += 1
            spawn_ball(LEFT)
    
    # draw scores
    canvas.draw_text(str(score1), (250,50), 40, "White")
    canvas.draw_text(str(score2), (330,50), 40, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
 
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -=3
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] +=3
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] -=3
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] +=3

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] +=3
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] -=3
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] +=3
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] -=3

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
new = frame.add_button('New game', new_game, 200)


# start frame
new_game()
frame.start()