import socket
import threading
import random
import os

# Função para enviar mensagem com rdt3.0
def send_rdt(message_str, client_socket, server_address):
    sequence_number = 0
    while True:
        # Adiciona o número de sequência à mensagem
        msg = f"ACK-{message_str}"
        # Envia a mensagem para o servidor
        if random.random() > 0.2:
            client_socket.sendto(msg.encode(), server_address)
            # Espera pelo ACK
            try:
                client_socket.settimeout(2)
                ack, _ = client_socket.recvfrom(2048)
                if ack.decode() == f"ACK":
                    break
            except socket.timeout:
                pass
        # Verifica se o número máximo de tentativas foi atingido
        sequence_number += 1
        if sequence_number > 3:
            print("Nao foi possivel enviar a mensagem.")
            break
        
# Função para receber mensagem com rdt3.0
def receive_rdt(client_socket):
    while True:
        # Recebe a mensagem do servidor
        try:
            client_socket.settimeout(2)
            msg, server_address = client_socket.recvfrom(2048)
            message_str = msg.decode()
            # Verifica se é um ACK
            if message_str.startswith("ACK"):
                # Devolve o ACK ao servidor
                ack = f"ACK"
                client_socket.sendto(ack.encode(), server_address)
                break
        except socket.timeout:
            pass
    
    str_list = message_str.split("-")
    if len(str_list) >= 2 and str_list[1] != "":
        return str_list[1][2:-1]
    else:
        return None


# Define o endereço do server
server_address = ('127.0.0.1', 12345)

# Define as informações do cliente
client_address = ('localhost', 0)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(client_address)

# Define as variáveis do cliente
nome = ''
connected = False

# Função para receber mensagens do servidor
def receive_messages():
    global connected
    while True:
        message_str = receive_rdt(client_socket)
        if message_str is not None:
            if message_str == 'usuario registrado':
                connected = True
            print(message_str)

# Função para enviar mensagens para o servidor
def send_message(message_str):
    global connected
    global nome 

    if message_str.startswith("connect as"):
        # Conecta o usuário ao servidor
        nome = message_str.split(" ")[2]
        # Envia mensagem de alerta da nova presença
        alert_message = f"{nome} entrou na sala."
        send_rdt(alert_message.encode(), client_socket, server_address)
    else:
        print("Voce precisa se conectar a sala primeiro.")

# Função para exibir a lista de usuários
def list_users():
    send_rdt("list".encode(),client_socket, server_address)

# Função para solicitar reserva ao servidor
def reservation(reserve):
    send_rdt(f"{reserve}".encode(), client_socket, server_address)

# Função para solicitar o cancelamento da reserva
def cancel_reserve(reserve):
    send_rdt(f"{reserve}".encode(),client_socket, server_address) #envia string pro server

# Função para verificar disponibilidade da sala
def check_disponibility(room):
    send_rdt(f"{room}".encode(),client_socket, server_address)

# Inicia a thread para receber mensagens do servidor
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

def menu():
    strfinal=''
    strmenu=['---------------------SISTEMA DE RESERVA DE SALA---------------------',
        'Conectar ao aplicativo:                 connect as <nome_do_usuario>',
        'Sair do aplicativo:                              bye                ',
        'Exibir lista de usuários:                        list               ',
        'Reservar uma sala:                  reservar <num_sala> <dia> <hora>',
        'Cancelar uma reserva:               cancelar <num_sala> <dia> <hora>',
        'Verificar disponibilidade da sala:      check <num_sala> <dia>      ',
        'Limpar terminal:                                  cls               ']
    strfinal= '\n'.join(strmenu)
    print(strfinal+ '\n')
# Loop principal do cliente
while True:
    message_str = input('')

    if message_str == 'cls' or message_str == 'help' or message_str == 'menu':
        if message_str == 'cls':
            os.system(message_str)
        else:
            menu()
    else:        
        # Verifica se o usuário está conectado
        if not connected:
            # Se não estiver, verifica se a mensagem é um comando de conexão
            send_message(message_str)
        else: 
            # Verifica se a mensagem é um comando
            if message_str.startswith("list"):
                list_users()

            elif message_str.startswith("reservar"): #reservar sala
                if(message_str.split(" ")[1] != "" and message_str.split(" ")[2] != "" and message_str.split(" ")[3] != ""):
                    reservation(message_str)
                else:
                    print("digite as informaçoes necessarias") #fazer menu

            elif message_str.startswith("cancelar"): #remove
                if(message_str.split(" ")[1] != "" and message_str.split(" ")[2] != "" and message_str.split(" ")[3] != ""):
                    cancel_reserve(message_str)
                else:
                    print("Voce precisa informar o nome de um usuario para removelo da sua lista de amigos.")

            elif message_str.startswith("check"): #cancelar reservar
                check_disponibility(message_str)

            elif message_str.startswith("bye"):
                connected = False
                send_rdt("bye".encode(),client_socket, server_address)
                print("Desconectado do servidor.")