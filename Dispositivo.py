class Dispositivo:

    def __init__(self, dict = {},nome = ''):
        self.dict = dict
        self.nome = nome

    def addOp(self,op,ret):
        self.dict[op] = ret

    def addDictOp(self,dict):
        self.dict.update(dict)

    def getOps(self):
        return self.dict.keys()

    def getDict(self):
        return self.dict