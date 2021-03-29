import weakref


class Objeto:
    def __del__(self):
        print('(BORRADO {})'.format(self))


objetos = []
ref = []
for i in range(3):
    objetos.append(Objeto)

# for obj in objetos:
#    ref = weakref.ref(obj)

#for obj in objetos:
#    print('obj1:', obj)

print("borrar")
for obj in objetos:
    del obj

for obj in objetos:
    print('obj1:', obj)

"""
print('obj2:', obj1)
print('ref2:', r1)
print('r()2:', r1())
print('deleting obj')
del obj1
print('r():', r1())
"""

print("FINI")
