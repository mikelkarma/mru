from colorama import Fore, Back, Style, init
import os
import math
import sys
import time

# Tamanho do mapa
MAP_WIDTH = 50
MAP_HEIGHT = 25
PLAYER_SYMBOL = '👾'
OBJECT_SYMBOL = '#'
WALL_HORIZONTAL = '-'
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
def exibir_banner(angulo_atual, mapa, log_commands, angulo_ultrassonico):
    clear_terminal()
    angulobar = loading_bar(angulo_atual)
    
    anguloultrassonico = loading_bar(angulo_ultrassonico)
    
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
        f"     |-> {angulobar} : Angulo do eixo do robo",
        f"     |-> {anguloultrassonico} : Angulo do eixo do servo "
    ]

    # Imprimir o banner e o mapa lado a lado
    for i in range(len(banner_lines)):
        map_row = ''.join(mapa[i]) if i < len(mapa) else ' ' * MAP_WIDTH
        print(f"{banner_lines[i]}    {map_row}")

    # Imprimir log de comandos abaixo do mapa
    print("\nLog de Comandos:")
    for log in log_commands:
        print(f"  - {log}")

# Cálculo de movimento retiliano uniforme
velocidade = 2 / 5
tempo_total = 4.3
angulo_atual = 0
angulo_ultrassonico = 0

# Função para calcular o tempo necessário para percorrer uma certa distância
def calcular_mru(distancia):
    return distancia / velocidade

# Função para calcular o tempo necessário para girar até um ângulo desejado
def calcular_angulo(angulo_desejado, tempo_total):
    return (angulo_desejado / 360) * tempo_total

# Função para enviar comandos e armazenar no log
def send_commands_serial(funcao, tempo):
    comando = f"{funcao} por {tempo:.2f} segundos"
    commands.append(comando)
    # Limita o log a 7 comandos
    if len(commands) > 7:
        commands.pop(0)  # Remove o comando mais antigo
    print(comando)

commands = []

def frente(distancia):
    tempo = calcular_mru(distancia)
    send_commands_serial("mover para frente", tempo)

def girar(angulo_atual, angulo_desejado, tempo_total):
    diferenca = (angulo_desejado - angulo_atual) % 360
    if diferenca > 180:
        angulo_final = (angulo_atual - (360 - diferenca)) % 360
    else:
        angulo_final = (angulo_atual + diferenca) % 360
    
    tempo = calcular_angulo(abs(angulo_final - angulo_atual), tempo_total)
    direcao = 'girar para a direita' if diferenca <= 180 else 'girar para a esquerda'
    send_commands_serial(direcao, tempo)
    
    return angulo_final

# Loop principal
player_pos = (MAP_WIDTH // 2, MAP_HEIGHT // 2)
objects = []

try:
    while True:
        # Atualiza o ângulo e o mapa
        mapa = draw_map(player_pos, objects)
        exibir_banner(angulo_atual, mapa, commands, angulo_ultrassonico)
        
        # Atualiza a saída em tempo real
        sys.stdout.flush()
        
        cmd = input('> ')
        if cmd == 'girar': 
           angulo = float(input("girar para qual angulo? "))
           angulo_atual = girar(angulo_atual, angulo, tempo_total)
        if cmd == 'frente':
            distancia = float(input('percorrer quantos metros? '))
            frente(distancia)
        if cmd == 'scan':
            objects = [] # // reset obeject
            angulo_ultrassonico = 0 # // reset servo
            for graus_utrassonico in range(angulo_ultrassonico, 360, 1):
               add_object(objects, graus_utrassonico, 5)               
               mapa = draw_map(player_pos, objects)
               exibir_banner(angulo_atual, mapa, commands, graus_utrassonico)
               sys.stdout.flush()
               
               
except KeyboardInterrupt:
    print("\nSaindo do programa.")
