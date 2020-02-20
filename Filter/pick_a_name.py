# -*- coding: utf-8 -*-

name_path = '/home/test/PycharmProjects/testScrapy/naming/naming.txt'

class Hanzi(object):
    # 甽-zhen4-8
    def __init__(self,format):
        self.char,pinyin,strokes=format.split('-')
        self.strokes = int(strokes[0])
        self.initial = pinyin[0]
        self.pinyin= pinyin[0:-1]
        self.final = pinyin[1:-1]
        self.tones = int(pinyin[-1])

    def __str__(self):
        return ("%s %s \n"%(self.char,self.pinyin))


class Rule(object):
    def flushToFile(self,hanzi_set):
        with open(self.get_file(),'w',encoding='utf-8') as fd:
            for hanzi in hanzi_set:
                fd.write(hanzi.__str__())


    def check(self,hanzi):
        assert isinstance(hanzi,Hanzi)
        if self.black_final(hanzi.final):
            return False
        if self.black_initial(hanzi.initial):
            return False
        if self.black_tones(hanzi.tones):
            return False
        if hanzi.strokes in self.get_stroke():
            return False

        return True

    def get_stroke(self):
        raise NotImplemented()

    def black_final(self,f):
        if f == 'iu':
            return True
        return  False

    def black_initial(self,i):
        if i == 'l':
            return True
        return False

    def black_tones(self,t):
        raise NotImplemented()
    def get_file(self):
        raise NotImplemented()

class MidRule(Rule):
    def get_stroke(self):
        return [8,18]

    def black_tones(self, t):
        if t < 3:
            return True
        return False

    def get_file(self):
        return  'mid.txt'

class LastRule(Rule):
    def get_stroke(self):
        return [3,13,13]

    def black_tones(self, t):
        if t >= 3:
            return True
        return False

    def get_file(self):
        return  'last.txt'

class Filter(object):
    def __init__(self,file):
        self.mid_rule = MidRule()
        self.last_rule = LastRule()
        self.file = file
        self.mid_set=[]
        self.last_set = []

    def start(self):
        with open(self.file,'r',encoding='utf-8') as fd:
            while True:
                line = fd.readline()
                if not line:
                    break

                hanzi = Hanzi(line)
                if self.mid_rule.check(hanzi):
                    self.mid_set.append(hanzi)
                elif self.last_rule.check(hanzi):
                    self.last_set.append(hanzi)
                else:
                    pass

        self.mid_rule.flushToFile(self.mid_set)
        self.last_rule.flushToFile(self.last_set)

filter = Filter(name_path)
filter.start()