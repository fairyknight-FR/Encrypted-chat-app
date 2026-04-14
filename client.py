import socket
import threading
from crypto import encrypt_message, decrypt_message

HOST = "127.0.0.1"  # Change if server remote
PORT = 9999

def receive_messages(client):
    while True:
        try:
            data = client.recv(4096)
            if not data:
                break

            try:
                message = decrypt_message(data)
                print(f"\nFriend: {message}")
            except:
                print("\n[!] Failed to decrypt message")

        except:
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    print("[+] Connected to server")

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    while True:
        msg = input("You: ")
        encrypted = encrypt_message(msg)
        client.send(encrypted)

if __name__ == "__main__":
    start_client()
