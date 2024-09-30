from colorama import Fore, Back, Style, init
import time
import os

# Inicializa o Colorama
init(autoreset=True)
def loading_bar(progress):
    total_length = 10
    filled_length = int(total_length * progress // 360)
    bar = '#' * filled_length + '-' * (total_length - filled_length)
    percentage = (progress / 360) * 100
    return (f'[{bar}] {progress}° ({percentage:.2f}%)')

# Banner com dados
def exibir_banner(angulo_atual):
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela
    angulobar=loading_bar(angulo_atual)
    banner = f'''
{Fore.MAGENTA}{Back.BLACK}                ____{Style.RESET_ALL}
                /___.`--.____ .--. ____.--(
                       .'_.- (    ) -._'. 
                     .'.'    |'..'|    '.' 
              .-.  .' /'--.__|____|__.--'\\ '.  .-.
             (O).)-| |  \\    |    |    /  | |-(.(O)
              `-'  '-'-._'-./      \\.-'_.-'-'  `-'
                 _ | |   '-.________.-'   | | _
              .' _ | |     |   __   |     | | _ '.      // Coded create by Luis F.
             / .' ''.|     | /    \\ |     |.'' '. \\     // Angulo atual: {angulo_atual}
             | |( )| '.    ||      ||    .' |( )| |          |-> {angulobar}
             \\ '._.'   '.  | \\    / |  .'   '._.' /
              '.__ ______'.|__'--'__|.'______ __.'
             .'_.-|         |------|         |-._'.
            //\\\\  |         |--::--|         |  //\\\\
           //  \\\\ |         |--::--|         | //  \\\\
          //    \\\\|        /|--::--|\\        |//    \\\\
         / '._.-'/|_______/ |--::--| \\_______|\\`-._.' \\
        / __..--'        /__|--::--|__\\        `--..__ \\
       / /               '-.|--::--|.-'               \\ \\
      / /                   |--::--|                   \\ \\
     / /                    |--::--|                    \\ \\
 _.-'  `-._                 _..||.._                  _.-` '-._
'--..__..--'               '-.____.-'                '--..__..--'  
    '''
    
    print(banner)

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

angulo_atual = girar(angulo_atual, 90, tempo_total)
exibir_banner(angulo_atual)
