import pygame
import os
import random
import csv
import button
import pyautogui
import webbrowser
import time
from animations import load_animation
import itertools
from ai import ai

pygame.init()

FULL_SCREEN_WIDTH = 1080
FULL_SCREEN_HEIGHT = 1920
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
programIcon = pygame.image.load('img/favicon/favicon-main.png')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))   #创建了游戏窗口，并设置了窗口的标题和图标。在循环中，处理了事件、更新游戏状态、渲染游戏界面等。
pygame.display.set_icon(programIcon)
pygame.display.set_caption('ombioo')
pygame.mouse.set_visible(1)

# FPS
clock = pygame.time.Clock()
FPS = 85
PING = [4, 5]


# VAR
GRAVITY = 0.50
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 22
MAX_LEVELS = 6
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False


# PLAYER VAR
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False
molotov = False
molotov_thrown = False


# HALLOWEEN UPDATE IMAGES万圣节更新图片 图片加载：这些图像包括按钮、背景、角色等，用于游戏中的显示和交互。
cat_halloween = pygame.image.load('img/Halloween_update/cat_halloween_update.png').convert_alpha()
pumpkin_halloween = pygame.image.load('img/Halloween_update/pumpkin_halloween_update.png').convert_alpha()
bat_halloween = pygame.image.load('img/Halloween_update/halloween_halloween_update.png').convert_alpha()
menu_halloween = pygame.image.load('img/Halloween_update/menuzombioo_halloween_update.png').convert_alpha()
happy_halloween = pygame.image.load('img/Halloween_update/happy_halloween_update.png').convert_alpha()
border_halloween1 = pygame.image.load('img/Halloween_update/border_lore_halloween1.png').convert_alpha()
border_halloween2 = pygame.image.load('img/Halloween_update/border_lore_halloween2.png').convert_alpha()


# IMAGES
start_img = pygame.image.load('img/btn/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/btn/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/btn/restart_btn.png').convert_alpha()
settings_img = pygame.image.load('img/btn/cog.png').convert_alpha()
jk_img = pygame.image.load('img/btn/jk.png').convert_alpha()
menubg = pygame.image.load('img/background/menuzombioo.png').convert_alpha()
speaker_img = pygame.image.load('img/btn/speaker.png').convert_alpha()
speaker_muted_img = pygame.image.load('img/btn/speaker_muted.png').convert_alpha()
info_img = pygame.image.load('img/btn/info_button.png').convert_alpha()
angel_statue = pygame.image.load('img/tile/20.png').convert_alpha()

#KEYBOARD
Wkey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/W_Key_Light.png').convert_alpha()
Akey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/A_Key_Light.png').convert_alpha()
Dkey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/D_Key_Light.png').convert_alpha()
Qkey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/Q_Key_Light.png').convert_alpha()
ESCkey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/Esc_Key_Light.png').convert_alpha()
SPkey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/Spacelarge_Key_Light.png').convert_alpha()
Mkey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/M_Key_Light.png').convert_alpha()
Ukey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/U_Key_Light.png').convert_alpha()
Fkey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/F_Key_Light.png').convert_alpha()
F5key = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/F5_Key_Light.png').convert_alpha()
F4key = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/F4_Key_Light.png').convert_alpha()

# BACKGROUND IMAGES
pine1_img = pygame.image.load(
    'img/background/2_background_NEST/2_game_background.png').convert_alpha()
pine2_img = pygame.image.load(
    'img/background/2_background_NEST/2_game_background.png').convert_alpha()
