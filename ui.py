from tkinter import *
import setting
import git
import ftp
class ui():
	def __init__(self):
		self.setting = setting.setting()
		self.curFiles = []

	def saveSetting(self):
		gitPath =  			self.entryGitPath.get()
		ftpUrl =  			self.entryFtpUrl.get()
		ftpPort =  			self.entryFtpPort.get()
		ftpFolder =  		self.entryFtpFolderPath.get()
		ftpActiveMode =  	self.activeMode.get()
		ftpLogin = 			self.login.get()
		ftpPassword = 		self.password.get()
		self.setting.set(gitPath=gitPath, ftpUrl=ftpUrl, ftpPort=ftpPort, ftpFolder=ftpFolder, ftpActiveMode=ftpActiveMode, ftpLogin=ftpLogin, ftpPassword=ftpPassword)
		self.lCommits = self.getCommits()

	def getCommits(self):
		try:
			dataSetting = self.dataSetting
		except:
			print('ERROR, not setting data')
		g = git.git(path=dataSetting['gitPath'])
		lCommits = g.getCommits()
		return lCommits

	def fillCommits(self):
		self.git_listbox.delete(0, END)
		if self.lCommits == None: return
		for x in self.lCommits: self.git_listbox.insert(END, x.commit)

	def getFiles(self, event):
		l = event.widget
		sel = l.curselection()
		files = []
		for x in sel:
			files += self.lCommits[x].files
		files = set([x[1] for x in files])
		return files

	def getFilesSelectCommits(self, event):
		self.curFiles = self.getFiles(event)
		self.showFilesInText(self.curFiles)

	def showFilesInText(self, files):
		self.text_files["state"] = "normal"
		self.text_files.delete(1.0, END)
		self.text_files.insert(1.0, '\n'.join(files))
		self.text_files["state"] = "disabled"

	def upload(self):
		f = ftp.ftp(setting=self.dataSetting, files=self.curFiles)
		f.upload()

	def run(self):
		root = Tk()
		root.title("git2ftp")
		root.geometry('500x500')

		frame1=Frame(root,width=500,heigh=100,bd=5)
		frame1.pack(fill="x", expand="True", side='top')

		frame2=Frame(root,width=500,heigh=150,bd=5)
		frame2.pack(fill="x", side='top')

		frame3=Frame(root,width=500,heigh=200,bd=5)
		frame3.pack(fill="both", expand="True", side='top')

		frame4=Frame(root,width=500,heigh=50,bd=5)
		frame4.pack(fill="x", side='top')

		frame_inside1=Frame(frame1)
		frame_inside1.pack(fill="x", side='top')

		frame_inside2=Frame(frame1)
		frame_inside2.pack(fill="y", side='top')
		
		frame_inside4=Frame(frame1)
		frame_inside4.pack(fill="y", side='top')

		frame_inside3=Frame(frame1)
		frame_inside3.pack(fill="y", side='top')

		label1=Label(frame_inside1, text=u'Setting')
		label1.pack(side="left")

		label2=Label(frame_inside2, text=u'GIT path: ')
		label2.pack(side="left")
		self.entryGitPath = Entry(frame_inside2, width='17')
		self.entryGitPath.pack(side='left')

		label3=Label(frame_inside2, text=u' FTP url: ')
		label3.pack(side="left")
		self.entryFtpUrl = Entry(frame_inside2, width='15')
		self.entryFtpUrl.pack(side='left')

		label4=Label(frame_inside2, text=u' FTP port: ')
		label4.pack(side="left")
		self.entryFtpPort = Entry(frame_inside2, width='3')
		self.entryFtpPort.pack(side='left')
		
		label6=Label(frame_inside4, text=u' login: ')
		label6.pack(side="left")
		self.login = Entry(frame_inside4, width='20')
		self.login.pack(side='left')

		label7=Label(frame_inside4, text=u' pass: ')
		label7.pack(side="left")
		self.password = Entry(frame_inside4, width='20')
		self.password.pack(side='left')

		label5=Label(frame_inside3, text=u' FTP folder path: ')
		label5.pack(side="left")
		self.entryFtpFolderPath = Entry(frame_inside3, width='20')
		self.entryFtpFolderPath.pack(side='left')

		self.activeMode = IntVar()
		self.checkActive=Checkbutton(frame_inside3, text=u' Active mode ', variable=self.activeMode, onvalue=1, offvalue=0)
		self.checkActive.pack(side="left")

		buttonSave=Button(frame_inside3,text=u'save',command=self.saveSetting)
		buttonSave.pack(side="right")

		self.git_listbox=Listbox(frame2,height=10,width=100,selectmode=EXTENDED)
		self.git_listbox.pack(side="top")
		self.git_listbox.bind("<<ListboxSelect>>", self.getFilesSelectCommits)

		self.text_files=Text(frame3,height=12,width=100, state=DISABLED)
		self.text_files.pack()

		button1=Button(frame4,text=u'SEND', command=self.upload)
		button1.pack(side="right")

		button2=Button(frame4,text=u'reload',command=self.fillCommits)
		button2.pack(side="right")

		#*********************************************
		self.dataSetting = self.setting.get()
		self.entryGitPath.insert(0, self.dataSetting['gitPath'])
		self.entryFtpUrl.insert(0, self.dataSetting['ftpUrl'])
		self.entryFtpPort.insert(0, self.dataSetting['ftpPort'])
		self.login.insert(0, self.dataSetting['ftpLogin'])
		self.password.insert(0, self.dataSetting['ftpPassword'])
		self.entryFtpFolderPath.insert(0, self.dataSetting['ftpFolder'])
		self.activeMode.set(self.dataSetting['ftpActiveMode'])

		self.lCommits = self.getCommits()
		self.fillCommits()

		root.mainloop()