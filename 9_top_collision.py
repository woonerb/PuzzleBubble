import pygame
import os
import random
import math


# 버블 클래스 생성
class Bubble(pygame.sprite.Sprite):
    def __init__(self, image , color, position=(0,0)):
        super().__init__()
        self.image  = image
        self.color  = color
        self.rect   = image.get_rect(center=position)
        self.radius = 9

    #버블의 위치 세팅해주는 setter
    def set_rect(self, position):   
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)    

    def set_angle(self, angle):
        self.angle = angle
        self.rad_angle = math.radians(self.angle) #각도를 라디안수치로 변경

    def move(self):
        to_x = self.radius * math.cos(self.rad_angle)
        to_y = self.radius * math.sin(self.rad_angle) * -1

        #버블의 이동 처리
        self.rect.x += to_x
        self.rect.y += to_y       

        #벽에 충돌 처리  (좌측을 벗어나거나 or 우측을 벗어난경우)
        if self.rect.left <0 or self.rect.right > screen_width:
            self.set_angle(180 - self.angle)                     #벽에 부딪히면 튕기게


# 발사대 클래스 생성
class LaunchPad(pygame.sprite.Sprite):
    def __init__(self, image, position,angle):
        super().__init__()
        self.image = image          #움직여진 각도의 이미지
        self.position = position
        self.rect = image.get_rect(center=position)
        self.angle = angle
        self.original_image = image  #0도의 이미지

    #draw 함수 정의
    #sprite.Group()은 draw함수가 있으나, sprite는 draw 함수가 없으므로 여기서 정의한다
    def draw(self, screen):
        screen.blit(self.image,self.rect)   #screen에 image를 rect에 맞추서 표시해준다.    

    # 회전 
    def rotate(self, angle):
        self.angle += angle

        if self.angle > 170:
            self.angle =170
        elif self.angle <10:
            self.angle = 10     

        #원본이미지의 각도 변화 시켜서 업데이트 시키도록 하자
        #self.original_image를 self.angle 각도 만큼 변화시켜서 self.image에 준다.
        #1은 몇배로 확대하느냐를 의미하는 변수
        self.image = pygame.transform.rotozoom(self.original_image,self.angle,1)
        
        #rect는 게임 시작시 position을 기준으로 더해진 각도로 
        self.rect = self.image.get_rect(center=self.position)     