mountain_img = pygame.image.load('img/background/2_background_NEST/2_game_background.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()
headhp = pygame.image.load('img/player/headHP.png').convert_alpha()
headdeadhp = pygame.image.load('img/player/headdeadHP.png').convert_alpha()
border_settings_img = pygame.image.load('img/background/border_settings.png').convert_alpha()
border_lore_img = pygame.image.load('img/background/border_lore.png').convert_alpha()



# TILES ETC
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/Tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

bullet_img = pygame.image.load('img/icons/ammo.png').convert_alpha()
bullet_zombie = pygame.image.load('img/icons/bulletzombie.png').convert_alpha

grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
molotov_img = pygame.image.load('img/icons/molotov.png').convert_alpha() 

health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
molotov_box_img = pygame.image.load('img/icons/molotov_box.png').convert_alpha()
item_boxes = {
    'Health'	: health_box_img,
    'Ammo'		: ammo_box_img,
    'Grenade'	: grenade_box_img,
    'Molotov'   :molotov_box_img
}

# COLORS颜色定义：定义了一些颜色常量，用于游戏中的绘制和填充
BG = (81, 6, 13)
RED = (176, 8, 12)
WHITE = (255, 255, 255)
GREEN = (26, 110, 15)
BLACK = (0, 0, 0)
CRIMSON = (191, 46, 72)

#MUSIC加载音乐文件
menumusic = pygame.mixer.music.load('audio/THEME.wav')
pygame.mixer.music.play(0)  #播放音乐
SHOOT_SOUND = pygame.mixer.Sound('audio/shot.mp3')   #加载其他音效文件，并设置音量。
SHOOT_SOUND.set_volume(0.6)

RELOAD = pygame.mixer.Sound('audio/Reloading.mp3')
RELOAD.set_volume(1)

GRENADESOUND = pygame.mixer.Sound('audio/grenade.mp3')
GRENADESOUND.set_volume(1)

MOLOTOVSOUND = pygame.mixer.Sound('audio/molotov.wav')
MOLOTOVSOUND.set_volume(1)

MOLOTOVBR = pygame.mixer.Sound('audio/molotovbr.wav')
MOLOTOVBR.set_volume(3)

PICK = pygame.mixer.Sound('audio/grenadepick.mp3')
PICK.set_volume(2)

PICKHEALTH = pygame.mixer.Sound('audio/pills.mp3')
PICKHEALTH.set_volume(2)

GRUNTING = pygame.mixer.Sound('audio/Grunting.mp3')
GRUNTING.set_volume(2)

ZOMBIEATTACK = pygame.mixer.Sound('audio/zombieattack.mp3')
ZOMBIEATTACK.set_volume(20)

MENUSELECT = pygame.mixer.Sound('audio/menuselect.mp3')
MENUSELECT.set_volume(9)

NEXTLEVEL = pygame.mixer.Sound('audio/nextlevel.mp3')
NEXTLEVEL.set_volume(9)

JUMP = pygame.mixer.Sound('audio/jump.mp3')
JUMP.set_volume(2)

GAMEOVER = pygame.mixer.Sound('audio/gameover.wav')
GAMEOVER.set_volume(2)

SCREENSHOT = pygame.mixer.Sound('audio/takingphoto.wav')
SCREENSHOT.set_volume(5)

# FONT字体：通过加载字体文件（.ttf）创建了几个字体对象，用于在游戏界面上显示不同的文本
font = pygame.font.Font("font/Futurot.ttf", 21)
ver = pygame.font.Font("font/Futurot.ttf", 10)
zombiootitle = pygame.font.Font("font/Futurot.ttf", 130)
BTNtext = pygame.font.Font("font/Futurot.ttf", 50)
YOUDIED = pygame.font.Font("font/Futurot.ttf", 110)
JanKupczyk = pygame.font.Font("font/Futurot.ttf", 13)
LORE = pygame.font.Font("font/Futurot.ttf", 14)
LOREsmall = pygame.font.Font("font/Futurot.ttf", 8)

pausetimerevent = pygame.USEREVENT + 1
paused = False

#这个函数用于在屏幕上绘制文本。它使用提供的字体、文本颜色、坐标参数来渲染文本图像，并将图像绘制到屏幕上。
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#这个函数用于绘制背景图像。它首先填充屏幕背景颜色，然后根据背景滚动值（bg_scroll）绘制天空、山脉和树木的图像。
def draw_sky():
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))

def draw_mountains():
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6,
                                   SCREEN_HEIGHT - mountain_img.get_height() - 300))

