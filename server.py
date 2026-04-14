import socket
import threading
from crypto import decrypt_message

HOST = "0.0.0.0"
PORT = 9999

clients = []

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket, addr):
    print(f"[+] New connection: {addr}")
    
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break

            # Log encrypted message
            with open("chat.log", "a") as f:
                f.write(data.hex() + "\n")

            try:
                decrypted = decrypt_message(data)
                print(f"[{addr}] {decrypted}")
            except:
                print(f"[{addr}] (Decryption Failed)")

            broadcast(data, client_socket)

        except:
            break

    print(f"[-] Disconnected: {addr}")
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[+] Server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)

        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
