import pygame , random , sys , heapq

# heapq: For implementing priority queues, used in A* algorithm.

#COULEURS
WHITE = (255,255,255)
BLACK = (0,0,0)
DARKBLUE = (57, 16, 123)
LAVENDER = (239, 181, 255)

#CONTANTES
WIDTH , HEIGHT = 1000 , 600
FPS = 60
GAME_SIZE = 3
TILE_SIZE = 200


# Initialization
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define a font and create a surface with the message
pygame.font.init()
font = pygame.font.SysFont(None, 50)
win_message = font.render("Congratulations! You won!", True, BLACK)
win_message_rect = win_message.get_rect(center=(WIDTH // 3, HEIGHT // 4))

#load all images
Shuffle_Button = pygame.image.load("assets/shuffle_btn.png")
Reset_Button = pygame.image.load("assets/reset_btn.png")
# BFS_Button = pygame.image.load("assets/bfs.png")
A_etoile = pygame.image.load("assets/A_etoile_btn.png")

message = pygame.image.load("assets/reset_message.png")

image1 = pygame.image.load("assets/11.png")
image2 = pygame.image.load("assets/22.png")
image3 = pygame.image.load("assets/33.png")
image4 = pygame.image.load("assets/44.png")
image5 = pygame.image.load("assets/55.png")
image6 = pygame.image.load("assets/66.png")
image7 = pygame.image.load("assets/77.png")
image8 = pygame.image.load("assets/88.png")
empty_image = pygame.image.load("assets/empty.png")


# images is a dictionary where the keys represent numbers (0 to 8) and the values represent corresponding images.
images={0:empty_image, 1:image1, 2:image2, 3:image3, 4:image4, 5:image5, 6:image6, 7:image7, 8:image8}

# This method is called when a new instance of the Button class is created.
class Button:
    # constructor (__init__ method) for the Button class
    def __init__(self, image, position):
        # self is this in java
        self.image = image
        self.rect = self.image.get_rect(topleft=position)

    # This method is responsible for drawing the button onto the screen.
    def draw(self, screen):
        # blit=draw 
        screen.blit(self.image, self.rect)

    def is_clicked(self, mouse_pos):
        #check if left mouse button is clicked on button
        return self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1

class Game:
    # constructor method (__init__), which is called when a new instance of the Game class is created.
    def __init__(self):
        pygame.init()
        # The caption appears in the title bar of the game window.
        pygame.display.set_caption("8-puzzle game")

        # The clock object will be used to control the frame rate of the game.
        self.clock = pygame.time.Clock()

        # This initializes the player_grid attribute of the Game instance by calling the create_grid() method. The player_grid represents the current state of the puzzle grid as seen by the player.
        self.player_grid = self.create_grid()
        # This initializes the completed_grid attribute of the Game instance by calling the create_grid() method. The completed_grid represents the state of the puzzle grid that the player needs to achieve to win the game.
        self.completed_grid = self.create_grid()

        # This attribute keeps track of whether the tiles have been shuffled at least once during the game.
        self.shuffle_once = False

        # This list will store the states of the puzzle grid after each shuffle operation. It is used to allow the player to undo shuffles if they choose to do so.
        self.shuffled_grids = []
    
    
    
    # generating the initial state of the puzzle grid
    def create_grid(self):
        GRID = []
        # initial number to be assigned to the cells of the grid
        CELL_NUM = 1

        # Within these loops, each cell of the grid is assigned a unique number starting from 1 and incremented by 1 for each cell.
        # These numbers represent the initial configuration of the puzzle, where each cell contains a unique number except for the empty cell.
        for row in range(GAME_SIZE):
            # For each iteration, a new empty list is appended to GRID, effectively creating a new row in the puzzle grid.
            GRID.append([])
            for col in range(GAME_SIZE):
                GRID[row].append(CELL_NUM)
                CELL_NUM += 1
        GRID[2][2] = 0 # empty cell
        return GRID

    def draw_grid(self):
        # This loop iterates over horizontal lines that will be drawn on the grid. The loop starts from -1 (to ensure the first line starts at the edge of the grid) and goes up to GAME_SIZE * TILE_SIZE (the size of the grid in pixels) with a step of TILE_SIZE (the size of each tile in pixels).
        for horz_line in range(-1,GAME_SIZE * TILE_SIZE , TILE_SIZE):
            pygame.draw.line(screen , BLACK , (horz_line,0) , (horz_line,GAME_SIZE * TILE_SIZE))
        for vert_line in range(-1,GAME_SIZE * TILE_SIZE, TILE_SIZE):
            pygame.draw.line(screen, BLACK,(0,vert_line),(GAME_SIZE * TILE_SIZE ,vert_line))

    def draw_tiles(self):
        # This loop iterates over each row of the player_grid attribute of the Game instance.
        # enumerate(self.player_grid) provides both the row index (row) and the row itself (list_row).
        for row , list_row in enumerate(self.player_grid):
            for col , element in enumerate(list_row):
                for i in (images.keys()):
                    # if element is 1, it means that the current cell contains the number 1. The code then checks images[1] to get the corresponding image to draw for the tile with the number 1. 
                    if element == i:
                        self.rect = images[i].get_rect()

                        # This method updates the position of the Rect object based on the row and column indices.
                        self.update(row ,col)

                        # Finally, it blits (draws) the image onto the game screen at the position determined by the Rect object's y and x attributes.
                        screen.blit(images[i],(self.rect.y,self.rect.x))


    # updating the position of the rectangle (Rect object) associated with a tile image.          
    def update(self , x , y):
        # x and y represent the row and column indices of the tile.
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
    

    # determine if a tile in the puzzle grid can be moved to the empty space (the space without a number) based on the given row and column indices of the tile.
    def valid_move(self , row , col):
        empty_x , empty_y = self.find_empty_tile(self.player_grid)
        return (row == empty_x and abs(col - empty_y) == 1) or (col == empty_y and abs(row - empty_x) == 1)
    
    # determine which tile was clicked based on the mouse coordinates. 
    def clicked_tile(self,mouse_x , mouse_y):
        x = mouse_y // TILE_SIZE 
        y = mouse_x // TILE_SIZE
        return x , y
    
    def find_empty_tile(self , grid):
        for x , list_row in enumerate(grid):
            for y , element in enumerate(list_row):
                if element == 0:
                    return x , y
                
    def handle_move(self , tile_x , tile_y):
        empty_x , empty_y = self.find_empty_tile(self.player_grid)
        if self.valid_move(tile_x , tile_y):
            self.player_grid[empty_x][empty_y] = self.player_grid[tile_x][tile_y]
            self.player_grid[tile_x][tile_y] = 0
        draw_all()
        
    def shuffle(self):
        reset_button.image = Reset_Button
        for i in range(99):
            empty_x , empty_y = self.find_empty_tile(self.player_grid)
            directions = [(empty_x + 1 , empty_y),(empty_x - 1 , empty_y),(empty_x , empty_y + 1),(empty_x , empty_y - 1)]
            valid_moves = [(x , y) for x , y in directions if 0 <= x <= 2 and 0 <= y <= 2]
            next_x , next_y = random.choice(valid_moves)
            self.handle_move(next_x , next_y)
        self.shuffle_once = True
        shuffle_grid = [row[:] for row in self.player_grid]
        self.shuffled_grids.append(shuffle_grid)

    def win(self):
        return self.player_grid == self.completed_grid
    
    def reset(self):
        if self.shuffle_once:
            if self.shuffled_grids == []:
                reset_button.image = message
            else:
                self.player_grid = self.shuffled_grids[0]
                self.shuffled_grids = []
    

    # the A* search algorithm
    def a_etoile_solution(self):
        # A copy of the current puzzle grid.
        current_grid = [row[:] for row in self.player_grid]

        # (number of moves).
        depth = 0

        # A set to keep track of visited states (grids).
        visited = set()

        # (deque) A priority queue that stores tuples containing the evaluation score, grid state, and path taken to reach that state.
        priority_queue = [(self.evaluate_state2(current_grid , depth), current_grid, [])]

        while priority_queue:
            _, grid , path = heapq.heappop(priority_queue)
            visited.add(tuple(map(tuple, grid)))

            if self.evaluate_state(grid) == 0:
                return path
            
            neighbors = self.generate_grids(grid)
            depth += 1
            for neighbor in neighbors:
                if tuple(map(tuple, neighbor)) not in visited:
                    heapq.heappush(priority_queue, (self.evaluate_state2(neighbor , depth), neighbor , path+[neighbor]))
        return None

    # def bfs_solution(self):
    #     current_grid = [row[:] for row in self.player_grid]
    #     visited = set()
    #     priority_queue = [(self.evaluate_state(current_grid), current_grid, [])]

    #     while priority_queue:
    #         _, grid , path = heapq.heappop(priority_queue)
    #         visited.add(tuple(map(tuple, grid)))  # Convertir la grille en tuple pour vérifier la visite
            
    #         if self.evaluate_state(grid) == 0:
    #             return path
            
    #         neighbors = self.generate_grids(grid)
    #         for neighbor in neighbors:
    #             if tuple(map(tuple, neighbor)) not in visited:
    #                 heapq.heappush(priority_queue, (self.evaluate_state(neighbor), neighbor , path+[neighbor]))
    #     return None
        
    def evaluate_state(self, state):
        # Fonction d'évaluation : retourne le nombre de tuiles mal placées
        nbre_unplaced_tiles = 0
        for i in range(GAME_SIZE):
            for j in range(GAME_SIZE):
                if state[i][j] != self.completed_grid[i][j]:
                    nbre_unplaced_tiles += 1
        return nbre_unplaced_tiles
    
    def evaluate_state2(self, state , depth):
        nbre_unplaced_tiles = 0
        for i in range(GAME_SIZE):
            for j in range(GAME_SIZE):
                if state[i][j] != self.completed_grid[i][j]:
                    nbre_unplaced_tiles += 1
        return nbre_unplaced_tiles + depth

    def generate_grids(self, grid):
        neighbors = []
        empty_x, empty_y = self.find_empty_tile(grid)
        directions = [(empty_x + 1, empty_y), (empty_x - 1, empty_y), (empty_x, empty_y + 1), (empty_x, empty_y - 1)]
        for next_x, next_y in directions:
            if 0 <= next_x < GAME_SIZE and 0 <= next_y < GAME_SIZE:
                new_grid = [row[:] for row in grid]
                new_grid[empty_x][empty_y], new_grid[next_x][next_y] = new_grid[next_x][next_y], new_grid[empty_x][empty_y]
                neighbors.append(new_grid)
        return neighbors

#Create buttons
shuffle_button = Button(Shuffle_Button, (WIDTH - 300, HEIGHT - 575))
reset_button = Button(Reset_Button, (WIDTH - 300, HEIGHT - 425))
# bfs_button = Button(BFS_Button, (WIDTH - 300, HEIGHT - 275))
a_etoile_button = Button(A_etoile, (WIDTH - 300, HEIGHT - 125))

def draw_buttons():
    shuffle_button.draw(screen)
    reset_button.draw(screen)
    # bfs_button.draw(screen)
    a_etoile_button.draw(screen)

def draw_all():
    screen.fill(DARKBLUE)
    game.draw_tiles()
    game.draw_grid()
    draw_buttons()

#GAME LOOP
game = Game()
game.shuffle()
moves = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x , mouse_y = pygame.mouse.get_pos()
            mouse_pos = (mouse_x,mouse_y)
            clicked_x , clicked_y = game.clicked_tile(mouse_x , mouse_y)
            if shuffle_button.is_clicked(mouse_pos):
                moves = 0
                game.shuffle()
            elif reset_button.is_clicked(mouse_pos):
                moves = 0
                game.reset()
            # elif bfs_button.is_clicked(mouse_pos):
            #     win_path = game.bfs_solution()
            #     if win_path:
            #         for i , grid_step in enumerate(win_path):
            #             game.player_grid = grid_step
            #             moves = i + 1
            #             print("move n°",moves)
            #             for row in grid_step:
            #                 print(row)
            #             draw_all()
            #             pygame.display.update()
            #             pygame.time.wait(500)
            #     else:
            #         print("Aucune solution trouvée.")
            elif a_etoile_button.is_clicked(mouse_pos):
                win_path = game.a_etoile_solution()
                if win_path:
                    for i , grid_step in enumerate(win_path):
                        game.player_grid = grid_step
                        moves = i + 1
                        print("move n°",moves)
                        for row in grid_step:
                            print(row)
                        draw_all()
                        pygame.display.update()
                        pygame.time.wait(500)
                else:
                    print("Aucune solution trouvée.")
            else:
                if pygame.mouse.get_pressed()[0] == 1 and not game.win():
                    game.handle_move(clicked_x, clicked_y)
                    moves += 1
    if game.win():
        screen.fill(DARKBLUE)
        shuffle_button.draw(screen)
        reset_button.draw(screen)
        screen.blit(win_message, win_message_rect)
        moves_text = font.render(f"Moves: {moves}", True, BLACK)
        moves_rect = moves_text.get_rect(midtop=(WIDTH // 3, HEIGHT // 2))
        screen.blit(moves_text, moves_rect)
        
    else:
        draw_all()
    game.clock.tick(FPS)
    pygame.display.update()