def draw_pine1():
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7,
                                SCREEN_HEIGHT - pine1_img.get_height() - 150))

def draw_pine2():
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8,
                                SCREEN_HEIGHT - pine2_img.get_height()))

def draw_bg():
    screen.fill(BG)
    draw_sky()
    draw_mountains()
    draw_pine1()
    draw_pine2()


# LEVEL RESET这个函数用于重置关卡。它清空了一些游戏元素的组（如敌人、子弹、道具等），并返回一个二维数组data。这个数组用于存储关卡地图的布局。
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    zombiebullet_group.empty()
    grenade_group.empty()
    molotov_group.empty()
    explosion_group.empty()
    moloexplosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    # TILE2
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data

# 定义常量
MAX_HEALTH = 130
#继承自pygame.sprite.Sprite。它表示游戏中的士兵角色，具有移动、射击、动画更新等功能。
class Soldier(pygame.sprite.Sprite):
    #初始化士兵对象的属性。其中包括角色类型（char_type），位置（x和y），缩放比例（scale），速度（speed），弹药数量（ammo），手雷数量（grenades）和燃烧瓶数量（molotovs）等
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades, molotovs):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.molotovs = molotovs
        self.health = MAX_HEALTH  # 使用常量变量
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # AI VAR
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        # IDLE RUN JUMP DEATH FLIP空转跳跃死亡翻转
        # self.animation_list = self.load_animation(char_type, scale)
        self.animation_list = load_animation(char_type, ['Idle', 'Run', 'Jump', 'Death'], scale)  # 模块化加载动画

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()


    #更新士兵的动画和状态。在这个方法中，会调用update_animation()和check_alive()方法。
    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    #处理士兵的移动。根据传入的moving_left和moving_right参数决定士兵的水平移动方向。方法中还包括处理士兵跳跃和重力的逻辑，以及与障碍物的碰撞检测。
    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        # Movment variables
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # JUMP
        if self.jump == True and self.in_air == False:
            JUMP.play()
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # GRAV
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # self.rect.x += dx
        # self.rect.y += dy

        # Scroll background
        screen_scroll, level_complete = self.handle_scroll(dx,dy)
        return screen_scroll, level_complete

    def handle_scroll(self, dx, dy):
        screen_scroll = 0
        level_complete = False

        # COLLISION
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True
            NEXTLEVEL.play()

        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        self.rect.x += dx
        self.rect.y += dy

        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                    or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete


    #处理士兵射击行为。根据射击冷却时间和弹药数量，创建子弹对象并添加到bullet_group中，同时播放射击音效和减少弹药数量
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.60 *
                                                 self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            SHOOT_SOUND.play()
            # AMMO
            self.ammo -= 1

    def ai(self):
        ai(self,player,TILE_SIZE,screen_scroll)

    #更新士兵的动画。根据时间和动画切换间隔，切换士兵当前动作的帧索引。
    def update_animation(self):
        ANIMATION_COOLDOWN = 90
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    #更新士兵的当前动作。当传入的新动作与当前动作不同时，更新动作、帧索引和计时器。
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    #检查士兵是否存活。当士兵的生命值小于等于0时，将其设为死亡状态，停止移动并更新动作。
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    #绘制士兵在屏幕上的图像。根据士兵的水平朝向，翻转图像后绘制在屏幕上。
    def draw(self):
        screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)

