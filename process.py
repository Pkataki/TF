import socket
import time
import random
import threading
from Queue import *



adjectives = ["hard",
		"boundless",
		"shrill",
		"bashful",
		"opposite",
		"fluffy",
		"dear",
		"astonishing",
		"eight",
		"sick",
		"placid",
		"ad hoc",
		"ambiguous",
		"irate",
		"ordinary",
		"numerous",
		"brawny",
		"harsh",
		"calm",
		"jumbled" 
]

nouns = ["snails",
		"believe",
		"apparatus",
		"horn",
		"eggs",
		"desire",
		"snail",
		"fireman",
		"pets",
		"stocking",
		"curtain",
		"prose",
		"doctor",
		"expansion",
		"fish",
		"hammer",
		"tail",
		"profit",
		"grip",
		"regret"
];
verbs = ["lock",
		"apologise",
		"knock",
		"advise",
		"scatter",
		"nest",
		"bomb",
		"roll",
		"decorate",
		"memorise",
		"name",
		"store",
		"harass",
		"remain",
		"last",
		"hop",
		"yell",
		"mug",
		"object",
		"weigh"
]

ponctuation =[ "?", "!" ,".", "...!"]


number_process = 3

ports = [7876, 7877, 7878]

buffer_port = 7706


class process():
	time_stamp = 0
	state = "released"
	num_process = 0
	q  = []
	sentence = ""
	type_client = ""
	mutex = threading.Lock()  

	def __init__(self):
		self.clock = 0
		self.q = Queue()

	def set_num_process(self, num_process):
		self.num_process = num_process
		
	def get_state(self):
		return self.state

	def set_type_client(self,type_client):
		self.type_client = type_client
	
	def get_time_stamp(self):
		return self.time_stamp;
	
	def set_state(self, state):
		self.state = state
	
	def set_time_stamp(self, time_stamp):
		self.time_stamp = time_stamp

	def on_message_received (self , time_stamp):
		self.time_stamp = max (self.time_stamp + 1 , time_stamp + 1 )

	def produce(self):

		self.sentence = adjectives[random.randint(0, len(adjectives)-1)] + " "
		self.sentence += nouns[random.randint(0, len(nouns)-1)] + " "
		self.sentence += verbs[random.randint(0, len(verbs)-1)] + " "
		self.sentence += ponctuation[random.randint(0, len(ponctuation)-1)]

		addr = (('127.0.0.1',buffer_port))
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		client_socket.connect(addr)
		tup = (self.sentence , self.num_process)
		
		client_socket.send(bytes(tup))
		response = client_socket.recv(1024)
		if response == "success":
			print "\n\nProcess " + str(self.num_process) + " stored  " + self.sentence + " sucessfully"
		else : 	
			print "\n\nError: Process " + str(self.num_process) + " couldn't store  " + self.sentence + " on buffer"

	def consume(self):

		addr = (('127.0.0.1',buffer_port))
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		client_socket.connect(addr)
		
		self.sentece = "want a sentence"
		
		tup = (self.sentece, self.num_process)

		client_socket.send(bytes(tup))
		self.sentece = client_socket.recv(1024)

		if self.sentece != "empty buffer":
			print "\nProcess " + str(self.num_process) + " got the sentence:  " + self.sentence
		else :
			print "\n\nError: Process " + str(self.num_process) + " couldn't consume a sentece"

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
			time.sleep(5)
			print "Process " + str(self.num_process) + " has the timestamp: " + str(self.time_stamp)  
			self.state = "wanted"
			if self.make_request(self.time_stamp)  == True : 
				self.state = "held"
			
				#inside critical region
				print "Process " + str(self.num_process) + " is in critical region"
				if self.type_client == "producer":
					self.produce()
				else:
					self.consume()
				print "Process " + str(self.num_process) + " is out of critical region"
				#out of critical region
				
				
				tup1 = (self.state, self.num_process, self.time_stamp)
				self.mutex.acquire()
				self.state = "released"
				while self.q.qsize() > 0:
					pro = self.q.get()
					addr = (('127.0.0.1',ports[pro[1]])) 
					client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
					client_socket.connect(addr)	
					client_socket.send(bytes(tup1))
					state = eval(client_socket.recv(1024))
					client_socket.close()
					self.on_message_received ( pro[2])
				self.mutex.release()
				
			else:
				time.sleep(1)

	def listen_process(self):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		server_socket.bind(('', ports[self.num_process]))
		server_socket.listen(1)

		while True:	
			connection_socket, addr = server_socket.accept()
			s = connection_socket.recv(1024)
			if s == "":
				continue
			#print s + " **"
			tup1 = eval(s)
		
			tup2 = (self.state,self.num_process, self.time_stamp)
			if self.state == "held" or (self.state == "wanted" and self.time_stamp < tup1[2]):
				self.mutex.acquire()
				self.q.put(tup2) 
				self.mutex.release()
			else:
				connection_socket.send(bytes(tup1))
			
		connection_socket.close()

	def init_thread(self):
		t2 = threading.Thread(target=self.listen_process)
		t2.start()

	def begin_requests(self):
		t1 = threading.Thread(target=self.enter_critical_region)
		t1.start()


if __name__ == "__main__":
	print "opa"