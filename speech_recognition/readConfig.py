class config():
    def __init__(self):
        self.file = open("testfile.txt", "r+")
    def __del__(self):
        self.file.close()
    def appendData(self,text):
        self.file.write(text)
    def readData(self):
        return self.file.read()
    def getList(self):
        list = []
        list2 = []
        for x in self.readData().split(';'):
            list.append(x.split('->'))
        return list