import subprocess
from os import system as sys

def create_u_con():
    process = subprocess.Popen(['docker', 'run', '-it', '--rm', '--detach', 'ubuntu_con'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)
    return(process.stdout.readline()[0:12:1])

def get_con_ip(con_id):
    process = subprocess.Popen(['docker', 'inspect', '-f', '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}',con_id], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)
    return(process.stdout.readline()[:-1])

def print_ping(con1,con2_ip):
    p = subprocess.Popen(['docker', 'exec', '-it', con1, 'ping','-c', '3', con2_ip], stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, shell=False)
    p.wait()
    print(p.stdout.read().decode())

#build image
subprocess.run("docker build -t ubuntu_con .")

con1 = create_u_con()
con2 = create_u_con()
subprocess.run("docker ps")

con1_ip = get_con_ip(con1)
con2_ip = get_con_ip(con2)

print('\n')
print("con1: ping -c 3 con2",'\n')
print_ping(con1,con2_ip)
print('\n')
print("con1: ping -c 3 con2",'\n')
print_ping(con2,con1_ip)

""" result = subprocess.run(['docker', 'exec', '-it', con1, 'ping','-c', '3', con2_ip],capture_output=True)
print(str(result.stdout))
print('\n')
print("con2: ping -c 3 con1",'\n')
result = subprocess.run(['docker', 'exec', '-it', con2, 'ping','-c', '3', con1_ip],capture_output=True)
print(str(result.stdout)) """

subprocess.run("docker stop "+con1)
subprocess.run("docker stop "+con2)