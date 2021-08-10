import json

class tst():
    def __init__(self, v):
        self.value = v

    def a(self, tmp):
        print(self.value)

def a():
    print('a()')

t = tst('tst.a()')
b = tst('tst.a() 2')

refs = {
    'r1': a,
    'r2': t.a,
    'r3': b.a
}

print(refs)
refs['r2'](1)
refs['r3'](4)