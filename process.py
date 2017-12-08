import socket
import time
import thread

number_process = 3

ips = ['localhost','localhost','localhost']
ports = [5005, 5006, 5007]
	

class process:
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
		t1 = threading.Thread(target=enter_critical_region)
		t2 = threading.Thread(target=listen_process)

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
			client_socket.send(bytes(tup1))
			state = eval(client_socket.recv(1024))
			if state[0]  == "held":
				return False; 
			client_socket.close()
		return True

	def enter_critical_region(self):
		while True:
			self.state = "wanted"
			t = random.radint()
			if make_request(self.num_process, t)  == True : 
				self.state = "held"
			#inside critical region
			sleep(5)
			#out of critical region
			self.state = "released"
			tup1 = (self.state, self.num_process, self.time_stamp)
			while q.qsize() > 0:
				pro = q.get()
				addr = (('127.0.0.1',ports[pro[1]])) 
				client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
				client_socket.connect(addr)
				client_socket.send(bytes(tup1))
				state = eval(client_socket.recv(1024))
	def listen_process(self):
		while True:
			connection_socket, addr = server_socket.accept()

			tup1 = eval(connection_socket.recv(1024))
			self.on_message_received ( tup1[2] )
			tup2 = (self.state,self.num_process, self.time_stamp)
			if self.state == "held" or (self.state == "wanted" and self.time_stamp < tup1[2]):
				q.put(tup2) 
			else:
				connection_socket.send(tup1)
			connection_socket.close()

if __name__ == "__main__":
	print "opa"