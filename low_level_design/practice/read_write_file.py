lines = []
with open('python_interface.py', 'r') as f:
    lines = f.readlines()

print(lines)

with open('test', 'a+') as f:
    f.write('new_val\n')