#imports
from pprint import pprint
import pygame 
import random

#Initialize pygame
pygame.init()
pygame.mixer.init()


#Window size
res = (640, 800)

#display window
screen = pygame.display.set_mode(res)

#fps
last_time = pygame.time.get_ticks()
fps = 10
time_per_frame = 1000 / fps
clock = pygame.time.Clock()

#Vars
drop_piece_x = 400
drop_piece_y = 50
lines = 10
columns = 7
game_state = 1
piece_position = 3
last_row_piece = 10
drop_start_position = 3
drop_beggining = 0
isDropping = 0
piece_fall_timer = 5
chosen_img = 0
draw_start_x = 64
draw_start_y = 64


#faz referencias que depois uma linha altera as outras todas
#game_matrix = [[0]*columns]*lines
game_matrix = [
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,2,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,2,0,0,0],
    [0,0,0,1,0,0,0]
]


def count_column_filled(column_number):
    counted = 0
    for i in range(0, len(game_matrix)):
        if(game_matrix[i][column_number] == 0):
            counted  += 1
    #print("COUNTER -> " + str(counted))
    return counted


def falling_neighbours(position, pos, fall_timer):
    x = position[0]
    y = position[1]
    if (pos == "a" and game_matrix[x-1][y] >= 0 and fall_timer>0):
        return(game_matrix[x][y-1])
    elif (pos == "a" and game_matrix[x-1][y] >= 0 and fall_timer==0):
        return(game_matrix[x+1][y-1])
    elif (pos == "d" and game_matrix[x+1][y] <= columns-1 and fall_timer>0):
        return(game_matrix[x][y+1])
    elif (pos == "d" and game_matrix[x+1][y] <= columns-1 and fall_timer==0):
        return(game_matrix[x+1][y+1])


def placement_neighbours(x, y, pos, piece, piece_position):

    max_neigh = 2
    curr_neigh = 1
    arr_result= [x,y]
    count_same = 1

    if(pos == "hl"):
        for i in range(curr_neigh, max_neigh):
            if(piece_position-1 >= 0):
                if(game_matrix[x][y-curr_neigh] == piece):
                    arr_result.append((x,y-curr_neigh))
                    count_same += 1
                    piece_position -= 1
                else:
                    break

    if(pos == "hr"):
        for i in range(curr_neigh, max_neigh):
            if(piece_position+1 <= 6):
                if(game_matrix[x][y+curr_neigh] == piece):
                    arr_result.append((x,y+curr_neigh))
                    count_same += 1
                    piece_position += 1
                else:
                    break

    return arr_result, count_same


# loaders
background_img = pygame.image.load("bg.png")
logo = pygame.image.load("logo.png")
img1 = pygame.image.load("G1.png")
img2 = pygame.image.load("G2.png")
img3 = pygame.image.load("G3.png")
img4 = pygame.image.load("G4.png")

#python doesn't play because of (libmodplug-1.dll)
#pygame.mixer.music.load('Game_Audio.mp4')
#pygame.mixer.music.play(-1)

