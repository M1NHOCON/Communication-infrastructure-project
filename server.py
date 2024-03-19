import socket
import random

# Define as informações do servidor
server_address = ('127.0.0.1', 12345)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)
print(f"Servidor hospedado em {server_address}")

# Define as variáveis do servidor
clientes = []

reservas = []

# Função para enviar mensagem com rdt3.0
def send_rdt(message_str, client_socket,client_address):
    seq_num = 0
    while True:
        # Adiciona o número de sequência à mensagem
        message = f"ACK-{message_str}"
        # Envia a mensagem para o servidor
        if random.random() > 0.2:
            client_socket.sendto(message.encode(), client_address)
            # Espera pelo ACK
            try:
                client_socket.settimeout(2)
                ack, _ = client_socket.recvfrom(2048)
                if ack.decode() == f"ACK":
                    break
            except socket.timeout:
                pass
        # Verifica se o número máximo de tentativas foi atingido
        seq_num += 1
        if seq_num > 3:
            print("Nao foi possivel enviar a mensagem.")
            break

# Função para receber mensagem com rdt3.0
def receive_rdt(client_socket):
    while True:
        # Recebe a mensagem do servidor
        try:
            client_socket.settimeout(2)
            message, client_address = client_socket.recvfrom(2048)
            message_str = message.decode()
            # Verifica se a mensagem é um ACK
            if message_str.startswith("ACK"):
                # Envia o ACK de volta para o servidor
                ack = f"ACK"
                client_socket.sendto(ack.encode(), client_address)
                break
        except socket.timeout:
            pass

    part = message_str.split("-")
    if len(part) >= 2 and part[1] != "":
        return part[1][2:-1], client_address
    else:
        return None,None

# Função para enviar mensagem para todos os clientes
def broadcast(mensage, sender_address):
    if len(clientes) > 1:
        for cliente in clientes:
            if cliente['address'] != sender_address:
                send_rdt(mensage, cliente['socket'], cliente['address'])

# Função implementada para conectar clientes
def conecta_cliente(message, client_address, client_socket):
    global login
    nome = message.split() 

    usuario_presente = any(usuario["nome"] == nome[0] for usuario in clientes)
    aviso = "  Este nome de usuário já está em uso. "
    usuario_registrado = 'usuario registrado'
    if usuario_presente:
        send_rdt(aviso, client_socket, client_address)

    else:
        clientes.append({"nome": nome[0], "address": client_address, 'socket': client_socket})
        send_rdt(usuario_registrado.encode(), client_socket, client_address)
        aviso = f'  {nome[0]} se juntou a plataforma de reservas! '
        broadcast(aviso, client_address)
        login = True
        print(f'{nome[0]}:{client_address} se conectou')

# Função para verificar se dia, horario e sala estao entre os limites permitidos
def validar_horario(dia, horario, sala):
    dias_validos = ['seg', 'ter', 'qua', 'qui', 'sex']
    horas_validas = list(range(8, 18))
    salas_validas = list(range(101, 106))
    return str(dia).lower() in dias_validos and int(horario) in horas_validas and int(sala) in salas_validas

# Função para verificar se a sala está disponivel
def reserva_disponivel(dia, horario, sala):
    return not any(reserva['sala'] == sala and reserva['dia'] == dia and reserva['horario'] == horario for reserva in reservas)

# Função para reservar sala
def reservar_sala(info_reserva, client_address):
    info = info_reserva.split()
    sala = info[1]
    dia = info[2]
    horario = info[3]

    client_socket = [cliente['socket'] for cliente in clientes if cliente['address'] == client_address]
    
    if validar_horario(dia, horario, sala): 
        if reserva_disponivel(dia, horario, sala):
            nome = ''.join([cliente['nome'] for cliente in clientes if cliente['address'] == client_address]) # Nome recebe nome do usuario
            reservas.append({"sala": sala, "dia": dia, "horario": horario, "usuario": nome})   # Adiciona uma reserva no final do da lista de reservas

            broadcast(f"  {nome} reservou a sala {sala} na {dia} às {horario}h. ", client_address)
            send_rdt(f"  Você reservou a sala {sala} na {dia} às {horario}h. ", client_socket[0], client_address)
        else:
            send_rdt(f"  A sala {sala} na {dia} às {horario}h já está reservada. ", client_socket[0], client_address)
    else:
        send_rdt("  Horário inválido para reserva. ", client_socket[0], client_address)

