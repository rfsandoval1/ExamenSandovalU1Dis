"""Cliente de terminal para el chat TCP."""

import argparse
import socket
import threading


def receive_messages(connection: socket.socket) -> None:
    """Imprime todos los mensajes que llegan mientras el usuario escribe."""
    buffer = ""
    try:
        while True:
            chunk = connection.recv(4096)
            if not chunk:
                print("\n[SISTEMA] El servidor cerro la conexion ya no hay chat.")
                return
            buffer += chunk.decode("utf-8")
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                print(f"\r{line}\n> ", end="", flush=True)
    except (ConnectionError, UnicodeDecodeError):
        print("\n[SISTEMA] Se perdio la conexion con el servidor.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Cliente del chat TCP")
    parser.add_argument("--name", required=True, help="Nombre visible del cliente")
    parser.add_argument("--host", default="127.0.0.1", help="Host del servidor")
    parser.add_argument("--port", type=int, default=5000, help="Puerto del servidor")
    args = parser.parse_args()

    with socket.create_connection((args.host, args.port)) as connection:
        prompt = connection.recv(128)
        print(prompt.decode("utf-8"), end="", flush=True)
        connection.sendall(f"{args.name}\n".encode("utf-8"))

        threading.Thread(target=receive_messages, args=(connection,), daemon=True).start()
        print("Escribe mensajes y presiona Enter. Usa Ctrl+C para salir.")
        try:
            while True:
                message = input("> ").strip()
                if message:
                    connection.sendall(f"{message}\n".encode("utf-8"))
        except (KeyboardInterrupt, EOFError):
            print("\n[SISTEMA] Cliente cerrado.")


if __name__ == "__main__":
    main()