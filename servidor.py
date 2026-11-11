"""Servidor de chat TCP multihilo.

El servidor acepta hasta dos clientes y reenvia cada mensaje a todos los
participantes conectados. Tambien puede enviar mensajes desde su propia
terminal, por lo que existen tres participantes.
"""

import os
import socket
import threading


HOST = "0.0.0.0"
PORT = int(os.getenv("CHAT_PORT", "5000"))
MAX_CLIENTS = 2

clients: dict[socket.socket, str] = {}
clients_lock = threading.Lock()


def broadcast(message: str, sender: socket.socket | None = None) -> None:
    """Envia un mensaje a todos los clientes."""
    data = f"{message}\n".encode("utf-8")
    with clients_lock:
        recipients = list(clients)

    for client in recipients:
        if client is sender:
            continue
        try:
            client.sendall(data)
        except OSError:
            remove_client(client)


def remove_client(client: socket.socket) -> str | None:
    """Quita un cliente de la lista y cierra su socket."""
    with clients_lock:
        name = clients.pop(client, None)
    try:
        client.close()
    except OSError:
        pass
    return name


def handle_client(client: socket.socket, address: tuple[str, int]) -> None:
    """Lee mensajes de un cliente hasta que este se desconecta."""
    try:
        client.sendall(b"Escribe tu nombre: ")
        name = client.recv(128).decode("utf-8").strip()
        if not name:
            name = f"Cliente-{address[1]}"

        with clients_lock:
            clients[client] = name

        print(f"[SISTEMA] {name} Este wey se conecto desde {address[0]}:{address[1]}")
        broadcast(f"[SERVIDOR] {name} el wey se conecto.", sender=client)
        client.sendall(b"[SERVIDOR] Conexion establecida con exito exitoso. Ya se puede escribir en este chat secreto.\n")

        buffer = ""
        while True:
            chunk = client.recv(4096)
            if not chunk:
                break
            buffer += chunk.decode("utf-8")
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                message = line.strip()
                if message:
                    formatted = f"[{name.upper()}]: {message}"
                    print(formatted)
                    broadcast(formatted, sender=client)
    except (ConnectionError, UnicodeDecodeError) as error:
        print(f"[SISTEMA] Conexion interrumpida noooo!!! : {error}")
    finally:
        name = remove_client(client)
        if name:
            print(f"[SISTEMA] {name} se desconecto.")
            broadcast(f"[SERVIDOR] {name} se ha desconectado.")


def server_input() -> None:
    """Permite al servidor escribir mensajes sin que se bloquen las las conexiones."""
    while True:
        try:
            message = input()
        except EOFError:
            return
        if message.strip():
            formatted = f"[SERVIDOR]: {message.strip()}"
            print(formatted)
            broadcast(formatted)


def main() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(MAX_CLIENTS)

    print(f"[SERVIDOR] Escuchando en {HOST}:{PORT}")
    print(f"[SERVIDOR] Esperando hasta {MAX_CLIENTS} clientes. Escribe mensajes cuando quieras no te semores mucho.")
    threading.Thread(target=server_input, daemon=True).start()

    try:
        while True:
            client, address = server.accept()
            with clients_lock:
                is_full = len(clients) >= MAX_CLIENTS
            if is_full:
                client.sendall(b"[SERVIDOR] Ya hay dos clientes conectados solo se puede dos. Conexion rechazada.\n")
                client.close()
                continue
            threading.Thread(target=handle_client, args=(client, address), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[SERVIDOR] Cerrando servidor adios...")
    finally:
        with clients_lock:
            connected_clients = list(clients)
        for client in connected_clients:
            client.close()
        server.close()


if __name__ == "__main__":
    main()