#负责处理关卡数据并根据瓦片值创建游戏对象。它处理障碍物、装饰物、水、出口和物品箱。
class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(
                            img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:  # create player
                        player = Soldier('player', x * TILE_SIZE,
                                         y * TILE_SIZE, 1.65, 5, 20, 5, 5)
                        health_bar = HealthBar(
                            10, 10, player.health, player.health)
                    elif tile == 16:  # create enemies
                        enemy = Soldier('enemy', x * TILE_SIZE,
                                        y * TILE_SIZE, 1.65, 2, 20, 0, 0)
                        enemy_group.add(enemy)
                    elif tile == 17:  # create ammo box
                        item_box = ItemBox(
                            'Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18:  # create grenade box
                        item_box = ItemBox(
                            'Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:  # create health box
                        item_box = ItemBox(
                            'Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:  # create exit
                        exit_obj = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit_obj)

        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

#装饰、水、出口和 ItemBox 类是 pygame.sprite.Sprite 的子类，代表游戏世界中不同类型的对象。它们有更新其位置和与其他游戏对象交互的方法。
class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Health':
                player.health += 20
                PICKHEALTH.play()
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 3
                RELOAD.play()
            elif self.item_type == 'Grenade':
                player.grenades += 1
                PICK.play()
            elif self.item_type == 'Molotov':
                player.molotovs += 1
                PICK.play()
            self.kill()

#HealthBar类管理玩家的健康条UI元素。它包括一种在屏幕上绘制健康条的方法。
class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))
        screen.blit(headhp, (-4, 2))
        screen.blit(update_fps(), (1050,5))
        draw_text('FPS', font, WHITE, 1000, 5)
        screen.blit(update_ping(), (1065,30))
        draw_text('MS', font, WHITE, 1005, 30)
        screen.blit(update_ms(), (70, 820))
        draw_text('TIME', font, WHITE, 5, 820)
        draw_text('Current build V2.0 (release.01.11.2021)', ver, WHITE, 5, 853)

#子弹类代表玩家发射的子弹。它朝着一个方向移动，并检查是否与障碍物、敌人和玩家发生碰撞。
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 13
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed) + screen_scroll
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= random.randint(40,99)
                    ZOMBIEATTACK.play()
                    self.kill()
#更新游戏的帧率，并返回一个渲染了帧率的文本对象
def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pygame.Color("white"))
	return fps_text
#更新游戏的毫秒数，并返回一个渲染了毫秒数的文本对象。
def update_ms():
    mss = str(pygame.time.get_ticks()/1000)
    mss_text = font.render(mss, 1, pygame.Color("white"))
    return mss_text
#更新游戏的延迟时间，并返回一个渲染了延迟时间的文本对象。
def update_ping():
    ping = str(int(random.choice(PING)))
    ping_text = font.render(ping, 1, pygame.Color("white"))
    return ping_text
#显示游戏的控制设置，包括各个按键的说明和图像
def settings_show():
        draw_text('CONTROL:', font, WHITE, 73, 385),
        draw_text('JUMP', font, WHITE, 145, 415),
        screen.blit(Wkey, (100, 400)),
        draw_text('LEFT', font, WHITE, 20, 450),
        screen.blit(Dkey, (135, 435)),
        draw_text('RIGHT', font, WHITE, 183, 450),
        screen.blit(Akey, (65, 435)),
        draw_text('SHOOT', font, WHITE, 170, 490),
        screen.blit(SPkey, (85, 460)),
        draw_text('NADE', font, WHITE, 55, 546),
        screen.blit(Qkey, (5, 530)),
        draw_text('MUTE MUSIC', font, WHITE, 55, 586),
        screen.blit(Mkey, (5, 570)),
        draw_text('UNMUTE MUSIC', font, WHITE, 55, 626),
        screen.blit(Ukey, (5, 610)),
        draw_text('FULLSCREEN', font, WHITE, 55, 666),
        screen.blit(Fkey, (5, 650)),
        draw_text('TAKE SCREENSHOT', font, WHITE, 55, 706),
        screen.blit(F5key, (5, 690)),
        draw_text('EXIT', font, WHITE, 55, 746),
        screen.blit(ESCkey, (5, 730))
        screen.blit(border_settings_img, (-139, 349))
        # screen.blit(border_halloween2, (-139, 349)) #halloween_update

#显示静音状态，暂停音乐和设置所有声音效果的音量为0
def speaker_show():
    pygame.mixer.music.pause()
    SHOOT_SOUND.set_volume(0)
    RELOAD.set_volume(0)
    GRENADESOUND.set_volume(0)
    MOLOTOVSOUND.set_volume(0)
    MOLOTOVBR.set_volume(0)
    PICK.set_volume(0)
    PICKHEALTH.set_volume(0)
    GRUNTING.set_volume(0)
    ZOMBIEATTACK.set_volume(0)
    MENUSELECT.set_volume(0)
    NEXTLEVEL.set_volume(0)
    JUMP.set_volume(0)
    GAMEOVER.set_volume(0)
    SCREENSHOT.set_volume(0)
    screen.blit(speaker_muted_img, (70, 795))
