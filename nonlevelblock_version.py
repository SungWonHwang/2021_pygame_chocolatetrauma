import pygame
from pygame.locals import *
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()


#스크린
screen_width = 1045
screen_height = 660
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Chocolate Trauma')

#변수설정
tile_size = 55
main_menu = True
game_over = 0
level=1
score=0
lives = 3
flag = False
last_sound=False


#배경이미지로드
bg_img = pygame.image.load('asset/bg.png')
screen_img = pygame.image.load('asset/screen3.png')
last_img = pygame.image.load('asset/lastscore.png')
love_img = pygame.image.load('asset/hud_heartFull.png')
ice_img = pygame.image.load('asset/ice.png')



#메뉴이미지로드
start_img = pygame.image.load('asset/startbtn.png')
exit_img = pygame.image.load('asset/quitbtn.png')
restart_img = pygame.image.load('asset/restartbtn.png')

#사운드로드
pygame.mixer.music.load('asset/bensound-buddy.mp3')
pygame.mixer.music.play(-1, 0.0, 5000)

jump_fx = pygame.mixer.Sound('asset/jump.wav')
jump_fx.set_volume(2)

hurt_fx = pygame.mixer.Sound('asset/hurt.wav')
hurt_fx.set_volume(2)

heart_fx = pygame.mixer.Sound('asset/winningCoin.wav')
heart_fx.set_volume(2)

last_fx = pygame.mixer.Sound('asset/levelcompleted.wav')
last_fx.set_volume(2)



#텍스트설정
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)
last_score = pygame.font.SysFont('Bauhaus 93', 100)
white = (200, 255, 255)
color1 = (255, 255, 200)
black = (0, 0, 0)

######################################################################################
######################################################################################

#텍스트
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))



    
#버튼 클래스
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        #draw button
        screen.blit(self.image, self.rect)

        return action



    
