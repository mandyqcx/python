'''
try:
    file = open('write_test.txt','w+')
    file.write('jfdksjfiafsgsdg')
    file.read(6)
finally:
    file.close()'''

'''
with open('write_test.txt','w+') as file:
    file.write('hellgjj')
    file.read(5)'''

'''
file=open('write_test.txt')
for i in range(3):
    print(str(i) + ': ' + file.readline(), end='')
file.close()'''

'''import pprint
pprint.pprint(open(r'F:\learnpython\python\PYbasic\test_file\write_test.txt').readlines())
'''

'''
file=open('write_test.txt')
lines=file.readlines()
print(lines)
file.close()


lines[1]='1234;\n'
file=open('write_test.txt','w+')
file.writelines(lines)
file.seek(0,0)
lines_b=file.readlines()
print(lines_b)
file.close()'''

'''
def process(string):
    print('processing:',string)

with open('write_test.txt') as f:
    for char in f.readlines():
        process(char)


with open('write_test.txt') as f:
    while True:
        char=f.read()
        if not char:
            break
        process(char)'''


import fileinput

def process(string):
    print('processing:',string)

for line in fileinput.input('write_test.txt'):
    process(line)







