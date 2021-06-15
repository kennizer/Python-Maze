import pygame, sys, random,textwrap
class Direction: 
    UP = 1 
    DOWN = -1
    LEFT = 2
    RIGHT = -2 
    STOPPED = 0 
class Cell: 
    def __init__ (self,x,y): 
        self.directions = [] 
        self.cords = (x,y)
    def addDirection (self, direction): 
        self.directions.append(direction)
def valid (x,y, width, height): 
    return x>=0 and x<width and y>=0 and y<height
def print_maze (maze): 
    for m in maze: 
        cords,direction = m 
        print("Coord: ", cords.cords, " Direction: ", direction)
def print_full_maze(maze):
    for i in range (len(maze)): 
        row = maze[i]
        for r in row: 
            print ("Coords: ", r.cords, "Directions available", r.directions, end=" ")
        print("\n")
def draw_maze (maze, x_size, y_size, screen, thickness,min_x, min_y): 
    color = (255,255,255)
    closed = True 
    index = 0
    for m in maze: 
        cell,direction = m 
        x,y = cell.cords
        print("X: ", x,"Y: ", y, "Direction: ", direction, "Index: ",index)
        if direction==Direction.UP: 
            width = x_size - thickness
            height = y_size 
            rectangle = (x*x_size+ thickness/2+min_x, y*y_size- y_size/2 + min_y, width, height)
            pygame.draw.rect(screen, color, rectangle, 0)
        elif direction==Direction.DOWN: 
            width = x_size - thickness
            height = y_size 
            rectangle = (x*x_size+ thickness/2+min_x, y*y_size+ y_size/2 + min_y, width, height)
            pygame.draw.rect(screen, color, rectangle, 0)
        elif direction==Direction.RIGHT: 
            width = x_size
            height = y_size - thickness
            rectangle = (x*x_size +x_size/2+min_x, y*y_size+ thickness/2 + min_y, width, height)
            pygame.draw.rect(screen, color, rectangle, 0)
        elif direction==Direction.LEFT: 
            width = x_size
            height = y_size -thickness
            rectangle = (x*x_size - x_size/2 +min_x , y*y_size + thickness/2 + min_y, width, height)
            pygame.draw.rect(screen, color, rectangle, 0)

def draw_square(x,y,x_size,y_size, color, screen,thickness,min_x,min_y, up):
    rectangle = None
    if up:
        rectangle = (x*x_size+thickness/2+min_x, y*y_size+min_y, x_size-thickness, y_size)
    else: 
        rectangle = (x*x_size+thickness/2+min_x, y*y_size+thickness/2+min_y, x_size, y_size-thickness)
    pygame.draw.rect(screen,color,rectangle,0)

def draw_circle (x,y, x_size,y_size,radius, color, screen,thickness, min_x, min_y): 
    x_center = x * x_size + x_size/2 + min_x 
    y_center = y * y_size + y_size/2 + min_y
    pygame.draw.circle(screen, color, (x_center,y_center), radius, thickness) 

def draw_grid(x_size, y_size, cell_x, cell_y, screen, thickness, min_y, min_x): 
    color = (0,0,0)
    for x in range (cell_x): 
        for y in range (cell_y): 
            pygame.draw.rect(screen, color, (x*x_size+min_x, y*y_size+min_y, x_size, y_size), thickness)

def draw_fast_maze(maze, x_size,y_size,screen, thickness): 
    visited = [] 
    colors = [(255,0,0), (0,255,0), (0,0,255)]
    index = 0
    for m in maze: 
        cell,direction = m 
        x,y = cell.cords 
        if (x,y) in visited: 
            index = (index+1)%3
        else: 
            visited.append((x,y))
        pygame.draw.rect(screen, colors[index],(x*x_size, y*y_size,x_size, y_size), thickness)
def generate_maze(start, end,  size_x, size_y):
    start_x, start_y = start 
    maze = [] 
    #first initialization of the maze 
    for i in range (size_x): 
        row = [] 
        for j in range (size_y): 
            new_cell = Cell(i,j)
            row.append(new_cell)
        maze.append(row)
    steps = [] 
    queue = [maze[start_x][start_y]]
    visited = []
    while len(queue)>0: 
        current_cell = queue[0]
        x,y = current_cell.cords
        if current_cell.cords == end: 
            queue = queue[1:]
            steps.append((current_cell, Direction.STOPPED))
        else: 
            next_cell = None 
            directions = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]
            for d in current_cell.directions: 
                directions.remove(d)
            #picks only directions that it has never explored 
            ''' 
            It first checks which direction is good and if the direction is valid, it will choose that direction accordsingly
            If there is no direction available, the queue is popped,
            '''
            v = False
            temp_x = x 
            temp_y = y 
            while len(directions)>0 and (next_cell is None or next_cell.cords in visited): 
                v = False 
                direction = random.choice(directions) 
                opposite = direction * -1
                temp_x = x 
                temp_y = y 
                if direction == Direction.UP:  
                    temp_y-=1 
                elif direction == Direction.DOWN:  
                    temp_y+=1 
                elif direction == Direction.LEFT:  
                    temp_x-=1 
                elif direction == Direction.RIGHT:  
                    temp_x+=1 
                directions.remove(direction)
                v = valid(temp_x,temp_y,size_x,size_y)
                next_cell = maze[temp_x][temp_y] if v else None 
            if next_cell is None or next_cell.cords in visited: 
                queue = queue[1:]
                steps.append((current_cell, Direction.STOPPED))
            else: 
                next_cell.addDirection(opposite)
                current_cell.addDirection(direction)
                if direction == Direction.UP: 
                    steps.append((current_cell, Direction.UP))
                elif direction == Direction.DOWN:
                    steps.append((current_cell, Direction.DOWN))
                elif direction == Direction.LEFT:
                    steps.append((current_cell, Direction.LEFT))
                elif direction == Direction.RIGHT:
                    steps.append((current_cell, Direction.RIGHT))
                queue.insert(0,next_cell)
        visited.append(current_cell.cords)
    return steps,maze


