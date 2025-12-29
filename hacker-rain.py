import pygame
import random
import sys
import os
import tkinter as tk

def get_last_monitor_info():
    root = tk.Tk()
    root.withdraw() # Прячем окно тикинтера
    
    # Получаем данные о мониторах через WinAPI/X11
    # screen_width и height — это суммарное разрешение, если мы не уточняем.
    # Поэтому используем более надежный метод через pygame после инициализации.
    root.destroy()

def run_matrix():
    # Предварительная инициализация для получения данных о дисплеях
    pygame.init()
    
    # Находим самый правый монитор по координате X
    num_displays = pygame.display.get_num_displays()
    
    # Если монитор один, выбора нет. Если больше — ищем последний.
    last_idx = num_displays - 1
    
    # Пытаемся получить геометрию последнего монитора
    # В полноэкранном режиме (но без захвата) используем дисплей по индексу
    
    # ВАЖНО: Устанавливаем переменную окружения ДО создания окна
    # Она привязывает окно к верхнему левому углу нужного монитора
    # Но в некоторых версиях SDL надежнее просто указать display в set_mode
    
    # Флаги: NOFRAME (без рамок), ALWAYS_ONTOP (поверх всех)
    flags = pygame.NOFRAME
    if hasattr(pygame, 'ALWAYS_ONTOP'):
        flags |= pygame.ALWAYS_ONTOP

    try:
        # display=last_idx — ключевой параметр
        # (0, 0) говорит Pygame взять полное разрешение этого монитора
        screen = pygame.display.set_mode((0, 0), flags, display=last_idx)
    except:
        # Если не вышло, пробуем принудительно через FULLSCREEN на конкретном дисплее
        screen = pygame.display.set_mode((0, 0), flags | pygame.FULLSCREEN, display=last_idx)

    width, height = screen.get_size()
    pygame.mouse.set_visible(False)

    # Параметры дождя
    font_size = 22
    font = pygame.font.SysFont('consolas', font_size, bold=True)
    columns = width // font_size
    drops = [random.randint(-height // font_size, 0) for _ in range(columns)]

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # Эффект затухания
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 35)) 
        screen.blit(overlay, (0, 0))

        for i in range(len(drops)):
            char = random.choice(['0', '1'])
            char_render = font.render(char, True, (0, 255, 70))
            
            x = i * font_size
            y = drops[i] * font_size
            screen.blit(char_render, (x, y))

            if y * font_size > height and random.random() > 0.975:
                drops[i] = 0
            drops[i] += 1

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    run_matrix()