#显示游戏的信息和背景故事
def info_show():
        screen.blit(border_lore_img, (646, 200))
        # screen.blit(border_halloween1, (646, 200)) #halloween_update
        draw_text('In ZOMBIOO you have to survive the zombie', LORE, WHITE, 680, 350)
        draw_text('apocalypse, use everything you can find', LORE, WHITE, 680, 370)
        draw_text('from grenades, molotovs, and various', LORE, WHITE, 680, 390)
        draw_text(' ammunition to kill zombies and heal', LORE, WHITE, 680, 410)
        draw_text('  yourself with a first aid kit', LORE, WHITE, 680, 430)
        draw_text('', LORE, WHITE, 680, 450)
        draw_text('', LORE, WHITE, 680, 470)
        screen.blit(angel_statue, (985, 480))
        draw_text('On each level, you must', LORE, WHITE, 680, 490)
        draw_text('collect special statues', LORE, WHITE, 680, 510)
        draw_text(' to finish it', LORE, WHITE, 680, 530)
        draw_text('ANGEL STATUE', LOREsmall, WHITE, 975, 575)
#合并重复方法
def update_movement(self):
    self.vel_y += GRAVITY
    dx = self.direction * self.speed
    dy = self.vel_y

    for tile in world.obstacle_list:
        if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
            self.direction *= -1
            dx = self.direction * self.speed
        if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
            self.speed = 0
            if self.vel_y < 0:
                self.vel_y = 0
                dy = tile[1].bottom - self.rect.top
            # Check height
            elif self.vel_y >= 0:
                self.vel_y = 0
                dy = tile[1].top - self.rect.bottom

    self.rect.x += dx + screen_scroll
    self.rect.y += dy

#表示手雷的类，具有抛出和爆炸的功能
class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 6
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self):
        update_movement(self)
        # GRENADE POS

        # CD GRENADE TIMER
        self.timer -= 0.95
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 1.5)
            explosion_group.add(explosion)
            #DAMAGE
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 3 and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 3:
                    enemy.health -= 1000
                    GRUNTING.play()


#表示燃烧瓶的类，具有抛出和爆炸的功能。
class Molotov(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 99
        self.vel_y = -10
        self.speed = 11
        self.image = molotov_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self):
        update_movement(self)
        # MOLOTOV r


        # CD MOLOTOV TIMER
        self.timer -= 2
        if self.timer <= 0:
            self.kill()
            moloexplosion = MoloExplosion(self.rect.x, self.rect.y, 1.5)
            moloexplosion_group.add(moloexplosion)
            #DAMAGE
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 25
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 4 and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 4:
                    enemy.health -= 55
                    GRUNTING.play()
                    GRUNTING.play()
                    GRUNTING.play()
#表示燃烧瓶爆炸的效果的类，具有动画效果。
class MoloExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        MOLOTOVBR.play()
        for num in range(0, 4):
            img = pygame.image.load(
                f'img/moloexplosion/Molo_{num}.png').convert_alpha()
            img = pygame.transform.scale(
                img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        MOLOTOVSOUND.play()
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.x += screen_scroll

        moloexplosion_speed = 23
        self.counter += 1

        if self.counter >= moloexplosion_speed:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]
#表示手雷爆炸的效果的类，具有动画效果
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 7):
            img = pygame.image.load(
                f'img/explosion/Explosion_{num}.png').convert_alpha()
            img = pygame.transform.scale(
                img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        GRENADESOUND.play()
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.x += screen_scroll

        EXPLOSION_SPEED = 7
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]

