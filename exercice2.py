import socket
import math
import time
import base64

class IRC:
    def __init__(self, name, channel, server="irc.root-me.org", port=6667):
        self.irc_conn = None
        self.name = name
        self.port = port
        self.server = server
        self.channel = channel

    def connect(self):
        print("Connection to the server...")
        self.irc_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc_conn.connect((self.server, self.port))
        time.sleep(1)
        self.send_command("USER", f"{self.name} 0 * :python")
        self.send_command("NICK", f"{self.name}")

    def send_command(self, cmd, message):
        full_command = f"{cmd} {message}\r\n".encode("utf-8")
        print(full_command)
        self.irc_conn.send(full_command)

    def send_full_command(self, cmd):
        full_command = f"{cmd}\r\n".encode("utf-8")
        print(full_command)
        self.irc_conn.send(full_command)

    def get_response(self):
        time.sleep(1)
        return self.irc_conn.recv(8000).decode("utf-8")

    def join_channel(self):
        command = "JOIN"
        channel = self.channel
        self.send_command(command, channel)

    def send_private_message(self, who, message):
        command = f"PRIVMSG {who} {message}"
        self.send_full_command(command)


if __name__ == "__main__":
    client = IRC("trolilol", "#root-me_challenge")
    client.connect()
    time.sleep(1)
    client.send_full_command("")
    print(client.get_response())
    # Join challenge channel and send a message to Candy
    client.join_channel()
    print(client.get_response())
    client.send_private_message("Candy", "!ep2")
    response = client.get_response()
    print(response)
    # Splitting response
    response = response.split(":")
    response = response[-1].split("\r\n")
    answer = response[0]
    print(answer)
    answer = base64.b64decode(answer.encode('utf-8'))
    client.send_full_command(f"PRIVMSG Candy !ep2 -rep {answer}")
    print(client.get_response())


    while True:
        message = input("\nMessage to Candy\n>")
        if message == "QUIT":
            client.send_full_command(message)
            exit()
        client.send_full_command(message)
        print(client.get_response())

