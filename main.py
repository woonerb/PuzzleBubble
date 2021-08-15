import pygame
import os

# 버블 클래스 생성
class Bubble(pygame.sprite.Sprite):
    def __init__(self, image , color, position):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)

#맵 만들기
def setup():
    global map
    map = [
        #["R","R","Y","Y","B","B","G","G",]
        list("RRYYBBGG"),
        list("RRYYBBG/"),  # '/' 로 표현한 것은 버블이 위치할 수 없는 곳임을 의미
        list("BBGGRRYY"),
        list("BGGRRYY/"),
        list("........"),  # '.' 로 표현한 것은 비어있는 공간임을 의미  
        list("......./"),
        list("........"),
        list("......./"),
        list("........"),
        list("......./"),
        list("........")
    ]

    for row_idx, row in enumerate(map):
        for col_idx, col in enumerate(row):
            if col in [".","/"]:
                continue 
            pos = get_bubble_position(row_idx,col_idx)  # 버블 표시할 좌표 찾기
            image = get_bubble_image(col)               # 버블의 이미지 찾기
            bubble_group.add(Bubble(image,col,pos))     # 버블객체를 만들어서 정보를 담아서 bubble_group에 삽입


#버블을 표시해야 할 좌표를 찾는다
def get_bubble_position(row_idx, col_idx):
    pos_x= col_idx * CELL_SIZE + (BUBBLE_WIDTH //2)   # ->파이썬에서 /쓰면 실수로 나오니 나머지 버리고 정수만 얻고 싶을때 사용
    pos_y= row_idx * CELL_SIZE + (BUBBLE_HEIGHT //2)
    if row_idx %2==1 : pos_x += CELL_SIZE //2         #홀수 행일때는 버블의 반칸 만큼 오른쪽으로 밀려있어야 하므로
    return pos_x, pos_y

#버블을 표시할 이미지를 가져온다
def get_bubble_image(color):
    if color == "R":
        return bubble_images[0]
    elif color == "Y":
        return bubble_images[1]
    elif color == "B":
        return bubble_images[2]
    elif color == "G":
        return bubble_images[3]
    elif color == "P":
        return bubble_images[4]
    else:
        return bubble_images[5]


pygame.init()
screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))  # 화면 크기 설정
pygame.display.set_caption("Puzzle Bobble")                     # 게임명 설정
clock = pygame.time.Clock()


# 배경이미지 불러오기
current_path = os.path.dirname(__file__)  #실행하는 py경로 가져오기
background = pygame.image.load(os.path.join(current_path, "background.png"))  #배경

# 버블 이미지 불러오기
bubble_images = [
     pygame.image.load(os.path.join(current_path, "red.png")).convert_alpha()                  #빨강 공
    ,pygame.image.load(os.path.join(current_path, "yellow.png")).convert_alpha()               #노랑 공
    ,pygame.image.load(os.path.join(current_path, "blue.png")).convert_alpha()                 #파랑 공
    ,pygame.image.load(os.path.join(current_path, "green.png")).convert_alpha()                #초록 공
    ,pygame.image.load(os.path.join(current_path, "purple.png")).convert_alpha()               #보라 공
    ,pygame.image.load(os.path.join(current_path, "black.png")).convert_alpha()                #검정 공
]

#게임 관련 변수
CELL_SIZE =     56
BUBBLE_WIDTH =  56
BUBBLE_HEIGHT = 62

map = [] #맵
bubble_group = pygame.sprite.Group()  # 버블을 생성해서 관리할 공간
setup()

running = True
while running:
    clock.tick(60) #FPS를 60으로 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False                                     #반복문 탈출하도록 running변수 변경

    screen.blit(background, (0,0))                              #(0,0) background 띄우기     
    bubble_group.draw(screen)
    pygame.display.update()
     
pygame.quit()