cell_x = 20 
cell_y = 20
start_x, start_y = 0,0 
end_x, end_y = cell_x-1, cell_y-1

steps, maze = generate_maze((start_x,start_y), (end_x,end_y), cell_x, cell_y)

colors = [(255,0,0), (0,255,0), (0,0,255), (0,0,0)]
erase = (255,255,255)
width = 500     
height = 500 

additional_x = 50
additional_y = 50
total_width = width + additional_x * 2 
total_height = height + additional_y*2
thickness = 5
radius = 7
top_font_size = 32
bottom_font_size = 20 
top_text = "A " + str(cell_x) + " x "+ str(cell_y)+ " Maze"
bottom_text = "Navigate from the red dot to the blue dot"

x_size = width/ cell_x
y_size = height/ cell_y

suggestion = "Want to speed things up? Press + to solve the puzzle."
inspiration_iterations = 0 
timer = 5000
inspiration_font_size = 16
inspirational_file = open('quotes.txt', 'r')
lines = inspirational_file.readlines() 
inspiration = []
for l in lines: 
    inspiration.append(l.strip())

pygame.init() 
screen = pygame.display.set_mode((total_width, total_height))
screen.fill(erase)

top_font = pygame.font.Font('freesansbold.ttf', top_font_size)
bottom_font = pygame.font.Font('freesansbold.ttf', bottom_font_size)
inspiration_font = pygame.font.Font('freesansbold.ttf', inspiration_font_size)
top_box = top_font.render(top_text, True, colors[3], erase)
top_rectangle = top_box.get_rect()
top_rectangle.center = (total_width/2, additional_y/2)
bottom_box = bottom_font.render(bottom_text, True, colors[3], erase)
bottom_rectangle = bottom_box.get_rect()
bottom_rectangle.center = (total_width/2, total_height-additional_y/2)
inspiration_rectangle = (0, total_height-additional_y/2)
last_font = bottom_font
last_rectangle = bottom_rectangle 
draw_grid (x_size, y_size, cell_x, cell_y, screen, thickness, additional_x, additional_y)
draw_maze(steps,x_size,y_size,screen,thickness,additional_x, additional_y)

up_start = Direction.UP in maze[start_x][start_y].directions or Direction.DOWN in maze[start_x][start_y].directions
up_end = Direction.UP in maze[end_x][end_y].directions or Direction.DOWN in maze[end_x][end_y].directions

circle_x, circle_y = start_x,start_y

draw_square(start_x,start_y,x_size,y_size,colors[0],screen,thickness,additional_x, additional_y, up_start)
draw_square(end_x,end_y,x_size,y_size,colors[2],screen,thickness,additional_x, additional_y, up_end)
draw_circle(circle_x,circle_y, x_size,y_size, radius, colors[1], screen, 0, additional_x,additional_y)
screen.blit(top_box,top_rectangle)
screen.blit(bottom_box,bottom_rectangle)

pygame.time.set_timer(pygame.USEREVENT, timer)

objective_achieved = False
while True: 
    draw_square(start_x,start_y,x_size,y_size,colors[0],screen,thickness,additional_x, additional_y, up_start)
    draw_square(end_x,end_y,x_size,y_size,colors[2],screen,thickness,additional_x, additional_y, up_end)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and not objective_achieved:
            directions = maze[circle_x][circle_y].directions
            #erasing
            draw_circle(circle_x,circle_y, x_size, y_size, radius, erase,screen,thickness,additional_x,additional_y)
            if event.key == pygame.K_LEFT: 
                if Direction.LEFT in directions: 
                    circle_x-=1
            elif event.key == pygame.K_RIGHT: 
                if Direction.RIGHT in directions: 
                    circle_x+=1
            elif event.key == pygame.K_UP: 
                if Direction.UP in directions: 
                    circle_y-=1
                draw_circle(circle_x,circle_y, x_size, y_size, radius, erase,screen,thickness,additional_x,additional_y )
            elif event.key == pygame.K_DOWN: 
                if Direction.DOWN in directions: 
                    circle_y+=1
            draw_circle(circle_x,circle_y, x_size, y_size, radius, colors[1],screen,thickness,additional_x,additional_y)
        elif event.type == pygame.USEREVENT and not objective_achieved:
            erase_text = last_font.render(bottom_text,True, erase,erase)
            screen.blit(erase_text,bottom_rectangle) 
            new_text = None
            if inspiration_iterations % 10 !=0:
                bottom_text = suggestion if inspiration_iterations%5==0 else random.choice(inspiration)
                new_text = inspiration_font.render(bottom_text, True, colors[3], erase)
                last_font = inspiration_font
                screen.blit(new_text,inspiration_rectangle)
                last_rectangle = inspiration_rectangle
            else: 
                bottom_text = "Navigate from the red dot to the blue dot"
                new_text = bottom_font.render(bottom_text, True, colors[3], erase)
                last_font = bottom_font
                screen.blit(new_text,bottom_rectangle)
                last_rectangle = bottom_rectangle
            inspiration_iterations+=1
    if (circle_x,circle_y) == (end_x,end_y): 
        objective_achieved = True 
        erase_text = last_font.render(bottom_text,True, erase,erase)
        screen.blit(erase_text,last_rectangle)
        bottom_text = "Objective achieved! Press + to show path"
        new_text = bottom_font.render(bottom_text, True, colors[3], erase)
        screen.blit(new_text,bottom_rectangle)
        last_rectangle = bottom_rectangle
    pygame.display.update()
