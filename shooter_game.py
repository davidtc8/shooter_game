import pygame

pygame.init()

# Screen config
SCREEN_WIDTH = 800
## The screen height will be just 80% of the screen height
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter Game!")

# set framerate, this is important, so that the soldiers cannot move really fast 
clock = pygame.time.Clock()
FPS = 60

# Define player action variables 
moving_left = False
moving_right = False

# Define colours
BG = (144,201,120)

def draw_bg():
    screen.fill(BG)

# Soldier class
class Soldier(pygame.sprite.Sprite):
    def __init__(self, character_type, x, y, scale, speed):
        '''
        Parameter:
        character_type = what kind of character will it be?
        x = x position in the map
        y = y position in the map
        scale = how big the image is
        speed = how many pixels can the soldier move around
        '''
        # This just means that I'm going to inherit the functionality from the Sprite class
        pygame.sprite.Sprite.__init__(self)
        self.character_type = character_type
        self.speed = speed
        # This two variables will help with the movement of the soldier
        self.direction = 1
        self.flip =  False
        # Loading the image of the soldier
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        # self.update_time is just to keep track when the last animation was animated
        self.update_time = pygame.time.get_ticks()
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'img/{self.character_type}/Idle/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f'img/{self.character_type}/Run/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        ## It will create a rectangle position around the image, so we can manage it later on
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def move(self, moving_left, moving_right):
        #reset movement variables (delta x and delta y)
        dx = 0
        dy = 0

        #  assign movement variables if moving left or right 
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # update rectangle poistion
        self.rect.x += dx 
        self.rect.y += dy
    
    def update_animation(self):
        # update animation
        ANIMATION_COOLDOW = 100
        # udpate image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOW:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1 
        # if the animation has run out, then back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0 
            self.update_time = pygame.time.get_ticks()
    
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# creating the player instance of the class Soldier.
player = Soldier('player' ,200, 200, 3, 5)

# Loop running the game
game_is_on = True
while game_is_on:
    # Displaying
    clock.tick(FPS)
    draw_bg()
    player.update_animation()
    player.draw()
    # update player actions
    if moving_left or moving_right:
        player.update_action(1)#1 means run
    else:
        player.update_action(0)#0 means idle
    player.move(moving_left, moving_right)

    # This will give me all the events that are happening
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            game_is_on = False
        # Keyboard being pressed
        if event.type == pygame.KEYDOWN:
            # The K_a means that if you press the letter "a" on the keyboard
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            # IMPORTANT, this is amazing, so you can close the game using Escape while playing.
            if event.key == pygame.K_ESCAPE:
                game_is_on = False
        #keyboard button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()



