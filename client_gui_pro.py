import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from crypto import encrypt_message, decrypt_message

HOST = "127.0.0.1"
PORT = 9999

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Encrypted Chat App")
        self.root.geometry("500x500")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        # Chat display
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state='disabled')

        # Input field
        self.msg_entry = tk.Entry(root)
        self.msg_entry.pack(padx=10, pady=10, fill=tk.X)
        self.msg_entry.bind("<Return>", self.send_message)

        # Send button
        self.send_btn = tk.Button(root, text="Send", command=self.send_message)
        self.send_btn.pack(pady=5)

        # Start receiving thread
        thread = threading.Thread(target=self.receive_messages)
        thread.daemon = True
        thread.start()

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def send_message(self, event=None):
        msg = self.msg_entry.get()
        if msg.strip() == "":
            return

        encrypted = encrypt_message(msg)
        self.client.send(encrypted)

        self.display_message(f"You: {msg}")
        self.msg_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(4096)
                if not data:
                    break

                try:
                    message = decrypt_message(data)
                    self.display_message(f"Friend: {message}")
                except:
                    self.display_message("[!] Decryption failed")

            except:
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()
