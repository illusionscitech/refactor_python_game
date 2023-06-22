# -*- coding: utf-8 -*-
# @Time ： 22.06.2023 11:07
# @Auth ： 张卓 zhang zhuo Чжан Чжо
# @File ：ai.py
# @IDE ：PyCharm
# @Motto：To live is to change the world.
import random

#处理士兵的AI行为。当士兵与玩家角色的视野矩形相交时，进行射击；否则，根据移动方向进行移动。此外，还包括处理士兵的闲置状态和视野范围的更新。
def ai(self,player,TILE_SIZE,screen_scroll):
    if self.alive and player.alive:
        if self.idling == False and random.randint(1, 400) == 1:
            self.update_action(0)  # IDLE
            self.idling = True
            self.idling_counter = 45
        if self.vision.colliderect(player.rect):
            self.update_action(0)  # IDLE
            # SHOOTING
            self.shoot()
        else:
            if self.idling == False:
                if self.direction == 1:
                    ai_moving_right = True
                else:
                    ai_moving_right = False
                ai_moving_left = not ai_moving_right
                self.move(ai_moving_left, ai_moving_right)
                self.update_action(1)  # RUN
                self.move_counter += 1
                self.vision.center = (
                    self.rect.centerx + 75 * self.direction, self.rect.centery)

                if self.move_counter > TILE_SIZE:
                    self.direction *= -1
                    self.move_counter *= -1
            else:
                self.idling_counter -= 1
                if self.idling_counter <= 0:
                    self.idling = False

    # SCROLLBG
    self.rect.x += screen_scroll