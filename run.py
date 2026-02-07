# Example file showing a circle moving on screen
import pygame
import random
from collections import deque

# pygame setup
pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0

# game setup
cell_size = 40
move_delay = 50
move_timer = 0
real_food_count = 0
fake_food_count = 0

game_over_msg = "GAME OVER"
game_info_msg = ""

class GameInfo:
    def __init__(self, msg):
        self.msg = msg
        
    def draw(self, msg, screen):
        font = pygame.font.SysFont(None, 100)
        text = font.render(msg)
        screen.blit(text, (cell_size// 2, cell_size// 2))

class FoodCount:
    def __init__(self):
        self.real_food_count = real_food_count
        
    def draw(self, screen):
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Food Count: {real_food_count}", True, "red")
        screen.blit(text, (0,0))
    

class Clocker:
    def __init__(self):
        self.current_time = pygame.time.get_ticks()
        
    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        self.last_time = current_time
        
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Play Time: {current_time // 1000}", True, "white")
        screen.blit(text, (0, 20))
        
class FakeFood:
    def __init__(self):
        self.position = (random.randint(0, screen_width // cell_size - 1) * cell_size,
                         random.randint(0, screen_height // cell_size - 1) * cell_size)

    def draw(self, screen):
        pygame.draw.rect(screen, "red", (self.position[0], self.position[1], cell_size, cell_size))

class Food:
    def __init__(self):
        self.position = (random.randint(0, screen_width // cell_size - 1) * cell_size,
                         random.randint(0, screen_height // cell_size - 1) * cell_size)

    def draw(self, screen):
        pygame.draw.rect(screen, "red", (self.position[0], self.position[1], cell_size, cell_size))

class Snake:
    def __init__(self):
        self.parts = deque([
            (screen_width // 2, screen_height // 2),
            (screen_width // 2 - cell_size, screen_height // 2),
            (screen_width // 2 - 2 * cell_size, screen_height // 2)
        ])
        # self.position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        # snake body segments
        self.direction = random.choice(["up", "down", "left", "right"])
        
        # snake speed in pixels per second
        self.speed = 100
        
        # check if the snake has eaten food and needs to grow
        self.update_length = False

    def draw(self, screen):
        for part in self.parts:
            pygame.draw.rect(screen, "green", (part[0], part[1], cell_size, cell_size))

    def move(self):
        head_x, head_y = self.parts[-1]

        if self.direction == 'up':
            head_y -= cell_size
        elif self.direction == 'down':
            head_y += cell_size
        elif self.direction == 'left':
            head_x -= cell_size
        elif self.direction == 'right':
            head_x += cell_size

        # push new head
        self.parts.append((head_x, head_y))

        if not self.update_length:
            # pop tail
            self.parts.popleft()
        else:
            self.update_length = False
            
    def move_direction(self, direction):
        if direction == "up" and self.direction != "down":
            self.direction = "up"
        elif direction == "down" and self.direction != "up":
            self.direction = "down"
        elif direction == "left" and self.direction != "right":
            self.direction = "left"
        elif direction == "right" and self.direction != "left":
            self.direction = "right"

# initialize game objects
snake = Snake()
food = Food()
fakeFood = FakeFood()
clocker = Clocker()
foodCount = FoodCount()
msg = GameInfo(game_over_msg)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        ##### Key handling    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snake.move_direction("up")
            elif event.key == pygame.K_s:
                snake.move_direction("down")
            elif event.key == pygame.K_a:
                snake.move_direction("left")
            elif event.key == pygame.K_d:
                snake.move_direction("right")

    # Key handling
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #     snake.move("up")
    # if keys[pygame.K_s]:
    #     snake.move("down")
    # if keys[pygame.K_a]:
    #     snake.move("left")
    # if keys[pygame.K_d]:
    #     snake.move("right")
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    move_timer += clock.get_time()
    if move_timer >= move_delay:
        snake.move()
        move_timer = 0

        # interact with food
        # head is last element in snake parts
        head_x, head_y = snake.parts[-1]
        
        # check if head is on food
        if (head_x, head_y) == food.position or (head_x, head_y) == fakeFood.position:
            
            if(food.position):
                snake.update_length = True  # next move will not pop tail -> grow
                real_food_count += 1
                
            elif(fakeFood.position):
                msg
                break
            
            
            # respawn food (avoid spawning on snake body)
            while True:
                food = Food()
                if food.position not in snake.parts:
                    break

    snake.draw(screen)
    food.draw(screen)
    fakeFood.draw(screen)
    foodCount.draw(screen)
    
    clocker.draw(screen)

    # pygame.draw.circle(screen, "red", snake, 40)

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #     snake.y -= 300 * dt
    # if keys[pygame.K_s]:
    #     snake.y += 300 * dt
    # if keys[pygame.K_a]:
    #     snake.x -= 300 * dt
    # if keys[pygame.K_d]:
    #     snake.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # clock tick is used to control how fast the screen updates
    dt = clock.tick(60) / 1000

pygame.quit()
