import cv2
import socket
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Função para enviar comando para o servidor TCP
def enviar_comando_tcp(comando):
    try:
        # Conectando ao servidor TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('192.168.10.150', 9999))  # Endereço e porta do servidor
            s.sendall(comando.encode('utf-8'))  # Envia o comando como bytes
            print(f'Comando enviado: {comando}')
    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")
        messagebox.showerror("Erro", f"Erro ao conectar ao servidor: {e}")
        return
    messagebox.showinfo("Sucesso", f"Comando {comando} enviado com sucesso!")

# Função para capturar o vídeo, detectar pessoas com Haar Cascade e atualizar a imagem no Tkinter
def gerar_video(label):
    # Carregar o classificador Haar Cascade para detecção de corpo humano
    body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

    # URL da câmera (substitua pelo IP correto)
    ip = "http://192.168.10.150:8080/video"
    video = cv2.VideoCapture(ip)

    if not video.isOpened():
        messagebox.showerror("Erro", "Erro ao abrir o vídeo da câmera. Verifique a URL e a conexão.")
        return

    # Variáveis para manter o maior corpo detectado e o tempo que ele deve permanecer na tela
    last_detected = None
    stay_time = 30  # Número de quadros que a caixa permanecerá na tela
    counter = 0  # Contador de quadros

    while True:
        check, frame = video.read()
        if not check:
            break

        # Converter a imagem para escala de cinza (necessário para detecção Haar Cascade)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detecção de pessoas no frame usando o classificador Haar Cascade
        bodies = body_cascade.detectMultiScale(gray, 1.1, 3)

        if len(bodies) > 0:
            # Encontrar o maior corpo detectado
            max_area = 0
            largest_body = None
            for (x, y, w, h) in bodies:
                area = w * h
                if area > max_area:
                    max_area = area
                    largest_body = (x, y, w, h)

            # Se encontramos um novo maior corpo, atualize a detecção
            last_detected = largest_body
            counter = stay_time  # Reinicia o contador de tempo para manter a caixa na tela

        # Se a caixa ainda deve permanecer na tela
        if last_detected and counter > 0:
            x, y, w, h = last_detected
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            label_text = "Pessoa"
            cv2.putText(frame, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            counter -= 1  # Diminui o contador a cada quadro

        # Converter o frame para RGB e mostrar na interface gráfica
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(img)

        # Atualizar o label com a nova imagem
        label.config(image=img_tk)
        label.image = img_tk

        # Atualizar a interface
        root.update()

# Função para enviar comando ao pressionar os botões
def enviar_comando(comando):
    enviar_comando_tcp(comando)

# Criando a interface gráfica com Tkinter
root = tk.Tk()
root.title("Controle de Videogame")

# Criando o rótulo para exibir o vídeo
label_video = tk.Label(root)
label_video.pack(padx=10, pady=10)

# Criando os botões para enviar comandos
button_frame = tk.Frame(root)
button_frame.pack(padx=10, pady=10)

btn_cima = tk.Button(button_frame, text="Cima", width=10, height=3, command=lambda: enviar_comando('w'))
btn_cima.grid(row=0, column=1, pady=10)

btn_esquerda = tk.Button(button_frame, text="Esquerda", width=10, height=3, command=lambda: enviar_comando('a'))
btn_esquerda.grid(row=1, column=0, pady=10)

btn_direita = tk.Button(button_frame, text="Direita", width=10, height=3, command=lambda: enviar_comando('d'))
btn_direita.grid(row=1, column=2, pady=10)

btn_baixo = tk.Button(button_frame, text="Baixo", width=10, height=3, command=lambda: enviar_comando('s'))
btn_baixo.grid(row=2, column=1, pady=10)

btn_parar = tk.Button(button_frame, text="Parar", width=10, height=3, command=lambda: enviar_comando('p'))
btn_parar.grid(row=3, column=1, pady=10)

# Iniciar a captura de vídeo
root.after(0, gerar_video, label_video)

# Iniciar o loop principal do Tkinter
root.mainloop()