#Game cycle
while (game_state==True):
    print(isDropping)
    if(isDropping == 0):
        piece_falling = random.randint(1, 4)

    game_matrix[drop_beggining][piece_position] = piece_falling

    #vars 
    draw_start_x = 64
    draw_start_y = 64

    for i in game_matrix:
        print(i)

    #draw background 
    screen.blit(background_img, (0,0))
    screen.blit(logo, (100,10))

    #draw pieces on window
    for lines_gm in game_matrix:
        draw_start_x = 64
        draw_start_y += 64
        for columns_gm in lines_gm:
            if(columns_gm==1):
                screen.blit(img1, (draw_start_x,draw_start_y))
            elif(columns_gm==2):
                screen.blit(img2, (draw_start_x,draw_start_y))
            elif(columns_gm==3):
                screen.blit(img3, (draw_start_x,draw_start_y))
            elif(columns_gm==4):
                screen.blit(img4, (draw_start_x,draw_start_y))
            draw_start_x += 64

    clock.tick(fps)

    # Process system events
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            exit()

    #saber quandos espacos estao vazios
    last_row_piece = count_column_filled(piece_position)
    print(last_row_piece)

    #pressed keys
    key = pygame.key.get_pressed()

    if(key[pygame.K_a]):
        if(piece_position > 0):
            if(falling_neighbours((drop_beggining, piece_position), "a", piece_fall_timer) == 0):
                #move left
                game_matrix[drop_beggining][piece_position] = 0
                game_matrix[drop_beggining][piece_position-1] = piece_falling
                piece_position -= 1

                ####CHECK the error happening falling to the right with empty spaces bellow


    if(key[pygame.K_d]):
        if(piece_position < 6):
            if(falling_neighbours((drop_beggining, piece_position), "d", piece_fall_timer) == 0):
                #move right
                game_matrix[drop_beggining][piece_position] = 0
                game_matrix[drop_beggining][piece_position+1] = piece_falling
                piece_position += 1

    if(key[pygame.K_s]):
        piece_fall_timer = 0


    #sets the value to 1, so the value doesnt get randomized
    isDropping = 1
    
    #Falling of the piece.. clearing the previous one 
    if(piece_fall_timer == 0):
        if(count_column_filled(piece_position) == 0):
            print("GAME OVER")
            screen.fill((100,100,0))
            #exit()

        #Insert the piece in the board
        game_matrix[drop_beggining][piece_position] = 0
        drop_beggining += 1
        game_matrix[drop_beggining][piece_position] = piece_falling
        piece_fall_timer = 5

        

    #reach last value on the column
    if(drop_beggining == last_row_piece):
        game_matrix[drop_beggining][piece_position] = piece_falling

        max_neigh = 3
        curr_neigh = 1
        arr_result= [(drop_beggining, piece_position)]
        final_array = []
        count_same = 1
        pposition = piece_position
        drop_position = drop_beggining
 



        #check left
        for i in range(curr_neigh, max_neigh):
            if(pposition-1 >= 0 and game_matrix[drop_beggining][pposition-curr_neigh] == piece_falling):
                arr_result.append((drop_beggining,pposition-curr_neigh))
                count_same += 1
                pposition -= 1
            else:
                break

        pposition = piece_position

        #check right
        for i in range(curr_neigh, max_neigh):
            if(pposition+1 <= 6 and game_matrix[drop_beggining][pposition+curr_neigh] == piece_falling):
                arr_result.append((drop_beggining,pposition+curr_neigh))
                count_same += 1
                pposition += 1
            else:
                break



        final_array = list(set(arr_result))
        #print("total count left + right->"+str(count_same))
        #print(final_array)

        if(count_same>=3):
            falling_pieces = drop_beggining
            for row in final_array:
                print(row[0])
                print(row[1])
                game_matrix[row[0]][row[1]] = 0

                #Pieces falling down according to the array deleted
                for i in range(falling_pieces, 0, -1):
                    game_matrix[i][row[1]] = game_matrix[i-1][row[1]]
                game_matrix[i-1][row[1]] = 0

            ## when all of them fall.. check them for neighbours and see if can popout more

        
        count_same = 1

        #check vertical +2 bellow
        for i in range(curr_neigh, max_neigh):
            if(drop_position <= 7 and game_matrix[drop_beggining+curr_neigh][pposition] == piece_falling):
                arr_result.append((drop_beggining+curr_neigh,pposition))
                count_same += 1
                drop_beggining += 1
            else:
                break

        print(arr_result)
        print("total count vertical->"+str(count_same))

        final_array = list(set(arr_result))
        print(final_array)

        if(count_same>=3):
            falling_pieces = drop_beggining
            for row in final_array:
                print(row[0])
                print(row[1])
                game_matrix[row[0]][row[1]] = 0


        isDropping = 0
        drop_beggining = 0

    #give time to the player move to the sides
    piece_fall_timer -= 1

    pygame.display.flip()
    pygame.display.update()


