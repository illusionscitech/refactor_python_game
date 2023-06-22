# -*- coding: utf-8 -*-
# @Time ： 22.06.2023 10:55
# @Auth ： 张卓 zhang zhuo Чжан Чжо
# @File ：animations.py
# @IDE ：PyCharm
# @Motto：To live is to change the world.
import os
import pygame

#模块化加载动画
def load_animation(char_type, animation_types, scale):
    animation_list = []

    for animation in animation_types:
        temp_list = []
        num_of_frames = len(os.listdir(f'img/{char_type}/{animation}'))
        for i in range(num_of_frames):
            img = pygame.image.load(f'img/{char_type}/{animation}/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        animation_list.append(temp_list)

    return animation_list