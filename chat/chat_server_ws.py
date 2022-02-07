
import socket
import websockets
import asyncio
import sys


async def client_handle(ws, path):
  print(f"-- {ws.host}:{ws.port} connected --")
  async for msg in ws:
    print(msg)



def main():
  argv = sys.argv
  argc = len(argv)
  if argc >= 3:
    host = argv[1]
    port = int(argv[2])

  else:
    host = socket.gethostbyname(socket.gethostname())
    port = 8080

  ws = websockets.serve(client_handle, host, port)
  print(f"-- server on address: {host}:{port} --")

  asyncio.get_event_loop().run_until_complete(ws)
  asyncio.get_event_loop().run_forever()








if __name__ == "__main__":
  main()