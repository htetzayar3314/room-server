# room_server.py
import socket
import threading
import os

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 60000))  # Render sets PORT

clients = []

def client_thread(conn, addr):
    print(f"[CONNECTED] {addr}")
    clients.append(conn)
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            for client in clients:
                if client != conn:
                    client.sendall(data)
    except:
        pass
    finally:
        print(f"[DISCONNECTED] {addr}")
        clients.remove(conn)
        conn.close()

def main():
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen()
    print(f"[LISTENING] on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=client_thread, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
