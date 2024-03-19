**Membros do grupo**:

Johnny Cleiton `<jcfl2>`

Romulo Artur `<raasa>`

Samuel Nunes de Andrade `<sna2>`

Sara Nicoly `<snfl>`

Vinicius dos Santos Felix `<vsf2>`

Vittor Matheus `<vmmc3>`

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