#플레이어 클래스
class Player():
    def __init__(self, x, y):
        self.reset(x,y)

    def update(self, game_over):
        dx = 0
        dy = 0


        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.jumped == False and '''self.in_air == False''':
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_UP] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
            if key[pygame.K_RIGHT]:
                dx += 5

            #중력
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #충돌반응
            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
   

            #플레이어죽음
            if pygame.sprite.spritecollide(self, slime_group, False):
                    game_over = -1
            if pygame.sprite.spritecollide(self, slime2_group, False):
                    game_over = -1
            if pygame.sprite.spritecollide(self, slime0_group, False):
                    game_over = -1
            if pygame.sprite.spritecollide(self, slime3_group, False):
                    game_over = -1

            if pygame.sprite.spritecollide(self, sword_group, False):
                    game_over = -1
                    
            if pygame.sprite.spritecollide(self, fire_group, False):
                    game_over = -1
                    


            #플레이어탈출
            if pygame.sprite.spritecollide(self, exit_group, False):
                    game_over = 1
            if pygame.sprite.spritecollide(self, exit_group2, False) :
                    game_over = 2
            if pygame.sprite.spritecollide(self, exit_group3, False):
                    game_over = 3

            #플레이어아이템

                    
                    

            #스크린 사방으로 막음
            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
                dy = 0
            if self.rect.top < 0:
                self.rect.top = 0
                dy = 0

            if self.rect.left < 0:
                self.rect.left = 0
                dx = 0

            if self.rect.right > screen_width:
                self.rect.right = screen_width
                dx = 0

        #게임오버시 귀신되는거
        elif game_over == -1:
            #self.image = self.dead_image
            if self.rect.y < screen_height:
                self.rect.y += 5

 
        #플레이어블릿
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over
    
    def reset(self, x, y):
        img = pygame.image.load('asset/player.png')
        self.dead_image = pygame.image.load('asset/ghost_dead.png')
        self.image = pygame.transform.scale(img, (48, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.in_air = True
        


#맵클래스   
class World():
    def  __init__(self, data):
        self.tile_list = []

        #로드 이미지
        cake_img = pygame.image.load('asset/cakeMid.png')
        cakeCenter_img = pygame.image.load('asset/cakeCenter.png')
        cakeCliffRight_img = pygame.image.load('asset/cakeCliffRight.png')
        cakeCliffLeft_img = pygame.image.load('asset/cakeCliffLeft.png')
        
        tundra_img = pygame.image.load('asset/iceWaterDeepStars.png')
        tundraCenter_img = pygame.image.load('asset/iceWaterDeepStarsAlt.png')
        tundraCliffRight_img = pygame.image.load('asset/iceWaterDeepAlt.png')
        tundraCliffLeft_img = pygame.image.load('asset/iceWaterDeepAlt.png')

        houseDark_img = pygame.image.load('asset/houseDarkTopMid.png')
        houseDarkCenter_img = pygame.image.load('asset/houseDarkAlt.png')
        houseDarkCliffRight_img = pygame.image.load('asset/houseDarkTopRight.png')
        houseDarkCliffLeft_img = pygame.image.load('asset/houseDarkTopLeft.png')




        

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1: #메인벽돌
                    img = pygame.transform.scale(cake_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2: #그냥갈색벽돌
                    img = pygame.transform.scale(cakeCenter_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3: #절벽오른쪽벽돌
                    img = pygame.transform.scale(cakeCliffRight_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4: #절벽왼쪽벽돌
                    img = pygame.transform.scale(cakeCliffLeft_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
#####################################################
                if tile == 21: #메인벽돌
                    img = pygame.transform.scale(tundra_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 22: #그냥갈색벽돌
                    img = pygame.transform.scale(tundraCenter_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 23: #절벽오른쪽벽돌
                    img = pygame.transform.scale(tundraCliffRight_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 24: #절벽왼쪽벽돌
                    img = pygame.transform.scale(tundraCliffLeft_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
#####################################################
                if tile == 31: #메인벽돌
                    img = pygame.transform.scale(houseDark_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 32: #그냥갈색벽돌
                    img = pygame.transform.scale(houseDarkCenter_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 33: #절벽오른쪽벽돌
                    img = pygame.transform.scale(houseDarkCliffRight_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 34: #절벽왼쪽벽돌
                    img = pygame.transform.scale(houseDarkCliffLeft_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

#####################################################

                if tile == 61: #창
                    window = Window(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    window_group.add(window)
                    
                if tile == 62: #펜스
                    fence = Fence(col_count * tile_size, row_count * tile_size+(tile_size // 2))
                    fence_group.add(fence)

                if tile == 63: #줄
                    line = Line1(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    line_group.add(line)


                if tile == 64: #바닐라
                    green = Green(col_count * tile_size, row_count * tile_size)
                    green_group.add(green)
                    
                if tile == 65: #핑크지팡이
                    pink = Pink(col_count * tile_size+30, row_count * tile_size+28)
                    pink_group.add(pink)

                if tile == 66: #초록지팡이
                    pinksand = Pinksand(col_count * tile_size+30, row_count * tile_size+28)
                    pinksand_group.add(pinksand)




#####################################################
                if tile == 5: #슬라임2
                    slime2 = Enemy2(col_count * tile_size, row_count * tile_size+26)
                    slime2_group.add(slime2)

                if tile == 6: #장애물-FIRE
                    fire = Fire(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    fire_group.add(fire)

                    
                if tile == 7: #장애물-칼
                    sword = Sword(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    sword_group.add(sword)

                    
                if tile == 8: #레벨1출구
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                    
                if tile == 9: #슬라임
                    slime = Enemy(col_count * tile_size, row_count * tile_size+26)
                    slime_group.add(slime)
                    
                if tile == 77: #슬라임0
                    slime0 = Enemy0(col_count * tile_size, row_count * tile_size+26)
                    slime0_group.add(slime0)
                if tile == 78: #슬라임3 위아래스피너
                    slime3 = Enemy3(col_count * tile_size, row_count * tile_size+26)
                    slime3_group.add(slime3)
                    
                if tile == 10: #레벨2출구
                    exit2 = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group2.add(exit2)
                    
                if tile == 11: #레벨3출구
                    exit3 = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group3.add(exit3)
                    
                if tile == 12: #얼음아이템
                    heart = Heart(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    heart_group.add(heart)

                if tile == 13: #목숨아이템
                    heartplus = HeartPlus(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    heartplus_group.add(heartplus)

                    
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)



#적클래스 -> 업데이트 및 움직임 주므로 SPRITE사용
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('asset/slimeWalk1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0


    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
            
class Enemy0(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('asset/slimeWalk1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = -1
        self.move_counter = 0


    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Enemy2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('asset/spinnerHalf.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0


    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Enemy3(pygame.sprite.Sprite): #위아래스피너
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('asset/spinner.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0


    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 80:
            self.move_direction *= -1
            self.move_counter *= -1

            
#장애물 클래스
class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('asset/swordSilver.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('asset/lava_2.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        
#아이템 클래스
class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('asset/iceBlockAlt.png')
        self.image = pygame.transform.scale(img, (tile_size//2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class HeartPlus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('asset/cherry.png')
        self.image = pygame.transform.scale(img, (tile_size//3*2, tile_size//3*2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        
#꾸미기 클래스

class Window(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('asset/windowCheckered.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Line1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('asset/metalPlatformWire.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)        
        
class Fence(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('asset/metalFence.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
class Pink(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('asset/canePinkSmall.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Pinksand(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('asset/caneGreenSmall.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)        
        
class Green(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('asset/creamVanilla.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        
#출구클래스
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('asset/doorLock.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


######################################################################################
######################################################################################

      
#레벨1
world_data_1 = [
[ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1], 
[ 2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2], 
[ 2,  8,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 64,  2], 
[ 2,  1,  1,  1,  1,  0,  0,  0,  0,  0, 65,  0,  0,  0,  0,  0,  0,  4,  2], 
[ 2,  2,  2,  2,  2,  0,  0,  0,  0,  0,  4,  3,  7,  0,  0,  0,  0,  0,  2], 
[ 2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4,  3,  0,  0,  0,  0,  2], 
[ 2,  0,  0,  0,  0, 64,  0,  0,  0,  0,  0,  0,  9,  0,  0,  9,  0, 12,  2], 
[ 2, 12,  0,  0,  7,  4,  3,  0,  0,  0,  0,  4,  1,  1,  1,  1,  1,  1,  2], 
[ 2,  1,  1,  1,  3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2], 
[ 2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2], 
[ 2,  0,  0,  0,  0,  0, 12,  0,  0,  0,  0,  0,  0, 65,  0, 65,  0, 13,  2],  
[ 2,  1,  1,  1,  1,  1,  1,  1,  1,  7,  7,  1,  1,  1,  1,  1,  1,  1,  2]
]


#레벨2
world_data_2 = [
[21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21], 
[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0], 
[ 0,  0, 24, 23,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 10], 
[ 0,  0,  0,  0,  0,  0,  0,  9,  0,  0,  0,  0, 77,  0,  0,  0,  0, 21, 21], 
[ 0,  0,  0,  0,  0,  0, 21, 21, 21,  0, 12, 21, 21, 21,  0,  0,  0,  0,  0], 
[ 0, 12,  0,  0, 21, 21, 22, 22, 22, 21, 21, 22, 22, 22, 21, 21, 21, 21, 21], 
[21, 21,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 22], 
[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 13,  0,  0,  0, 22], 
[ 0,  0,  0, 23, 24,  0,  0,  0, 23, 24,  0,  0,  0, 23, 24,  0,  0,  0, 22], 
[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 22], 
[62, 62, 62,  0,  0,  0, 66,  0,  0,  0,  0, 66,  0,  0,  0,  0,  0, 12, 22],  
[21, 21, 21,  6,  6, 21, 21, 21,  6,  6, 21, 21, 21,  6,  6, 21, 21, 21, 22]
]


#레벨3
world_data_3 = [
[31, 31, 31, 31, 31, 31, 31, 31, 31,  0,  0,  0,  0, 34, 31, 31, 31, 31, 31], 
[32,  0,  0,  0,  0,  0,  0,  0, 32, 11,  0,  0,  0,  0,  0,  0,  0,  0, 32], 
[32,  0, 63, 63, 63, 63, 63, 63, 32, 31, 33,  0,  0,  0, 63, 63, 63, 63, 32], 
[32, 12,  0,  0, 78,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 12, 32], 
[32, 31, 31, 33,  0,  0,  0, 13,  0,  0,  0,  0,  0,  0,  0, 34, 31, 31, 32], 
[ 0,  0,  0,  0,  0,  7, 31, 31, 31, 31,  7, 31, 31,  0,  0,  0,  0,  0, 32], 
[ 0,  0,  0,  0,  0, 34, 32, 32, 32, 32, 31, 32, 32,  0,  0,  0,  0,  0, 32], 
[ 0, 12,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 61,  0, 32], 
[31, 33,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 31, 32], 
[ 0,  0,  0,  0,  0,  0,  0, 61,  0, 61,  0, 61,  0,  0,  0,  0, 31, 32, 32], 
[62, 62, 62, 62, 62, 62, 62, 62,  0,  0,  0,  0,  5,  0,  0, 31, 32, 32, 32],  
[31, 31, 31, 31, 31, 31, 31, 31,  7,  7,  7, 31, 31, 31, 31, 32, 32, 32, 32]
]



#여러가지
player = Player(100, screen_height - 130)
slime_group = pygame.sprite.Group()
slime2_group = pygame.sprite.Group()
slime3_group = pygame.sprite.Group()
slime0_group = pygame.sprite.Group()
sword_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()
heart_group = pygame.sprite.Group()
heartplus_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
exit_group2 = pygame.sprite.Group()
exit_group3 = pygame.sprite.Group()
#
line_group = pygame.sprite.Group()
fence_group = pygame.sprite.Group()
window_group = pygame.sprite.Group()
pink_group = pygame.sprite.Group()
pinksand_group = pygame.sprite.Group()
green_group = pygame.sprite.Group()



score_heart = Heart(tile_size // 2, tile_size // 2)
heart_group.add(score_heart)

world = World(world_data_1)

#버튼
restart_button = Button(screen_width // 2-100, screen_height // 2-60, restart_img)
start_button = Button(screen_width // 2+200, screen_height // 2+110, start_img)
exit_button = Button(screen_width // 2+200, screen_height // 2+210, exit_img)
exit_button2 = Button(screen_width // 2-100, screen_height // 2+30, exit_img)



######################################################################################
######################################################################################

#게임동작
run = True
while run:

    screen.blit(bg_img, (0,0))

    #메인메뉴실행
    if main_menu == True:
        screen.blit(screen_img, (0,0))
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()

        if game_over == 0:
            screen.blit(love_img, (260,13))
            screen.blit(ice_img, (13,10))

            #점수체크
            if pygame.sprite.spritecollide(player, heart_group, True):
                heart_fx.play()
                score += 10
            if pygame.sprite.spritecollide(player, heartplus_group, True):
                heart_fx.play()
                lives += 1
            draw_text('ICE SCORE: ' + str(score), font_score, white, tile_size , 10)
            draw_text('LIFE: ' + str(lives), font_score, color1, tile_size + 250, 10)
            #slime_group.update()
        if game_over == -1:
            if lives > 0 and flag == False :
                lives -= 1
                hurt_fx.play()
                print(lives)
                flag = True

            #draw_text('GAME OVER', font, blue, (screen_width // 2) - 170, screen_height // 2-150)
            if lives == 0:
                if restart_button.draw():
                    lives = 3
                    player.reset(100, screen_height - 130)
                    flag = False
                    game_over = 0
                    score=0
                    slime_group.empty()
                    slime0_group.empty()
                    slime2_group.empty()
                    slime3_group.empty()
                    sword_group.empty()
                    fire_group.empty()
                    exit_group.empty()
                    exit_group2.empty()
                    exit_group3.empty()
                    heart_group.empty()
                    line_group.empty()
                    fence_group.empty()
                    window_group.empty()
                    pink_group.empty()
                    pinksand_group.empty()
                    green_group.empty()
                    heartplus_group.empty()
                    world = World(world_data_1)
                if exit_button2.draw():
                    run = False
            else:
                player.reset(100, screen_height - 130)
                flag = False
                game_over = 0

        #레벨관련        
        if game_over == 1:
            #world_data_1 = []
            slime_group.empty()
            slime2_group.empty()
            slime0_group.empty()
            slime3_group.empty()
            sword_group.empty()
            exit_group.empty()
            fire_group.empty()
            heart_group.empty()
            
            line_group.empty()
            fence_group.empty()
            window_group.empty()
            pink_group.empty()
            pinksand_group.empty()
            green_group.empty()

            
            heartplus_group.empty()
            world = World(world_data_2)
            player.reset(100, screen_height - 130)
            game_over = 0
            
        if game_over == 2:
            #world_data_2 = []
            slime_group.empty()
            slime2_group.empty()
            slime0_group.empty()
            slime3_group.empty()
            sword_group.empty()
            exit_group2.empty()
            fire_group.empty()
            heart_group.empty()
                        
            line_group.empty()
            fence_group.empty()
            window_group.empty()
            pink_group.empty()
            pinksand_group.empty()
            green_group.empty()

            heartplus_group.empty()
            world = World(world_data_3)
            player.reset(100, screen_height - 130)
            game_over = 0
            
        if game_over == 3:
            slime_group.empty()
            slime2_group.empty()
            slime0_group.empty()
            slime3_group.empty()
            sword_group.empty()
            exit_group3.empty()
            fire_group.empty()
            heart_group.empty()
            
            line_group.empty()
            fence_group.empty()
            window_group.empty()
            pink_group.empty()
            pinksand_group.empty()
            green_group.empty()
            
            heartplus_group.empty()
            screen.blit(last_img, (0,0))
            player.reset(-100, screen_height + 130)
            draw_text(str(score+lives*15), last_score, black, (screen_width // 2), screen_height // 2+50)
            #pygame.mixer.music.pause()
            #last_fx.play(1)
            
        slime_group.draw(screen)
        slime2_group.draw(screen)
        slime0_group.draw(screen)
        slime3_group.draw(screen)
        sword_group.draw(screen)
        fire_group.draw(screen)
        heart_group.draw(screen)
        heartplus_group.draw(screen)
        exit_group.draw(screen)
        exit_group2.draw(screen)
        exit_group3.draw(screen)
        #
        line_group.draw(screen)
        fence_group.draw(screen)
        window_group.draw(screen)
        green_group.draw(screen)
        pink_group.draw(screen)
        pinksand_group.draw(screen)


        slime_group.update()
        slime0_group.update()
        slime2_group.update()
        slime3_group.update()
        game_over = player.update(game_over)


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



    pygame.display.update()


pygame.quit()
    
