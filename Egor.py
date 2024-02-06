import os
import sys

import pygame
import requests

x, y = 133.795393, -25.694776
xm, ym = 32, 32
sloi = ['map', 'sat','skl']
index_map = 0
map_request = f"http://static-maps.yandex.ru/1.x/?ll={x},{y}&spn={xm},{ym}&l=map"
response = requests.get(map_request)

map_file = "map.png"
if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)


def map():
    with open(map_file, "wb") as file:
        file.write(response.content)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()

map()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if xm <= 32 and ym <= 32:
                    xm = int(xm * 2)
                    ym = int(ym * 2)
                    map_request = f"http://static-maps.yandex.ru/1.x/?ll={x},{y}&spn={xm},{ym}&l={sloi[index_map]}"
                    response = requests.get(map_request)
                    map()
            elif event.key == pygame.K_PAGEDOWN:
                if xm >= 3 and ym >= 3:
                    xm = int(xm // 2)
                    ym = int(ym // 2)
                    map_request = f"http://static-maps.yandex.ru/1.x/?ll={x},{y}&spn={xm},{ym}&l={sloi[index_map]}"
                    response = requests.get(map_request)
                    map()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                index_map += 1
                if index_map > 2:
                    index_map = 0
                map_request = f'http://static-maps.yandex.ru/1.x/?ll={x},{y}&spn={xm},{ym}&l={sloi[index_map]}'
                response = requests.get(map_request)
                map()

pygame.quit()

os.remove(map_file)
