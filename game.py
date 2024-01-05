
import pygame
import random
import os,sys

# Initialize pygame
pygame.init()

# Set the dimensions of the screen
screen_width = 540
screen_height = 600
cell_size = 60

# Set colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
font = pygame.font.SysFont('comicsans', 40)  # adjust font size

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Random Sudoku Grid")

# Game states
in_main_menu = False
selecting_difficulty = False
in_game = True
difficulty = "Easy"  # Default difficulty

# Main Menu
def display_main_menu(selected_option):
    screen.fill(white)
    title_text = font.render("Sudoku Game", True, black)
    play_text = font.render("Play Game", True, black)
    instructions_text = font.render("Instructions", True, black)
    exit_text = font.render("Exit", True, black)

    # Display menu options
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))
    screen.blit(play_text, (screen_width // 2 - play_text.get_width() // 2, 150))
    screen.blit(instructions_text, (screen_width // 2 - instructions_text.get_width() // 2, 200))
    screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, 250))

    # Draw boxes around the selected option
    if selected_option == "Play":
        pygame.draw.rect(screen, black, (240, 145, 120, 30), 2)
    elif selected_option == "Instructions":
        pygame.draw.rect(screen, black, (220, 195, 160, 30), 2)
    elif selected_option == "Exit":
        pygame.draw.rect(screen, black, (230, 245, 140, 30), 2)

    for event in pygame.event.get():
	    if event.type == pygame.MOUSEBUTTONDOWN:
	        print(pygame.mouse.get_pos())

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 150 < mouse_y < 170:  # Play Game
            	print('Play')
#            	return "Play"
            elif 200 < mouse_y < 220:  # Instructions
            	print('Instructions')
#            	return "Instructions"
            elif 250 < mouse_y < 270:  # Exit
            	print('Exit')
            	return "NA"
#            	return "Exit"
    pygame.display.update()

# Difficulty Selection
def select_difficulty():
    screen.fill(white)
    difficulty_text = font.render("Select Difficulty", True, black)
    easy_text = font.render("Easy", True, black)
    medium_text = font.render("Medium", True, black)
    hard_text = font.render("Hard", True, black)

    # Display difficulty options
    screen.blit(difficulty_text, (screen_width // 2 - difficulty_text.get_width() // 2, 50))
    screen.blit(easy_text, (screen_width // 2 - easy_text.get_width() // 2, 150))
    screen.blit(medium_text, (screen_width // 2 - medium_text.get_width() // 2, 200))
    screen.blit(hard_text, (screen_width // 2 - hard_text.get_width() // 2, 250))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 250 < mouse_x < 350 and 150 < mouse_y < 170:  # Easy
                global difficulty
                difficulty = "Easy"
                global selecting_difficulty
                global in_game
                selecting_difficulty = False
                in_game = True
            # Add event handling for other difficulty options (e.g., Medium, Hard)

    pygame.display.update()

# Generate a random Sudoku grid
def generate_sudoku_grid():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(20):  # Fill 20 random cells
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        num = random.randint(1, 9)
        if is_safe(grid, row, col, num):
            grid[row][col] = num
    return grid

# Check if it's safe to place a number in a cell
def is_safe(grid, row, col, num):
    return (not used_in_row(grid, row, num) and
            not used_in_col(grid, col, num) and
            not used_in_box(grid, row - row % 3, col - col % 3, num))

# Check if a number is used in a row
def used_in_row(grid, row, num):
    return num in grid[row]

# Check if a number is used in a column
def used_in_col(grid, col, num):
    return any(row[col] == num for row in grid)

# Check if a number is used in a 3x3 box
def used_in_box(grid, box_start_row, box_start_col, num):
    for i in range(3):
        for j in range(3):
            if grid[i + box_start_row][j + box_start_col] == num:
                return True
    return False

# Draw the Sudoku grid on the screen
def draw_sudoku_grid(grid, selected_cell, font):
    for i in range(9):
        for j in range(9):
            color = black
            if selected_cell is not None and (i, j) == selected_cell:
                pygame.draw.rect(screen, blue, (j * cell_size, i * cell_size, cell_size, cell_size), 3)  # Add a blue border
            pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size), 1)
            if grid[i][j] != 0:
                text = font.render(str(grid[i][j]), True, black)
                screen.blit(text, (j * cell_size + 20, i * cell_size + 10))

    for i in range(9):
        color = black if i % 3 == 0 else white
        pygame.draw.line(screen, color, (0, i * cell_size), (screen_width, i * cell_size), 2)
        pygame.draw.line(screen, color, (i * cell_size, 0), (i * cell_size, screen_height), 2)

# Get the cell value that is clicked with the mouse
def get_clicked_cell(pos):
    x, y = pos
    row = y // cell_size
    col = x // cell_size
    return row, col


# Game Loop
def game_loop():
	# Main loop
	running = True
	generate_new_grid = True  # Flag to generate a new grid initially
	sudoku_grid = generate_sudoku_grid()  # Generate a new Sudoku grid initially
	selected_cell = None  # Variable to store the selected cell

	while running:
	    for event in pygame.event.get():
	        if event.type == pygame.QUIT:
	            running = False
	        elif event.type == pygame.KEYDOWN:
	            if event.key == pygame.K_r:  # Check if "R" key is pressed
	                generate_new_grid = True  # Set the flag to generate a new grid
	        elif event.type == pygame.MOUSEBUTTONDOWN:
	            if event.button == 1:  # Check if left mouse button is clicked
	                pos = pygame.mouse.get_pos()
	                row, col = get_clicked_cell(pos)
	                if 0 <= row < 9 and 0 <= col < 9:
	                    selected_cell = (row, col)  # Set the selected cell
	        elif event.type == pygame.KEYDOWN:
	            if event.unicode.isdigit() and selected_cell is not None:
	                row, col = selected_cell
	                sudoku_grid[row][col] = int(event.unicode)  # Update the selected cell with the entered number

	    if generate_new_grid:
	        sudoku_grid = generate_sudoku_grid()
	        generate_new_grid = False  # Reset the flag after generating the new grid

	    screen.fill(white)
	    draw_sudoku_grid(sudoku_grid, selected_cell, font)  # Pass the selected_cell to the draw function
	    pygame.display.flip()

	pygame.quit()


# Inside the main loop
running = True
selected_option = ""  # Initialize the selected option
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if in_main_menu:
        selected_option = display_main_menu(selected_option)
        if selected_option == "Play":
            in_main_menu = False
            selecting_difficulty = True
    elif selecting_difficulty:
        select_difficulty()
    elif in_game:
        game_loop()

pygame.quit()
