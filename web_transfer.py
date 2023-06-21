import socket
from os import path
from tkinter import filedialog


file_dir = filedialog.askopenfilename()


def handle(conn):
	data = b''
	while True:
		d = conn.recv(16384)
		if not d:
			conn.close()
			return
		data += d
		if b'\r\n\r\n' in data:
			break
	# print(data)
	filename = file_dir.split("/")[-1:][0]
	res = f'HTTP/1.1 200 OK\r\nContent-Disposition: attachment; filename="{filename}"\r\nContent-Length: {path.getsize(file_dir)}\r\nContent-Type: application/octet-stream\r\nConnection: close\r\n\r\n'
	conn.send(bytes(res, encoding='utf-8'))

	with open(file_dir,'rb') as f:
		while True:
			chunk = f.read(16384)
			if not chunk:
				break
			conn.sendall(chunk)
	print('Transfer completed successfully.')
	conn.close()


def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('0.0.0.0', 11711))
	s.listen()
	print('\n>> listening at 0.0.0.0:11711\n\n')
	while True:
		try:
			conn, addr = s.accept()
			print(f'New connection >> {addr[0]}:{addr[1]}')
			handle(conn)
		except Exception as e:
			print(e)



if __name__ == '__main__':
	main()
