import socket
import time
import random
import threading
from Queue import *

number_process = 3

ports = [7502, 7503, 7420]
	

class process():
	clock = 0
	time_stamp = 0
	state = "released"
	num_process = 0
	q  = []
	t1 = 0
	t2 = 0
	def __init__(self):
		self.clock = 0
		self.q = Queue()

	def set_num_process(self, num_process):
		self.num_process = num_process
		
	def get_state(self):
		return self.state
	
	def get_time_stamp(self):
		return self.time_stamp;
	
	def set_state(self, state):
		self.state = state
	
	def set_time_stamp(self, time_stamp):
		self.time_stamp = time_stamp

	def on_message_received (self , time_stamp):
		self.clock = max (self.clock + 1 , time_stamp + 1 )

	def make_request(self, t):

		tup1 = ("wanted", self.num_process, t)
		for i in range(0,number_process-1):
			if i == self.num_process:
				continue
			addr = (('127.0.0.1',ports[i])) 
			client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
			client_socket.connect(addr)
			client_socket.send(bytes(str(bytes(tup1))))
			s = client_socket.recv(1024)

			if s == "":
				continue

			state = eval(s)
			if state[0]  == "held":
				return False; 
			client_socket.close()
		return True

	def enter_critical_region(self):

		while True:
			
			self.state = "wanted"
			t = random.randint(0 ,number_process)
			if self.make_request(t)  == True : 
				self.state = "held"
			#inside critical region
			time.sleep(5)
			#out of critical region
			self.state = "released"
			tup1 = (self.state, self.num_process, self.time_stamp)
			while self.q.qsize() > 0:
				pro = self.q.get()
				addr = (('127.0.0.1',ports[pro[1]])) 
				client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
				client_socket.connect(addr)	
				client_socket.send(bytes(str(bytes(tup1))))
				state = eval(client_socket.recv(1024))

	def listen_process(self):

		while True:

			server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
			server_socket.bind(('', ports[self.num_process]))
			server_socket.listen(15)
			connection_socket, addr = server_socket.accept()
			s = connection_socket.recv(1024)
			if s == "":
				continue
			#print s + " **"
			tup1 = eval(s)
			self.on_message_received ( tup1[2] )
			tup2 = (self.state,self.num_process, self.time_stamp)
			if self.state == "held" or (self.state == "wanted" and self.time_stamp < tup1[2]):
				self.q.put(tup2) 
			else:
				connection_socket.send(tup1)
			connection_socket.close()

	def init_thread(self):
		t2 = threading.Thread(target=self.listen_process)
		t2.start()

	def begin_requests(self):
		t1 = threading.Thread(target=self.enter_critical_region)
		t1.start()


if __name__ == "__main__":
	print "opa"