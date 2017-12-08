import socket
import time
import random
import threading
from Queue import *

number_process = 3

ports = [7802, 7803, 7820]
	

class process():
	clock = 0
	time_stamp = 0
	state = "released"
	num_process = 0
	q  = []
	t1 = 0
	t2 = 0
	mutex = threading.Lock()  

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
		self.time_stamp = max (self.clock + 1 , time_stamp + 1 )

	def make_request(self, t):

		tup1 = ("wanted", self.num_process, t)
		for i in range(0,number_process-1):
			if i == self.num_process:
				continue
			addr = (('127.0.0.1',ports[i])) 
			client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
			client_socket.connect(addr)
			client_socket.send(bytes(tup1))
			s = client_socket.recv(1024)

			if s == "":
				return False

			state = eval(s)
			
			if state[0]  == "held":
				return False 

			client_socket.close()
		return True

	def enter_critical_region(self):

		
		while True:
			self.state = "wanted"
			if self.make_request(self.time_stamp)  == True : 
				self.state = "held"
			#inside critical region
			print "Process " + str(self.num_process) + " is in critical region"
			time.sleep(3)
			print "Process " + str(self.num_process) + " is out of critical region"
			#out of critical region
			self.state = "released"
			tup1 = (self.state, self.num_process, self.time_stamp)
			self.mutex.acquire()
			while self.q.qsize() > 0:
				pro = self.q.get()
				addr = (('127.0.0.1',ports[pro[1]])) 
				client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
				client_socket.connect(addr)	
				client_socket.send(bytes(tup1))
				state = eval(client_socket.recv(1024))
				client_socket.close()
			self.mutex.release()

	def listen_process(self):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		server_socket.bind(('', ports[self.num_process]))
		server_socket.listen(15)
		while True:	
			connection_socket, addr = server_socket.accept()
			s = connection_socket.recv(1024)
			
			if s == "":
				continue
			#print s + " **"
			tup1 = eval(s)
			self.on_message_received ( tup1[2] )
			tup2 = (self.state,self.num_process, self.time_stamp)
			if self.state == "held" or (self.state == "wanted" and self.time_stamp < tup1[2]):
				self.mutex.acquire()
				self.q.put(tup2) 
				self.mutex.release()
			else:
				connection_socket.send(bytes(tup1))
			##connection_socket.close()
		connection_socket.close()

	def init_thread(self):
		t2 = threading.Thread(target=self.listen_process)
		t2.start()

	def begin_requests(self):
		t1 = threading.Thread(target=self.enter_critical_region)
		t1.start()


if __name__ == "__main__":
	print "opa"