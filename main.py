import pygame

pygame.init()
screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))  # 화면 크기 설정
pygame.display.set_caption("Puzzle Bobble")                     # 게임명 설정
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60) #FPS를 60으로 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False                                     #반복문 탈출하도록 running변수 변경

            
pygame.quit()