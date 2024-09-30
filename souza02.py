from colorama import Fore, Back, Style, init
import time
import os
import math

# Tamanho do mapa
MAP_WIDTH = 50
MAP_HEIGHT = 25
PLAYER_SYMBOL = '👾'  # Usando um símbolo mais visual para o jogador
OBJECT_SYMBOL = '#'    # Um símbolo diferente para os objetos
# WALL_HORIZONTAL = '━'
WALL_HORIZONTAL='-'
# WALL_VERTICAL = '┃'
WALL_VERTICAL = '|'
WALL_CORNER_TOP_LEFT = '┏'
WALL_CORNER_TOP_RIGHT = '┓'
WALL_CORNER_BOTTOM_LEFT = '┗'
WALL_CORNER_BOTTOM_RIGHT = '┛'

# Função para limpar o terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para desenhar o mapa
def draw_map(player_pos, objects):
    map_grid = [[' ' for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
    
    # Desenha paredes
    for y in range(MAP_HEIGHT):
        map_grid[y][0] = WALL_VERTICAL
        map_grid[y][-1] = WALL_VERTICAL
    for x in range(MAP_WIDTH):
        map_grid[0][x] = WALL_HORIZONTAL
        map_grid[-1][x] = WALL_HORIZONTAL

    # Desenhar cantos
    map_grid[0][0] = WALL_CORNER_TOP_LEFT
    map_grid[0][-1] = WALL_CORNER_TOP_RIGHT
    map_grid[-1][0] = WALL_CORNER_BOTTOM_LEFT
    map_grid[-1][-1] = WALL_CORNER_BOTTOM_RIGHT

    # Posição do player
    player_x, player_y = player_pos
    map_grid[player_y][player_x] = PLAYER_SYMBOL

    # Adiciona objetos
    for angle, distance in objects:
        obj_x = int(player_x + distance * math.cos(math.radians(angle)))
        obj_y = int(player_y + distance * math.sin(math.radians(angle)))
        if 0 <= obj_x < MAP_WIDTH and 0 <= obj_y < MAP_HEIGHT:
            map_grid[obj_y][obj_x] = OBJECT_SYMBOL

    return map_grid

# Função para adicionar objetos
def add_object(objects, angle, distance):
    objects.append((angle, distance))

# Inicializa o Colorama
init(autoreset=True)

def loading_bar(progress):
    total_length = 10
    filled_length = int(total_length * progress // 360)
    bar = '#' * filled_length + '-' * (total_length - filled_length)
    percentage = (progress / 360) * 100
    return f'[{bar}] {progress}° ({percentage:.2f}%)'

# Banner com dados
def exibir_banner(angulo_atual, mapa):
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela
    angulobar = loading_bar(angulo_atual)
    banner_lines = [
        
       
        "                /___.`--.____ .--. ____.--(                      ",
        "                       .'_.- (    ) -._'.                        ",
        "                     .'.'    |'..'|    '.'                       ",
        "              .-.  .' /'--.__|____|__.--'\\ '.  .-.               ",
        "             (O).)-| |  \\    |    |    /  | |-(.(O)              ",
        "              `-'  '-'-._'-./      \\.-'_.-'-'  `-'               ",
        "                 _ | |   '-.________.-'   | | _                  ",
        "              .' _ | |     |   __   |     | | _ '.               ",
        "             / .' ''.|     | /    \\ |     |.'' '. \\              ",
        "             | |( )| '.    ||      ||    .' |( )| |              ",
        "             \\ '._.'   '.  | \\    / |  .'   '._.' /              ",
        "              '.__ ______'.|__'--'__|.'______ __.'               ",
        "             .'_.-|         |------|         |-._'.              ",
        "            //\\\\  |         |--::--|         |  //\\\\        '    ",
        "           //  \\\\ |         |--::--|         | //  \\\\            ",
        "          //    \\\\|        /|--::--|\\        |//    \\\\           ",
        "         / '._.-'/|_______/ |--::--| \\_______|\\`-._.' \\          ",
        "        / __..--'        /__|--::--|__\\        `--..__ \\         ",
        "       / /               '-.|--::--|.-'               \\ \\        ",
        "      / /                   |--::--|                   \\ \\       ",
        "     / /                    |--::--|                    \\ \\      ",
        " _.-'  `-._                 _..||.._                  _.-` '-._  ",
        "'--..__..--'               '-.____.-'                '--..__..--'",
        "// Coded create by Luis F.                                 '     ",
        "// Angulo atual: " + str(angulo_atual) + "                '                            ",
        f"     |-> {angulobar}                        '      "
        
    ]

    # Imprimir o banner e o mapa lado a lado
    for i in range(len(banner_lines)):
        map_row = ''.join(mapa[i]) if i < len(mapa) else ' ' * MAP_WIDTH
        print(f"{banner_lines[i]}    {map_row}")

# Cálculo de movimento retiliano uniforme
velocidade = 2 / 5
tempo_total = 4.3
angulo_atual = 0

# Função para calcular o tempo necessário para percorrer uma certa distância
def calcular_mru(distancia):
    return distancia / velocidade

# Função para calcular o tempo necessário para girar até um ângulo desejado
def calcular_angulo(angulo_desejado, tempo_total):
    return (angulo_desejado / 360) * tempo_total

def send_commands_serial(funcao, tempo):
    print(funcao, tempo)

def frente(distancia):
    tempo = calcular_mru(distancia)
    send_commands_serial("w", tempo)

def girar(angulo_atual, angulo_desejado, tempo_total):
    diferenca = (angulo_desejado - angulo_atual) % 360
    if diferenca > 180:
        angulo_final = (angulo_atual - (360 - diferenca)) % 360
    else:
        angulo_final = (angulo_atual + diferenca) % 360
    
    tempo = calcular_angulo(abs(angulo_final - angulo_atual), tempo_total)
    send_commands_serial('angulo_direita' if diferenca <= 180 else 'angulo_esquerda', tempo)
    return angulo_final

# Loop principal
player_pos = (MAP_WIDTH // 2, MAP_HEIGHT // 2)
objects = []

# Adiciona objetos em ângulos e distâncias
for graus in range(0, 361, 1):  # A cada 1 grau até 360
    add_object(objects, graus, 5)

angulo_atual = girar(angulo_atual, 90, tempo_total)
mapa = draw_map(player_pos, objects)
exibir_banner(angulo_atual, mapa)
