import socket
import threading
import time

class countingSemaphore:
	def __init__(self,count):
		self.count = count
		self.lock = threading.Lock()
		self.condition = threading.Condition(self.lock)
		
	def aquire(self):
		with self.condition:           #self.condition.acquire
			while(self.count==0):
				self.condition.wait()
			self.count-=1
	
	def release(self):
		with self.condition:
			self.count+=1
			self.condition.notify()

def scanning(ip,port):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		try:
			sock.settimeout(0.5)
			if(sock.connect_ex((ip, port)) == 0):
				try:
					servName = socket.getservbyport(port,"tcp") 
				except:
					servName = "unknown"	
				print(f"{port}\t{servName}\topen\n")
		except Exception as e:
			print(f"{port}\t\tError:{e}")
					
ip = input("Enter the ip address you wnat to scan")
semaphore = countingSemaphore(1000)

print("PORTNO\tSERVICENAME\tSTATUS\n")

threads = []
start_time = time.time()
for port in range(0,65535):
	t = threading.Thread(target=scanning, args=(ip,port,))
	threads.append(t)
	t.start()

for t in threads:
	t.join()
end_time = time.time()

print(f"scanned in {end_time-start_time:.2f} seconds")



'''for i in range(0, 1024):
	with socket.socket(AF_INET,SOCK_STREAM) as sock:
		sock.settimeout(0.5)
		if(sock.connect_ex((ip,i)) == 0):
			print(f"port {i} is open\n")'''
