import socket
import select
import keyboard
import pickle

HEADER_LENGTH = 10

IP = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432  # The port used by the server

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}

# REQUEST COMMANDS
ASK_FOR_SIT = "ask-for-sit"
UPDATE_POINTS = "update-points"
FREE_SIT = "free-sit"

G1_LABEL = "G1"
G2_LABEL = "G2"

print(f'Listening for connections on {IP}:{PORT}...')

# jakiś test róm
room = {
    "roomID": "1",
    "gracz1": "",  # czy ktoś siedzi na krześle gracza 1
    "gracz2": "",  # czy ktoś siedzi na krześle gracza 2
    "punkty_gracz1": 0,
    "punkty_gracz2": 0
}


def displayClients(e):
    if len(clients) != 0:
        print("--------------------------------------------------------------------------")
        print("Lista klientów:")
        for socket in sockets_list:
            if socket != server_socket:
                print(f" - {clients[socket]}")
        print("--------------------------------------------------------------------------")
    else:
        print("Nie ma klientów :(")


def deleteClient(sit):
    if len(clients) != 0:
        for socket in sockets_list:
            if socket != server_socket:
                if clients[socket]['sit'] == sit:
                    sockets_list.remove(socket)


def checkRoom(e):
    print(room)


# wciskamy i, wyświetli obecnych klientów w serwerze
keyboard.on_press_key("i", lambda e: displayClients(e))
keyboard.on_press_key("r", lambda e: checkRoom(e))


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            data = client_socket.recv(1024)
            result = 1
            if data is False:
                continue
            message = data.decode('utf-8')
            print(message)
            message = message.split(':')
            if message[0] == ASK_FOR_SIT:
                if message[1] == "G1" and len(room['gracz1']) == 0:
                    room['gracz1'] = message[2]
                    print("> sit accepted")
                    sockets_list.append(client_socket)
                    user = {'nickname': message[2], 'sit': message[1]}
                    clients[client_socket] = user
                    client_socket.sendall(b'1')
                elif message[1] == "G2" and len(room['gracz2']) == 0:
                    room['gracz2'] = message[2]
                    print("> sit accepted")
                    sockets_list.append(client_socket)
                    user = {'nickname': message[2], 'sit': message[1]}
                    clients[client_socket] = user
                    client_socket.sendall(b'1')
                else:
                    print("> sit denied")
                    client_socket.sendall(b'0')

            elif message[0] == UPDATE_POINTS:
                if message[1] == room['gracz1']:
                    room['punkty_gracz1'] += int(message[2])
                if message[1] == room['gracz2']:
                    room['punkty_gracz2'] += int(message[2])

            elif message[0] == FREE_SIT:
                if message[1] == G1_LABEL:
                    print("> sit 1 is now free & client deleted")
                    room['gracz1'] = ""
                    deleteClient(message[1])
                if message[1] == G2_LABEL:
                    print("> sit 2 is now free & client deleted")
                    deleteClient(message[1])
                    room['gracz2'] = ""
        else:
            message = receive_message(notified_socket)
            if message is False:
                # print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                # sockets_list.remove(notified_socket)
                # del clients[notified_socket]
                # print(sockets_list)
                continue
            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            for client_socket in clients:  # do wszystkich clientów
                if client_socket != notified_socket:  # oprócz wysyłającego
                    # coś możemy im wysłać, np odświeżenie ekranu
                    # client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                    print(user['headrer'])
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
