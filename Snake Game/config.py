import pygame

# Initialize pygame
pygame.init()

# Set screen dimensions
width, height = 900, 900
cell_size = 30

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
gray = (50, 50, 50)

# Initialize screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Clock and font
clock = pygame.time.Clock()
snake_speed = 3
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
top_score_font = pygame.font.SysFont("comicsansms", 20)

# Load sounds
eat_sound = pygame.mixer.Sound("Sounds/eat.mp3")

# Number of foods
num_foods = 30

# Top scores file
scores_file = "top_scores.txt"
