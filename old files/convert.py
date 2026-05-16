import os

model = open(os.path.join('old files','model.txt'))
new_vertices = ''

liz = model.readlines()
vertices = []
for line in liz:
     if line[0] == 'v':
        tring = line[2:len(line)-1]
        vertices.append(tring.split(' '))
for i in range(len(vertices)):
    for j in range(3):
        vertices[i][j] = float(vertices[i][j])

faces = []
for line in liz:
     if line[0] == 'f':
        tring = line[2:len(line)-1]
        faces.append(tring.split(' '))
for i in range(len(faces)):
    for j in range(3):
        faces[i][j] = int(faces[i][j])
    
        



model.close()

# new = open(os.path.join('old files','new.txt'),'w')
# for line in vertices:
#     new.write(f'{str(line)}, ')
# addntl = [
#     [0.313617, 2.98125, -0.08754],
#     [0.228728, 2.88333, -0.0638137],
#     [0.165279, 2.78542, -0.0460553]
# ] 