#TAKING SCREENSHOT截屏 代码定义了一个名为takescreenshot的函数，用于捕捉游戏屏幕的截图并将其保存为PNG文件
def takescreenshot(screen):
    time_ss = time.asctime(time.localtime(time.time()))
    time_ss = time_ss.replace(" ", "_")
    time_ss = time_ss.replace(":", ".")
    save_file_f = "screenshots/" + time_ss + ".png"
    pygame.image.save(screen, save_file_f)
    print("Taken screenshot: " + save_file_f)

#BTNs它创建了多个按钮对象，包括开始按钮、退出按钮、重新开始按钮、设置按钮、音频按钮、信息按钮和jk按钮。这些按钮会显示在游戏屏幕上。
start_button = button.Button(
    SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 90, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 64,
                            SCREEN_HEIGHT // 2 + 50, exit_img, 1)
exit_button_die = button.Button(SCREEN_WIDTH // 2 - 65,
                            SCREEN_HEIGHT // 2 + 55, exit_img, 1)
restart_button = button.Button(
    SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 50, restart_img, 2)
settings_button = button.Button(SCREEN_WIDTH // 1 - 1050, SCREEN_HEIGHT // 1 - 70, settings_img, 1)
speaker = button.Button(SCREEN_WIDTH // 1 - 1010, SCREEN_HEIGHT // 1 - 70, speaker_img, 1)
speaker_muted = button.Button(SCREEN_WIDTH // 1 - 1010, SCREEN_HEIGHT // 1 - 70, speaker_muted_img, 1)
info_button = button.Button(SCREEN_WIDTH // 1 - 975, SCREEN_HEIGHT // 1 - 72, info_img, 1)
jk_button = button.Button(SCREEN_WIDTH // 1 - 180, SCREEN_HEIGHT // 1 - 20, jk_img, 1)

# SPRITES
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
zombiebullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
molotov_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
moloexplosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#代码从CSV文件中加载关卡数据，并根据关卡数据创建游戏世界
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# load in level data and create world
def load_world_data(level):
    with open(f'level/level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)
    world = World()
    player, health_bar1 = world.process_data(world_data)
    return world, player, health_bar1

world, player, health_bar = load_world_data(level)

#它将初始游戏状态设置为"start_menu"，并初始化了一些变量。
game_state = "start_menu"
speaker_sp = "speaker"
run = True
#在游戏循环中，代码检查start_game是否为False。如果是，代码显示主菜单，其中包括开始游戏、退出游戏、访问设置和切换音频的按钮。还包括一个按钮，点击后会打开作者的GitHub页面链接。


while run:

    clock.tick(FPS)

    if start_game == False:
        # MENU
        screen.blit(menubg, (0, 0)) #screen.blit(menu_halloween, (0, 0)) #halloween_update
        draw_text('ZOMBIOO', zombiootitle, WHITE, 180, 125)
        draw_text('©2021 Jan Kupczyk', JanKupczyk, WHITE, 905, 845)
        draw_text('Current build V2.0 (released.01.11.2021)', ver, WHITE, 5, 845)
        # screen.blit(happy_halloween, (385, 80))   #halloween_update
        # screen.blit(cat_halloween, (783, 605))    #halloween_update
        # screen.blit(pumpkin_halloween, (175, -49))    #halloween_update
        # screen.blit(pumpkin_halloween, (550, -49))    #halloween_update
        # screen.blit(pumpkin_halloween, (668, -49))   #halloween_update
        # BTNS MENU
        if start_button.draw(screen):
            start_game = True
            MENUSELECT.play()
            pygame.mixer.music.stop()
        if exit_button.draw(screen):
            MENUSELECT.play()
            run = False
            pygame.display.update()
        if settings_button.draw(screen):
            MENUSELECT.play()
            game_state = "settings"
        elif game_state == "settings":
                settings_show()
                info_show()
        if jk_button.draw(screen):
            MENUSELECT.play()
            webbrowser.open('https://github.com/jankupczyk')
        if speaker.draw(screen):
            MENUSELECT.play()
            speaker_sp = "speaker_menu"
        elif speaker_sp == "speaker_menu":
            MENUSELECT.play()
            speaker_show()
        if info_button.draw(screen):
            MENUSELECT.play()
            webbrowser.open('https://github.com/jankupczyk/Zombioo/stargazers')
            webbrowser.open('https://jankupczyk.github.io/Zombioo/')
    else:   #如果start_game变量为True，代码进入游戏部分，并在屏幕上显示游戏世界、玩家生命值条、弹药数量、手榴弹数量和汽油弹数量。
        draw_bg()
        world.draw()
        health_bar.draw(player.health)
        draw_text('HEALTH', font, WHITE, 46, 12)
        draw_text('AMMO: ', font, WHITE, 10, 35)
        for x in range(player.ammo):
            screen.blit(bullet_img, (90 + (x * 10), 40))
        draw_text('GRENADES: ', font, WHITE, 10, 60)
        for x in range(player.grenades):
            screen.blit(grenade_img, (135 + (x * 15), 61))
        draw_text('MOLOTOVS: ', font, WHITE, 10, 85)
        for x in range(player.molotovs):
            screen.blit(molotov_img, (140 + (x * 15), 75))
        player.update()
        player.draw()

        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()

        zombiebullet_group.update()
        bullet_group.update()
        grenade_group.update()
        explosion_group.update()
        moloexplosion_group.update()
        molotov_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        zombiebullet_group.draw(screen)
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        moloexplosion_group.draw(screen)
        molotov_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

        if player.alive:
            if shoot:
                player.shoot()
            elif grenade and grenade_thrown == False and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),
                                  player.rect.top, player.direction)
                grenade_group.add(grenade)
                player.grenades -= 1
                grenade_thrown = True
            elif molotov and molotov_thrown == False and player.molotovs > 0:
                molotov = Molotov(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),
                                  player.rect.top, player.direction)
                molotov_group.add(molotov)
                player.molotovs -= 1
                molotov_thrown = True
            if player.in_air:
                player.update_action(2)  # 2: jump
            elif moving_left or moving_right:
                player.update_action(1)  # 1: run
            else:
                player.update_action(0)  # 0: idle
            screen_scroll, level_complete = player.move(
                moving_left, moving_right)
            bg_scroll -= screen_scroll
            # LEVEL COMPLETE
            if level_complete:
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    # CREATING WORLD
                    world, player, health_bar = load_world_data(level)

        else:  #如果玩家死亡，代码显示"YOU DIED!"的消息，并提供重新开始关卡或退出游戏的选项
            screen_scroll = 0
            draw_text('YOU DIED!', YOUDIED, WHITE, 260, 150), GAMEOVER.stop()
            screen.blit(headdeadhp, (-4, 2))
            if exit_button_die.draw(screen):
                MENUSELECT.play()
                run = False
            if restart_button.draw(screen):
                MENUSELECT.play()
                bg_scroll = 0
                world_data = reset_level()
                #CREATE WORLD DATA
                world, player, health_bar = load_world_data(level)


    for event in pygame.event.get():
        # QUIT GAME
        if event.type == pygame.QUIT:
            MENUSELECT.play()
            run = False
        # KEYBOARD SETT

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_e:
                molotov = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
                MENUSELECT.play()
            if event.key == pygame.K_m:
                pygame.mixer.music.pause()
                MENUSELECT.play()
            if event.key == pygame.K_u:
                pygame.mixer.music.unpause()
                MENUSELECT.play()
            if event.key == pygame.K_f:
                SCREEN_WIDTH = 1080
                SCREEN_HEIGHT = 1920
                pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                MENUSELECT.play()
            if event.key == pygame.K_F5:
                takescreenshot(screen)
                MENUSELECT.play()
                SCREENSHOT.play()

        # KEYBOARDS SETT2

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False
            if event.key == pygame.K_e:
                molotov = False
                molotov_thrown = False


    pygame.display.update()

pygame.quit()



# AUTHOR: Jan Kupczyk
# GITHUB: https://github.com/jankupczyk
# LICENSE: MIT

# FINALLY: 
# Be aware that Zombioo™ is my school project
# This Isn't a full plan game, does not guarantee that the game will be supported in the future!