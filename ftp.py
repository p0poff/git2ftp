import ftplib
import os

def chdir(path):
		os.chdir(path)

def curdir():
	return os.getcwd()

class ftp:
	def __init__(self, **args):
		setting = args['setting']
		self.url = 			setting.get('ftpUrl', 			'none')
		self.port =         int(setting.get('ftpPort',         21))
		self.folder = 		setting.get('ftpFolder', 		'none')
		self.activeMode = 	setting.get('ftpActiveMode', 	'none')
		self.login = 		setting.get('ftpLogin', 		'none')
		self.password = 	setting.get('ftpPassword', 		'none')
		self.gitPath = 		setting.get('gitPath', 		'none')
		self.files = args.get('files')

	def connect(self):
		print('connected...')
		try:
			self.ftp = ftplib.FTP()
			self.ftp.connect(self.url, self.port, timeout=30)
		except:
			self.ftp = None
			print('FTP connection is failed')
			return
		try:
			self.ftp.login(self.login, self.password)
			if self.activeMode==1:
				self.ftp.set_pasv(False)
			else:
				self.ftp.set_pasv(True)
		except:
			self.ftp = None
			print('login to FTP server wrong')
			return

	def quit(self):
		print('connect close')
		if self.ftp == None:
			pass
		else:
			self.ftp.quit()

	def upload(self):
		if len(self.files)==0:
			print('files count zero')
			return
		self.connect()
		if self.ftp==None:
			print('Upload is stopped')
			self.quit()
			return
		if self.setPath(self.folder)==False:
			self.quit()
			return
		for file in self.files:
			if self.changeDir(file)!=True:
				print('change directory failed')
				return
			if self.uploadFile(self.gitPath, file)!=True:
				print('dont upload %s on server' % (file))
		self.quit()

	def changeDir(self, path):
		self.setPath(self.folder)
		pieces = path.split('/')
		if len(pieces)==1:
			return True
		fullPath = self.folder
		for curDir in pieces[:-1]:
			fullPath += '/%s' % (curDir)
			if curDir in self.ftp.nlst():
				if self.setPath(fullPath)!=True:
					return False
			else:
				if self.createDir(fullPath)!=True:
					return False
				if self.setPath(curDir)!=True:
					return False
		return True


	def setPath(self, Path, callback=None):
		try:
			self.ftp.cwd(Path)
			return True
		except ftplib.error_perm: #no such directory 550 error
			if callback==None:
				print('no such dir')
				return False
			else:
				callback()
				return True
		except Exception as inst:
			print(inst.args[0])
			return False

	def createDir(self, nameDir):
		try:
			self.ftp.mkd(nameDir)
			return True
		except:
			print('dont create new dir')
			return False

	def uploadFile(self, path, filename):
		try:
			pieces = filename.split('/')
			if len(pieces)>1:
				filename = pieces[-1]
				path += '/'+'/'.join(pieces[:-1])
			print('upload file', path, filename)
			chdir(path)
			fh = open(filename, 'rb')
			self.ftp.storbinary('STOR %s' % (filename), fh)
			fh.close()
			return True
		except:
			return False
	