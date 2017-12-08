import socket


number_process = 3


ips = ['localhost','localhost','localhost']
ports = [5005, 5006, 5007]

class process:
	clock
	time_stamp
	state = "released"
	num_process

	def __init__(self):
    	self.clock = 0

	def set_num_preocess(self, num_process):
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
		tup1 = ("wanted", number_process, t)
		for i in range(0,self.num_process-1):
			if i == self.num_process:
				continue
			addr = (('127.0.0.1',ports[i])) 
			client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
			client_socket.connect(addr)

			client_socket.send(bytes(tup1))
			state = client_socket.recv(1024)
			if state[0]  == "held"
				return False;
			else if state[0] == "wanted" and  
			client_socket.close()
		return True

	def enter_critical_region(self):
		self.state = "wanted"
		t = random.radint()
		if make_request(self.num_process, t)  == True : 
			state = "held"
			