# Função para cancelar reserva
def cancelar_reserva(client_address, sala, dia, horario):
    usuario = [user for user in clientes if user["address"] == client_address] # Usuário que aparentemente reservou a sala

    if(validar_horario(dia, horario, sala)): # Verificando se o horário, dia e sala são válidos.
        if not reserva_disponivel(dia, horario, sala): # Verificando se a sala está dispinível.
            for reserva in reservas:
                if(reserva['horario'] == horario and reserva['dia'] == dia and reserva['sala'] == sala and reserva['usuario'] == usuario[0]['nome']): # Se o usuário quer cancelar uma reserva que é dele.
                    send_rdt('  Reserva cancelada ', usuario[0]['socket'], usuario[0]["address"])
                    reservas.remove(reserva)
                    broadcast(f'  {usuario[0]["nome"]} cancelou a reserva da sala {sala} às {horario}h do dia {dia}! ', client_address) 
                else:
                    send_rdt('  Você não tem permissão para cancelar a reserva de outro usuário. ', usuario[0]['socket'], usuario[0]["address"]) # Se o usuário quer cancelar uma reserva que não é dele.
        else:
            send_rdt("  A sala não está reservada. ", usuario[0]['socket'], client_address) # Não há reserva para ser cancelada nessa sala e nesse dia
    else:
        send_rdt("  Digite valores válidos para dia, horário e sala. ", usuario[0]['socket'], client_address)

# Função para desconectar o cliente
def desconectar_cliente(client_address):
    nome = ''
    for cliente in clientes:
        if cliente['address'] == client_address: # Encontrou os dados do cliente a ser desconectado
            nome = cliente['nome']
            alert_message = f"  {nome} {client_address} saiu da sala. "
            broadcast(alert_message, client_address)
            clientes.remove(cliente)
            print(f"Cliente {nome}:{client_address} desconectado.")
            break

# Função para checar as reserva
def check_reserva(info_reserva, client_address):
    info = info_reserva.split()
    sala = int(info[1])
    dia = info[2]

    dias_validos = ['seg', 'ter', 'qua', 'qui', 'sex']
    horas_validas = list(range(8, 18))
    salas_validas = list(range(101, 106))

    disponiveis = [f'{horario_disponivel}h' for horario_disponivel in horas_validas if horario_disponivel]

    client_socket = [cliente['socket'] for cliente in clientes if cliente['address'] == client_address] # Socket do cliente

    if sala in salas_validas and dia in dias_validos:
        for reserva in reservas:
            #Pega os horarios que ja estao reservada e remove das disponiveis
            if reserva['sala'] == str(sala) and reserva['dia'] == dia:
                disponiveis.remove(reserva['horario']+'h')

        if len(disponiveis) == 0: 
            send_rdt(f'  Não há horarios disponiveis na {dia} para sala {sala} ', client_socket[0], client_address)

        else:
            send_rdt(f"  Horários disponíveis para a sala {sala} na {dia}:\n{', '.join(disponiveis)} ", client_socket[0], client_address)

    else:
        send_rdt(f"  sala ou dia invalidos, digite corretamente. ", client_socket[0], client_address)

# Função para listar usuarios
def listar_usuarios(client_address):
    client_socket = [cliente['socket'] for cliente in clientes if cliente['address'] == client_address] # Pega o socket do liente que solicitou a listagem

    if len(clientes) > 1:
        lista = ''
        lista = '\n'.join([user['nome'] for user in clientes]) # Adiciona o nome dos usuarios ao final da lista
        logados = f"  Usuários conectados:\n{lista}  "
        send_rdt(logados, client_socket[0], client_address)
    else:
        msg = '  só você esta logado '
        send_rdt(msg, client_socket[0], client_address)

# Função para lidar com as mensagens recebidas
def handle_message(message, client_address):
    global clientes, reservas
    if message == "bye":
        # Remove o cliente da lista de clientes
        desconectar_cliente(client_address)

    elif message.startswith("list"):
        # Lista os clientes
        listar_usuarios(client_address)

    elif message.startswith("reservar"):
        # Reserva sala
        reservar_sala(message, client_address)

    elif message.startswith("cancelar"):
        # Cancela reserva
        parts = message.split()
        cancelar_reserva(client_address, parts[1], parts[2], parts[3])

    elif message.startswith("check"):
        # Checa horarios livres da sala   
        check_reserva(message, client_address)

# Loop principal do server
while True:
    # Recebe uma mensagem de um cliente
    message, client_address = receive_rdt(server_socket)

    if message is None and client_address is None:
        continue
    
    elif(message.__contains__("entrou na sala.")):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.connect(client_address)
        conecta_cliente(message, client_address, client_socket)
    else:
        # Verifica se o cliente está na lista de clientes
        for cliente in clientes:
            if client_address == cliente['address']:
                handle_message(message, client_address)