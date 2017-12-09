import threading
import random
from socket import *

BUFFER_SIZE = 3
indexBuffer = -1

mutex = threading.Semaphore(1)
buffer = list(range(BUFFER_SIZE))	


def Produce(sentence):
	global BUFFER_SIZE, indexBuffer, mutex, buffer
	
	if indexBuffer == BUFFER_SIZE - 1:
		return "full buffer"
	else:
		indexBuffer += 1
		buffer[indexBuffer] = sentence
		return "success"	
	

def Consume ():
	global BUFFER_SIZE, indexBuffer, mutex, buffer
	if indexBuffer == -1:		
		return "empty buffer"
	else :
		indexBuffer -= 1
		
		return (buffer[indexBuffer+1] )
		

buffer_port = 7706
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', buffer_port))
serverSocket.listen(1)
print ('The server is ready to receive')
while 1:
    connectionSocket, addr = serverSocket.accept()
    tup = connectionSocket.recv(1024)
    sentence = ""
    message = eval(tup)
    mutex.acquire()


    print "****************************************\n"
    print "Process " + str(message[1]) + " entered in the buffer"
    if message[0] == "want a sentence":
    	sentence = Consume()
    	
    	if sentence == "empty buffer":
    		print "Error: Process " +str(message[1]) + " couldn't consume a sentece"
    	else:
    		print "Process " + str(message[1]) + " consumed the sentece: " + sentence
    else:
    	sentence = Produce(message[0])

    	if sentence == "full buffer":
    		print "\n\nError: Process " + str(message[1]) + " couldn't store  " + message[0]+ " on buffer"
    	else:
    		print "Process " + str(message[1]) + " produced the sentece: " + sentence
    connectionSocket.send(sentence)
    print "Process " + str(message[1]) + " left out the buffer"
    print "****************************************\n"
    mutex.release()
    

    connectionSocket.close()     