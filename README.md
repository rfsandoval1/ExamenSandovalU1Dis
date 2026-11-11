# Chat TCP multihilo con Docker

La apliacion de chat en tiempo real esta echa en pyton, con sokets TCP e hilos
el servidor acepta dos clientes simultaneamente y distribuye los mensajes y el servidor tambien puede escribir mensajes

## Lo que se necesita

- Docker Desktop instalado y ejecutandose.
- Python 3.10 para los clientes.
- Dos terminales.

## 1. Iniciar el servidor en Docker

Desde la carpeta del proyecto, ejecutar:

```bash
docker compose up --build
```

El puerto TCP es el 5000 del contenedor queda publicado como 5000 en la
computadora ejecutar si se quieere detener docker compose down.

## 2. Iniciar Cliente1

En la primera terminal de VS Code, ejecutar:

```bash
py cliente.py --name "Cliente 1" --host 127.0.0.1 --port 5000
```

## 3. Iniciar Cliente2

En una segunda terminal de VS Code, ejecutar:

```bash
py cliente.py --name "Cliente 2" --host 127.0.0.1 --port 5000
```

cualquier cliente puede esribir cuando quiera. no existe un turno como tal
un hilo resibe los mensajes miestras que el hilo que es como principal espara
una entrada por el teclado.

## 4. Demostracion de funcionamiento

1. Levantar el servidor con `docker compose up --build`.
2. Conectar Cliente 1 y escribir `Hola `.
3. Conectar Cliente 2 y escribir `hola`.
4. Verificar que ambos clientes reciben los mensajes enviados por el otro.
5. Escribir un mensaje en la terminal del servidor y comprobar que lo reciben
   los dos clientes.

como deberia verse

```text
[CLIENTE 1]: Hola
[CLIENTE 2]: hola
[SERVIDOR]: Mensaje recibido por todos
```

## Estructura

- `servidor.py`: servidor TCP, limite de dos clientes, broadcast e hilo de entrada.
- `cliente.py`: cliente con hilo receptor y envio desde la terminal.
- `Dockerfile`: imagen del servidor Python.
- `docker-compose.yml`: construccion en el puerto `5000`.
