import pygame
import os  # sistema de arquivos
import random  # posição aleatória dos canos

# -------------------config constants-------------------
WIDTH_SCREEN = 500
HIGHT_SCREEN = 800

PIPE_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png"))
)
FLOOR_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "base.png"))
)
BACKGROUND_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bg.png"))
)
BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]

pygame.font.init()
FONT_POINTS = pygame.font.SysFont("arial", 20)


class Bird:
    # global
    imgs = BIRD_IMAGES

    # rotation animate
    max_rotation = 25
    speed_rotation = 20
    time_animate = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.hight = self.y
        self.time = 0
        self.count_image = 0
        self.image = self.imgs[0]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.hight = self.y

    def move(self):
        # DISPLACEMENT

        # S = S0 + v0 . t + a . t²/2
        self.time += 1
        displacement = 1.5 * (self.time**2) + self.speed * self.time

        # MAX DISPLACEMENT

        if displacement > 16:
            displacement = 16
        elif displacement < 0:  # optional
            displacement -= 2

        self.y += displacement

        # ANGLE
        if displacement < 0 or self.y < (self.hight + 50):
            if self.angle < self.max_rotation:
                self.angle = self.max_rotation
        else:
            if self.angle > -90:
                self.angle -= self.speed_rotation

    def draw(self, screen):
        # animate bird
        self.count_image += 1

        if self.count_image < self.time_animate:  # execute time 1
            self.image = self.imgs[0]
        elif self.count_image < self.time_animate * 2:  # execute time 2
            self.image = self.imgs[1]
        elif self.count_image < self.time_animate * 3:  # execute time 3
            self.image = self.imgs[2]
        elif self.count_image < self.time_animate * 4:  # execute time 4
            self.image = self.imgs[1]
        elif self.count_image >= self.time_animate * 4 + 1:
            self.image = self.imgs[0]
            self.count_image = 0  # initial state

        # if the bird is falling, change!
        if self.angle <= -80:
            self.image = self.img[1]
            self.count_image = self.time_animate * 2

        # draw image
        rotate_image = pygame.transform.rotate(self.image, self.angle)
        position_center = self.image.get_rect(topleft=(self.x, self.y)).center
        hitbox_bird = rotate_image.get_rect(center=position_center)

        # (image, position)
        screen.blit(rotate_image, hitbox_bird.topleft)

    def get_mask(self):  # hitbox bird with pipes
        return pygame.mask.from_surface(self.image)


class Pipe:
    DISTANCE = 200
    SPEED = 5

    def __init__(self, x):
        self.x = x
        self.hight = 0
        self.position_top = 0
        self.position_base = 0
        # (x axis and y axis)
        self.pipe_top = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.pipe_base = PIPE_IMAGE
        self.passed = False
        self.define_hight()

    def define_hight(self):
        self.hight = random.randrange(50, 450)
        self.position_base = self.hight - self.pipe_top.get_height()
        self.position_base = self.hight + self.DISTANCE

    def move(self):
        self.x -= self.SPEED

    def draw(self, screen):
        screen.blit(self.pipe_top, (self.x, self.position_top))
        screen.blit(self.pipe_base, (self.x, self.position_base))

    def collision(self, bird):
        bird_hitbox = bird.get_mask()
        top_hitbox = pygame.mask.from_surface(self.pipe_top)
        base_hitbox = pygame.mask.from_surface(self.pipe_base)

        distance_top = (self.x - bird.x, self.position_top - round(bird.y))
        distance_base = (self.x - bird.x, self.position_base - round(bird.y))

        top_point = bird_hitbox.overlap(top_hitbox, distance_top)
        base_point = bird_hitbox.overlap(base_hitbox, distance_base)

        if base_point or top_point:
            return True
        else:
            return False


class Floor:
    SPEED = 5
    WIDTH = FLOOR_IMAGE.get_width()
    IMAGE = FLOOR_IMAGE

    def __init__(self, y):
        self.y = y
        self.floor1 = 0
        self.floor2 = self.floor1 + self.WIDTH

    def move(self):
        self.floor1 -= self.SPEED
        self.floor2 -= self.SPEED

        if self.floor1 + self.WIDTH < 0:
            self.floor1 = self.floor1 + self.WIDTH
        if self.floor2 + self.WIDTH < 0:
            self.floor2 = self.floor2 + self.WIDTH

    def draw(self, screen):
        screen.blit(self.IMAGE, (self.floor1, self.y))
        screen.blit(self.IMAGE, (self.floor2, self.y))


def draw_screen(screen, birds, pipes, floor, points):
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    for bird in birds:  # machine learning in birds
        bird.draw(screen)

    for pipe in pipes:
        pipe.draw(screen)

    texto = FONT_POINTS.render(f"Score: {points}", 1, (255, 255, 255))
    screen.blit(texto, (WIDTH_SCREEN - 10 - texto.get_width(), 10))
    floor.draw(screen)
    pygame.display.update()


def main():
    birds = [Bird(230, 350)]
    floor = Floor(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((WIDTH_SCREEN, HIGHT_SCREEN))
    points = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        # fps
        clock.tick(30)

        # key pressed by user with machine learning
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()

            # move things in screen
            for bird in birds:
                bird.move()
            floor.move()

            # move pipe
            add_pipe = False
            remove_pipes = []
            for pipe in pipes:
                for i, bird in enumerate(birds):  # take bird id (i)
                    if pipe.collision(bird):
                        birds.pop(i)  # remove bird from list

                    if not pipe.passed and bird.x > pipe.x:
                        pipe.passed = True
                        add_pipe = True
            pipe.move()
            if pipe.x + pipe.pipe_top.get_width() < 0:
                remove_pipes.append(pipe)
    if add_pipe:
        points += 1
        pipes.append(Pipe(600))
    for pipe in remove_pipes:
        pipes.remove(pipe)

        #colision with sky 
        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > floor.y or bird.y < 0: #floor
                birds.pop(i)
        
        draw_screen( screen, birds, floor, pipes, points)

if __name__ == '__main__': #if import file it will not run
    main()