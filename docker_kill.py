import os

os.system("docker ps -a > temp.txt")

containers = []
images = []
with open("temp.txt", 'r') as f:
    for line in f:
        containers.append(line.split()[0])

for container in containers:
    os.system(f"docker stop {container}")
    os.system(f"docker rm {container}")

os.system("docker images > temp2.txt")

with open("temp2.txt", 'r') as f:
    for line in f:
        if line.split()[0] == '<none>':
            images.append(line.split()[2])

for image in images:
    os.system(f"docker image rm {image}")

os.remove("temp.txt")
os.remove("temp2.txt")
