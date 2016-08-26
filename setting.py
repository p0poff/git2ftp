import json

class setting:
	def __init__(self):
		self.fileName = './setting.json'
		f = open(self.fileName, 'r')
		self.d = json.loads(f.read())

	def set(self, **args):
		self.d['gitPath'] = 		args.get('gitPath', 'none')
		self.d['ftpUrl'] = 			args.get('ftpUrl', 'none')
		self.d['ftpPort'] = 		args.get('ftpPort', '21')
		self.d['ftpFolder'] = 		args.get('ftpFolder', 'none')
		self.d['ftpActiveMode'] = 	args.get('ftpActiveMode', 'none')
		self.d['ftpLogin'] = 		args.get('ftpLogin', 'none')
		self.d['ftpPassword'] = 	args.get('ftpPassword', 'none')
		self.save()

	def get(self):
		return self.d

	def save(self):
		jD = json.dumps(self.d)
		f = open(self.fileName, 'w')
		f.write(jD)
		f.close()