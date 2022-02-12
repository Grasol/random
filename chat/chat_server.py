import ast
import socket
import sys
import threading

CONTENT_LENGTH = "Content-Length:"

DEBUG_MODE = True

class GlobalChat:
  def __init__(self):
    self.chat = []
    self.len = 0

  def append(self, msg):
    if type(msg) is str:    
      m = ast.literal_eval(msg)
      new_m = []
      new_m.append(m["user"])
      new_m.append(m["text"])
      
      self.chat.append(new_m)
      self.len = len(self.chat)

    print(self.chat)

  def build(self):
    res = ""
    for m in self.chat:
      user = m[0]
      text = m[1]
      res += f"<p class=\"chat_msg\" ><b>[{user}]</b>: {text}</p>"

    return res


global_chat = GlobalChat() 

def parserHTTP(http):
  data = http.split()
  verb = data[0]
  path = data[1]
  ver = data[2]

  header_fields = {}
  key = None
  arg = []
  for d in data[3:]:
    if d[-1] == ":":
      if len(arg) != 0:
        header_fields.setdefault(key, arg)
        arg = []

      key = d

    else:
      arg.append(d)

  else:
    if len(arg) != 0:
      header_fields.setdefault(key, arg)

  return header_fields, verb, path, ver

def returnHTTP(data="", status=200, status_text="OK", mime="text/plain; charset=utf-8", fmt="utf-8"):
  http = [f"HTTP/1.1 {status} {status_text}"]
  
  http += [f"Access-Control-Allow-Origin: *"]

  if len(data) != 0 and type(data) is str:
    http += [f"Content-Type: {mime}"]
    http += [f"Content-Length: {len(data.encode(fmt))}"]
    http += ["", data]

  else:
    http += ["\r\n"]

  return '\r\n'.join(http)

def sendAll(sock, txt, fmt="utf-8"):
  data = txt
  if type(data) not in (bytes, bytearray):
    data = data.encode(fmt)

  sock.sendall(data)

def recvAll(sock, max, fmt="utf-8"):
  data = b""
  while (n := (max - len(data))) > 0:
    data += sock.recv(n)
    if len(data) == 0:
      return False

  return str(data, fmt)

def recvUntil(sock, text, fmt="utf-8"):
  data = ""
  while text not in data:
    d = sock.recv(1).decode(fmt)
    if len(d) == 0:
      return False

    data += d

  return data

def handle_client(conn, tcp_addr, gen_addr):
  global global_chat
  if DEBUG_MODE: print(f"-- {tcp_addr} connected -- ", end='')

  header = recvUntil(conn, "\r\n\r\n")
  if not header:
    print(f"-- {tcp_addr} fatal, disconnected --")
    return 
    
  header, verb, path, ver = parserHTTP(header)
  if DEBUG_MODE: print(f"-- {tcp_addr} {verb} {path} {ver} --")

  data = ""
  if (CONTENT_LENGTH in header):
    max_b = int(header[CONTENT_LENGTH][0])
    if (max_b != 0):
      data = recvAll(conn, max_b)
      if data is False:
        print(f"-- {tcp_addr} fatal, disconnected --")
        return

  back_data = ""
  status = 200
  mime = "text/plain; charset=utf-8"

  match path:
    case "/msg":
      if len(data) != 0:
        global_chat.append(data)

      else:
        status = 400


    case "/len":
      back_data = str(global_chat.len)


    case "/chat":
      back_data = global_chat.build()
      mime = "text/html; charset=utf-8"

    case _:
      status = 400

  sendAll(conn, returnHTTP(data=back_data, status=status, mime=mime))

  conn.shutdown(socket.SHUT_RDWR)
  conn.close()

def main():
  argv = sys.argv
  argc = len(argv)
  
  host = socket.gethostbyname(socket.gethostname())
  port = 8080
  if argc >= 3:
    host = argv[1]
    port = int(argv[2])

  elif argc == 2:
    try:
      port = int(argv[1])

    except ValueError:
      host = argv[1]

  tcp_addr = (host, port)
  
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(tcp_addr)
  sock.listen()
  print(f"-- server on address: {tcp_addr} --")

  while True:
    conn, n_tcp_addr = sock.accept()
    th = threading.Thread(target=handle_client, args=(conn, n_tcp_addr, tcp_addr))
    th.start()


if __name__ == "__main__":
  main()