import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
image = pygame.image.load(
    "./Images/Objects/banner/Ci2logo.png").convert_alpha()
image = pygame.transform.scale(image, (100, 100))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    screen.blit(image, (50, 50))
    pygame.display.flip()
