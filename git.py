from subprocess import Popen, PIPE

class commit:
	def __init__(self, data):
		self.files = []
		self.comment = ''
		self.parse(data)

	def parse(self, data):
		first = False
		second = False
		for item in data:
			if 		item[:6]=='commit': 	self.commit = item
			elif 	item[:7]=='Author:': 	self.author = item
			elif 	item[:5]=='Date:': 		self.date = item
			elif 	item[:2]=='A\t' or item[:2]=='M\t': self.files.append(item.split('\t'))

			if item == '':
				if first == False: first = True
				elif first == True: second = True

			if first == True and second == False: self.comment += item + ' '

class git:
	def __init__(self, **args):
		self.path = args['path'] + '/.git'

	def cut(self, data):
		l = []
		lCur = []
		for x in data:
			if x[:6]=='commit':
				if len(lCur)>0:
					l.append(lCur)
					lCur = []
			lCur.append(x)
		return l if len(l)>0 else None

	def getCommits(self):
		command = "git -C %s log -n 100 --name-status" % (self.path)
		res = Popen(command, shell=True, stdin=PIPE, stdout=PIPE).stdout.read()
		res = res.decode('utf-8').split('\n')
		print(res)
		try:
			return [commit(x) for x in self.cut(res)]
		except:
			return None

if __name__ == "__main__":
	g = git(path='~/work/python/git2ftp')
	print(g.getCommits())
