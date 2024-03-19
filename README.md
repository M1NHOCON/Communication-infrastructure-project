# Communication-infrastructure-project

#Portuguese

Este projeto, da disciplina de infraestrutura de comunicação, trata-se de um sistema de reservas de salas. todo o projeto foi desenvolvido em python utilizando sockets, UDP (como protocolo de transporte) implementado juntamente com o RDT 3.0 (para assegurar que os dados vao ser transmitidos corretamente).

**Servidor**:

1. **Inicialização do Servidor**: O servidor é inicializado em um endereço IP específico (`127.0.0.1`) e na porta `12345`. Um socket UDP é criado e vinculado ao endereço do servidor.
2. **Função de Envio e Recebimento com RDT 3.0**: As funções `send_rdt()` e `receive_rdt()` são responsáveis pela comunicação confiável entre cliente e servidor usando o protocolo RDT 3.0. Elas garantem que as mensagens sejam entregues corretamente e na ordem correta.
3. **Gerenciamento de Clientes**: Os clientes conectados são armazenados em uma lista de clientes, que contém informações como nome, endereço IP:PORTA e soquete do cliente.
4. **Gerenciamento de Reservas**: As reservas de salas são armazenadas em uma lista de reservas. A função `reservar_sala()` permite que os clientes reservem salas para determinados dias e horários, enquanto a função `cancelar_reserva()` permite que os clientes cancelem suas reservas.
5. **Listagem de Usuários Conectados**: A função `listar_usuarios()` permite que os clientes vejam uma lista de todos os usuários conectados ao servidor.
6. **Checagem de Disponibilidade de Reservas**: A função `check_reserva()` permite que os clientes verifiquem a disponibilidade de horários para uma determinada sala em um determinado dia.
7. **Loop Principal do Servidor**: O servidor fica em um loop infinito, recebendo mensagens dos clientes, processando-as e respondendo conforme necessário.
8. **Conexão de Clientes**: Quando um cliente se conecta ao servidor, ele envia uma mensagem informando seu nome de usuário.
9. **Desconexão de Clientes**: Quando um cliente deseja se desconectar do servidor, ele envia uma mensagem com o comando "bye", e o servidor remove o cliente da lista de clientes e informa aos outros clientes sobre sua saída.


**Cliente:**

1. **Conexão com o Servidor:** Os clientes podem se conectar ao servidor digitando o comando `connect as <nome_do_usuario>`. Uma vez conectados, eles podem interagir com o sistema de reservas.
2. **Reserva de Salas:** Os clientes podem reservar uma sala especificando o número da sala, o dia e a hora desejados, usando o comando `reservar <num_sala> <dia> <hora>`.
3. **Cancelamento de Reservas:** Os clientes podem cancelar uma reserva específica usando o comando `cancelar <num_sala> <dia> <hora>`.
4. **Verificação de Disponibilidade de Salas:** Os clientes podem verificar a disponibilidade de uma sala em um determinado dia usando o comando `check <num_sala> <dia>`.
5. **Listagem de Usuários Conectados:** Os clientes podem visualizar uma lista de todos os usuários conectados ao servidor digitando o comando `list`.
6. **Menu de Ajuda:** Os clientes podem visualizar um menu de ajuda digitando os comandos `help` ou `menu`.
7. **Limpeza do Terminal:** Os clientes podem limpar o terminal digitando o comando `cls`.

**Como usar o programa?**

1 - Pelo terminal, inicialize primeiramente o servidor (server.py)
2 - Inicialize os clientes (client.py)
3 - Caso tenha alguma dúvida para utilizar o programa, utilize o comando `help` ou `menu`
4 - Para se conectar no servidor, use o comando `connect as <nome_usuario>`
5 - Para listar os usuários conectados no momento, utilize o comando `list`
6 - Para realizar uma reserva, utilize o comando `reservar <num_sala> <dia> <hora>`, certifique-se de que o dia está entre segunda e sexta, e a hora está entre 8h e 17h
7 - Para cancelar uma reserva, utilize o comando `cancelar <num_sala> <dia> <hora>`, certifique-se de que a reserva realmente foi feita.
8 - Para verificar a disponibiidade de uma sala em um determinado dia, utilize o comando `check <num_sala> <dia>`.
9 - Para sair do servidor, use o comando `bye`.

#English

This project, from the Communication Infrastructure course, is a room reservation system. The entire project was developed in Python using sockets, UDP (as the transport protocol) implemented together with RDT 3.0 (to ensure that data is transmitted correctly).

**Server**:

1. **Server Initialization**: The server is initialized at a specific IP address (`127.0.0.1`) and port `12345`. A UDP socket is created and bound to the server's address.
2. **Sending and Receiving Function with RDT 3.0**: The `send_rdt()` and `receive_rdt()` functions are responsible for reliable communication between client and server using the RDT 3.0 protocol. They ensure that messages are delivered correctly and in the correct order.
3. **Client Management**: Connected clients are stored in a list of clients, which contains information such as name, IP:PORT address, and client socket.
4. **Reservation Management**: Room reservations are stored in a list of reservations. The `reservar_sala()` function allows clients to reserve rooms for specific days and times, while the `cancelar_reserva()` function allows clients to cancel their reservations.
5. **Listing Connected Users**: The `listar_usuarios()` function allows clients to see a list of all users connected to the server.
6. **Checking Reservation Availability**: The `check_reserva()` function allows clients to check the availability of time slots for a particular room on a specific day.
7. **Server's Main Loop**: The server remains in an infinite loop, receiving messages from clients, processing them, and responding as necessary.
8. **Client Connection**: When a client connects to the server, it sends a message informing its username.
9. **Client Disconnection**: When a client wants to disconnect from the server, it sends a message with the "bye" command, and the server removes the client from the list of clients and informs other clients about their departure.

**Client**:

1. **Connecting to the Server**: Clients can connect to the server by typing the command `connect as <username>`. Once connected, they can interact with the reservation system.
2. **Room Reservation**: Clients can reserve a room by specifying the room number, day, and desired time using the command `reservar <room_num> <day> <time>`.
3. **Canceling Reservations**: Clients can cancel a specific reservation using the command `cancelar <room_num> <day> <time>`.
4. **Checking Room Availability**: Clients can check the availability of a room on a particular day using the command `check <room_num> <day>`.
5. **Listing Connected Users**: Clients can view a list of all users connected to the server by typing the command `list`.
6. **Help Menu**: Clients can view a help menu by typing the commands `help` or `menu`.
7. **Terminal Clearing**: Clients can clear the terminal by typing the command `cls`.

**How to use the program?**

1 - First, initialize the server in the terminal (server.py)
2 - Initialize the clients (client.py)
3 - If you have any questions about using the program, use the `help` or `menu` command
4 - To connect to the server, use the command `connect as <username>`
5 - To list the users currently connected, use the command `list`
6 - To make a reservation, use the command `reservar <room_num> <day> <time>`, make sure the day is between Monday and Friday, and the time is between 8am and 5pm
7 - To cancel a reservation, use the command `cancelar <room_num> <day> <time>`, make sure the reservation was actually made.
8 - To check the availability of a room on a specific day, use the command `check <room_num> <day>`.
9 - To disconnect from the server, use the command `bye`.
