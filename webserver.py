import socket
import re
import time
import multiprocessing


class Server():
    def __init__(self, host:str, port:int):
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 处理挥手问题
        pass
        self.host = host
        self.port = port
        self.addr = (host, port)
        self.tcp_server_socket.bind(self.addr)
        self.tcp_server_socket.listen(100) # accept 100 connections
        print('Listening on %s:%d ...' % (host, port))
        pass
        
    def serve_client(self, client_socket):
        data = client_socket.recv(1024).decode("utf-8")
        print(data)
        header = 'HTTP/1.1 200 ok'
        body = '<h1>hello</h1>'
        re_data = "{header}\r\n\r\n{body}".format(header=header, body=body)
        client_socket.send(re_data.encode('utf-8'))
        client_socket.close()

    def start(self):
        while True:
            client_socket, client_addr = self.tcp_server_socket.accept()
            p = multiprocessing.Process(target=self.serve_client, args=(client_socket,))
            p.start()
            client_socket.close()


def main():
    host, port = '127.0.0.1', 10086
    server = Server(host=host, port=port)
    server.start()


if __name__ == "__main__":
    main()
