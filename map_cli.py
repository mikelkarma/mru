import math
import os
import time

# Tamanho do mapa
map_width = 80
map_height = 40
player_pos = (map_width // 2, map_height // 2)

# Função para desenhar o mapa
def draw_map(objects):
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpa o terminal
    map_grid = [[' ' for _ in range(map_width)] for _ in range(map_height)]
    
    # Desenha linhas paralelas
    for y in range(map_height):
        map_grid[y][0] = '|'
        map_grid[y][-1] = '|'
    for x in range(map_width):
        map_grid[0][x] = '-'
        map_grid[-1][x] = '-'

    # Posição do player
    player_x, player_y = player_pos
    map_grid[player_y][player_x] = 'P'  # 'P' para Player

    # Adiciona objetos
    for angle, distance in objects:
        obj_x = int(player_x + distance * math.cos(math.radians(angle)))
        obj_y = int(player_y + distance * math.sin(math.radians(angle)))
        if 0 <= obj_x < map_width and 0 <= obj_y < map_height:
            map_grid[obj_y][obj_x] = 'O'  # 'O' para Object

    # Exibe o mapa
    for row in map_grid:
        print(''.join(row))

# Função para adicionar objetos
def add_object(angle, distance):
    objects.append((angle, distance))

# Loop principal
def main():
    global objects
    objects = []

    # Adiciona objetos em ângulos e distâncias
    for graus in range(0, 361, 20):  # A cada 20 graus até 360
      add_object(graus, 10)

    while True:
        draw_map(objects)
        time.sleep(0.5)

if __name__ == "__main__":
    main()  
