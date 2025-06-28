import pygame
import sys
from board import Board
from ai_agent import Connect4AI

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
BOARD_ROWS = 6
BOARD_COLS = 7
SQUARE_SIZE = WINDOW_SIZE // BOARD_COLS
BOARD_HEIGHT = SQUARE_SIZE * BOARD_ROWS
PADDING = 50  # Increased padding for text area
TEXT_AREA_HEIGHT = 60  # Fixed height for text area

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DGrey = (100, 100, 100)

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, BOARD_HEIGHT + TEXT_AREA_HEIGHT))
pygame.display.set_caption("Connect4")

def draw_board(board, game_over=False, winner=None, difficulty='medium', ai_first=False):
    # Clear the entire screen with Dark Grey
    screen.fill(DGrey)
    
    # Draw the board background
    pygame.draw.rect(screen, DGrey, (0, 0, WINDOW_SIZE, BOARD_HEIGHT))
    
    # Draw the pieces area background
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            pygame.draw.circle(screen, WHITE,
                             (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                              row * SQUARE_SIZE + SQUARE_SIZE // 2),
                             SQUARE_SIZE // 2 - 5)
    
    # Draw the pieces
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board.board[row][col] != 0:
                color = YELLOW if board.board[row][col] == 2 else RED  # AI is yellow, player is red
                pygame.draw.circle(screen, color,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                  row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                 SQUARE_SIZE // 2 - 5)
    
    # Draw game over message if game is over
    if game_over and winner is not None:
        font = pygame.font.Font(None, 74)
        if winner == 0:
            text = font.render('Draw!', True, WHITE)
        else:
            text = font.render(f'{"AI" if winner == 2 else "Player"} Wins!', True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, BOARD_HEIGHT // 2))
        # Draw semi-transparent overlay
        s = pygame.Surface((WINDOW_SIZE, BOARD_HEIGHT))
        s.set_alpha(128)
        s.fill(BLACK)
        screen.blit(s, (0,0))
        screen.blit(text, text_rect)
    
    # Draw the text area background
    pygame.draw.rect(screen, BLACK, (0, BOARD_HEIGHT, WINDOW_SIZE, TEXT_AREA_HEIGHT))
    
    # Draw the status text
    font = pygame.font.Font(None, 36)
    if not game_over:
        status_text = f"Difficulty: {difficulty} ({'AI' if ai_first else 'Human'} moves first)"
    else:
        status_text = "Press R to restart"
    text = font.render(status_text, True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, BOARD_HEIGHT + TEXT_AREA_HEIGHT // 2))
    screen.blit(text, text_rect)
    
    pygame.display.flip()

def draw_difficulty_menu(screen):
    # Clear the screen
    screen.fill(DGrey)
    
    # Draw title
    font = pygame.font.Font(None, 74)
    title = font.render('Select Difficulty', True, WHITE)
    title_rect = title.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 4))
    screen.blit(title, title_rect)
    
    # Draw instructions
    font = pygame.font.Font(None, 48)
    instructions = font.render('Press 1 for Easy, 2 for Medium, 3 for Hard', True, WHITE)
    instructions_rect = instructions.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
    screen.blit(instructions, instructions_rect)
    
    pygame.display.flip()

def draw_first_move_menu(screen):
    # Clear the screen
    screen.fill(DGrey)
    
    # Draw title
    font = pygame.font.Font(None, 74)
    title = font.render('Who Makes First Move?', True, WHITE)
    title_rect = title.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 4))
    screen.blit(title, title_rect)
    
    # Draw instructions
    font = pygame.font.Font(None, 48)
    instructions = font.render('Press A for AI, S for Human', True, WHITE)
    instructions_rect = instructions.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
    screen.blit(instructions, instructions_rect)
    
    pygame.display.flip()

def get_difficulty_choice():
    choice_made = False
    
    while not choice_made:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'Easy'
                elif event.key == pygame.K_2:
                    return 'Medium'
                elif event.key == pygame.K_3:
                    return 'Hard'
        
        draw_difficulty_menu(screen)
        pygame.time.Clock().tick(60)

def get_first_move_choice():
    choice_made = False
    
    while not choice_made:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    return 2  # AI moves first
                elif event.key == pygame.K_s:
                    return 1  # Human moves first
        
        draw_first_move_menu(screen)
        pygame.time.Clock().tick(60)

def main():
    board = Board(BOARD_ROWS, BOARD_COLS)
    
    # Map difficulty levels to AI strategies
    difficulty_to_strategy = {
        'Easy': 'hill_climbing',
        'Medium': 'simulated_annealing',
        'Hard': 'minimax'
    }
    
    while True:  # Main game loop
        # Get difficulty choice first
        difficulty = get_difficulty_choice()
        strategy = difficulty_to_strategy[difficulty]
        
        # Get first move choice
        choice = get_first_move_choice()
        ai_first = (choice == 2)  # Store who moves first
        
        # Initialize AI with selected strategy
        ai = Connect4AI(max_depth=4, strategy=strategy)
        
        # Reset game state
        board = Board(BOARD_ROWS, BOARD_COLS)
        board.set_first_player(2 if ai_first else 1)  # Set the correct first player
        game_over = False
        winner = None
        
        # If AI is chosen to move first
        if ai_first:
            ai_move = ai.get_move(board)
            board.make_move(ai_move)
        
        while not game_over:  # Game round loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart game
                        game_over = True  # Break out of game round loop
                        break  # Break out of game round loop to restart
                
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    x, y = event.pos
                    col = x // SQUARE_SIZE
                    
                    # Check if it's a valid move and it's the player's turn
                    if board.is_valid_move(col):
                        # When AI is first, player is 1; when human is first, player is 1
                        if board.current_player == 1:  # It's always player's turn when current_player is 1
                            # Make player's move
                            board.make_move(col)
                            
                            # Check for game over
                            winner = board.check_winner()
                            if winner is not None:
                                game_over = True
                            else:
                                # AI's turn
                                ai_move = ai.get_move(board)
                                if ai_move is not None and board.is_valid_move(ai_move):
                                    board.make_move(ai_move)
                                    
                                    # Check for game over again
                                    winner = board.check_winner()
                                    if winner is not None:
                                        game_over = True
                                else:
                                    # If AI couldn't make a valid move, end the game as a draw
                                    winner = 0  # 0 indicates a draw
                                    game_over = True
            
            # Draw the board and current difficulty
            draw_board(board, game_over, winner, difficulty, ai_first)
            pygame.time.Clock().tick(60)  # Limit frame rate to 60 FPS
        
        # Show game over screen and wait for restart
        if winner is not None:  # Only show game over screen if there's a winner or draw
            waiting_for_restart = True
            while waiting_for_restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        waiting_for_restart = False
                draw_board(board, game_over, winner, difficulty, ai_first)
                pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main() 