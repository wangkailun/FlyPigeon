#!/usr/bin/evn python
#_*_coding:"utf-8"_*_

#接收客户端的数据并回复
import socket  , socketserver ,os , struct
from tkinter import *
import _thread
import time

class Server:
	def __init__(self):
		self.window = Tk()
		self.window.title("飞鸽服务器端")
		self.frame1 = Frame(self.window)
		self.frame1.pack()
		self.text = Text(self.frame1)
		self.text.pack()
		self.text.config(bd = 4 , relief =RIDGE)
		self.MSG = StringVar()
		self.entry = Entry(self.frame1 , textvariable = self.MSG)
		self.entry.pack(side = LEFT , expand = True , fill = BOTH)
		self.entry.config(bd = 4 , relief = GROOVE)
		self.button = Button(self.frame1 , text = "发送" , command = self.SendMessage)
		self.button.pack(side = RIGHT)
		self.button.config(bd = 4 , relief = RAISED)
		self.button2 = Button(self.frame1 , text = "接收文件" , command = self.ReceiveFile)
		self.button2.pack(fill = BOTH)
		self.button2.config(bd = 4 , relief = RAISED)

	def ReceiveFile(self):
		BindIP = ''
		BindPort = 50002

		self.s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
		self.s.bind((BindIP , BindPort))
		self.s.listen(1)

		while True:
			self.connection , self.IPaddress = self.s.accept()
			self.text.tag_config('a',foreground = "green")
			self.text.insert(INSERT , "服务器 * * * * "+a+" * * * * *\n" , "a")
			self.text.insert(INSERT , "   连接成功\n")
			fileinfo_size = struct.calcsize("128sl")

			buf = self.connection.recv(fileinfo_size)
			if buf:
				filename , filesize = struct.unpack("128sl" , buf)
				filename_f = filename.strip('\00')
				filenewname = os.path.join('e:\\' ,('new_'+filename_f))

				recvd_sized = 0

				file = open(filenewname , "wb")
				self.text.insert(INSERT , "服务器 * * * * "+a+" * * * * *\n" , "a")
				self.text.insert(INSERT , "   开始传输文件\n")
				while recvd_sized != filesize:
					if filesize - recvd_sized > 1024:
						rdata = self.connection.recv(1024)
						recvd_sized += len(rdata)
						
					else:
						rdata = self.connection.recv(filesize - recvd_sized)
						recvd_sized = filesize
					file.write(rdata)
				file.close()
				self.text.insert(INSERT , "服务器 * * * * "+a+" * * * * *\n" , "a")
				self.text.insert(INSERT , "   文件传输完毕！")
				self.connection.close()
				break


	def ReceiveMessage(self):
		BindIP = ''
		BindPort = 50001
		self.s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
		self.s.bind((BindIP , BindPort))
		self.s.listen(5)
		
		while True:
			self.connection ,self.IPaddress = self.s.accept()
			while True:
				self.data = self.connection.recv(1024).decode("utf8")
				if self.data == '':
					continue
				else:
					a =time.strftime("%H:%M:%S" , time.localtime())
					self.text.tag_config('a',foreground = "green")
					self.text.insert(INSERT , "客户端 * * * * "+a+" * * * * *\n",'a')
					self.text.insert(INSERT , "   "+self.data+"\n")

	def SendMessage(self):
		self.message = self.MSG.get()
		if self.message != '':
			a = time.strftime("%H:%M:%S" , time.localtime())
			self.text.tag_config('a',foreground = "green")
			self.text.insert(INSERT , "服务器 * * * * "+a+" * * * * *\n",'a')
			self.text.insert(INSERT,"   "+self.message+"\n")
			self.connection.send(self.message.encode("utf8"))
			self.entry.delete(0,END)
			
	def StartNewThread(self):
		_thread.start_new_thread(self.ReceiveMessage,())

	
def main():
	server = Server()
	server.StartNewThread()
	server.window.mainloop()
		
			
		
		

if __name__ == "__main__":
	main()