#맵 만들기
def setup():
    global map
    map = [
        
        list("...R...."),
        list("......./"),
        list("........"),
        list("......./"),

        #list("RRYYBBGG"),
        #,list("RRYYBBG/"),  # '/' 로 표현한 것은 버블이 위치할 수 없는 곳임을 의미
        #,list("BBGGRRYY"),
        #list("BGGRRYY/"),
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


#다음번에 발사할 버블을 준비한다
def prepare_bubbles():
    global CURR_BUBBLE, NEXT_BUBBLE
    
    #다음에 쏠 버블이 있다면, 현재 버블에 다음 버블을 넣는다.
    if NEXT_BUBBLE:
            CURR_BUBBLE = NEXT_BUBBLE
    #다음에 쏠 버블이 없다면, 버블을 새로 만든다.
    else:
        CURR_BUBBLE = create_bubble() #새 버블 만들기
    
    CURR_BUBBLE.set_rect((screen_width// 2, 624))        #버블의 위치를 발사대 위치로 정해준다.

    NEXT_BUBBLE = create_bubble()
    NEXT_BUBBLE.set_rect((screen_width // 4 , 688))      #버블의 위치를 다음에 쏠 위치로 정해준다.

    

#버블을 만든다
def create_bubble():
    color = get_random_bubble_color()
    image = get_bubble_image(color)
    return Bubble(image,color) #우선 버블의 위치는 정하지 않고, 객체만 생성
    

#랜덤으로 버블 색깔을 정한다
def get_random_bubble_color():
    colors = [] #색깔의 후보가 될 수 있는 것들
    for row in map:
        for col in row:
            # 비어있거나 || .이거나 || / 아닌 경우 col을 하나 추가한다
            if col not in colors and col not in [".","/"]:
                colors.append(col)
    return random.choice(colors)            

def process_collision():
    global CURR_BUBBLE, FIRE
    #충돌한 버블
    hit_bubble = pygame.sprite.spritecollideany(CURR_BUBBLE, bubble_group, pygame.sprite.collide_mask)
     #버블끼리 충돌 or 천장에 부딪힌경우
    if hit_bubble or CURR_BUBBLE.rect.top <= 0:
        #(* ㅁㅁ) 적으면 튜플형태를 (ㅇ,ㅇ)형태로 분리해서 전달
        row_index, col_idx = get_map_index(*CURR_BUBBLE.rect.center)
        place_bubble(CURR_BUBBLE, row_index, col_idx) 
        CURR_BUBBLE = None
        FIRE = False


def get_map_index(x, y):
    row_idx = y // CELL_SIZE
    col_idx = x // CELL_SIZE
    if row_idx %2 ==1:
        col_idx = (x - (CELL_SIZE //2)) // CELL_SIZE
        if col_idx < 0 : col_idx = 0
        if col_idx > MAP_ROW_COUNT - 2 : col_idx = MAP_ROW_COUNT - 2    
    return row_idx, col_idx

#버블을 특정 위치에 붙인다(충돌시 붙이기 위해서)
def place_bubble(bubble, row_idx, col_idx):
    map[row_idx][col_idx] = bubble.color
    position = get_bubble_position(row_idx, col_idx)
    bubble.set_rect(position)
    bubble_group.add(bubble)

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

#발사대 이미지 불러오기
launchPad_image = pygame.image.load(os.path.join(current_path, "launchPad.png"))
launchPad = LaunchPad(launchPad_image,( screen_width //2, 624),90)                               #발사대 위치 세팅

#게임 관련 변수
CELL_SIZE =     56
BUBBLE_WIDTH =  56
BUBBLE_HEIGHT = 62
MAP_ROW_COUNT = 11        #맵의 행 갯수
MAP_COLUMN_COUNT=8        #맵의 열 갯수

CURR_BUBBLE = None      #이번에 쏠 버블
NEXT_BUBBLE = None      #다음에 쏠 버블
FIRE        = False     #발사중인지 여부

#발사대 관련 변수
TO_ANGLE_LEFT     = 0   # 좌로 움직인 각도의 정보
TO_ANGLE_RIGHT    = 0   # 우로 움직인 각도의 정보
ANGLE_SPEED = 1.5       # 움직일 속도(1.5도씩 움직이게 됨)


map = [] #맵
bubble_group = pygame.sprite.Group()  # 버블을 생성해서 관리할 공간
setup()

running = True
while running:
    clock.tick(60) #FPS를 60으로 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False                                     #반복문 탈출하도록 running변수 변경

        # 키보드의 아래화살표가 눌려졌을때 이벤트 처리
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                TO_ANGLE_LEFT += ANGLE_SPEED

            elif event.key == pygame.K_RIGHT:    
                TO_ANGLE_RIGHT -= ANGLE_SPEED

            #스페이스바가 눌려지고 && CURR_BUBBLE 만들어져 있으며 && 발사중인상태가 아닐때 <발사!>
            elif event.key == pygame.K_SPACE: 
                if CURR_BUBBLE and not FIRE :
                    FIRE = True
                    CURR_BUBBLE.set_angle(launchPad.angle)            

    # 키보드의 아래화살표가 떼어졌을때 이벤트 처리
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                TO_ANGLE_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                TO_ANGLE_RIGHT = 0


    if not CURR_BUBBLE:
        prepare_bubbles()

    if FIRE:
        #충돌처리
        process_collision()

    screen.blit(background, (0,0))                              #(0,0) background 표시하기     
    bubble_group.draw(screen)                                   #버블 표시하기
    launchPad.rotate(TO_ANGLE_LEFT+TO_ANGLE_RIGHT)              #발사대 이미지 각도 표현하기
    launchPad.draw(screen)                                      #발사대 표시하기
    
    #발사할 버블을 표시하기
    if CURR_BUBBLE:                                             
        #발사중이라면
        if FIRE:                
            CURR_BUBBLE.move()
        CURR_BUBBLE.draw(screen)

    #다음에 발사할 버블을 표시하기
    if NEXT_BUBBLE:
            NEXT_BUBBLE.draw(screen)        

    pygame.display.update()
     
pygame.quit()