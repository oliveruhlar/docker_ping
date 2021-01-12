from subprocess import PIPE, Popen, run

def create_u_con():
    process = Popen(['docker', 'run', '-dt', '--rm', '--detach', 'ubuntu_con'], 
                           stdout=PIPE,
                           universal_newlines=True)
    return(process.stdout.readline()[0:12:1])

def get_con_ip(con_id):
    process = Popen(['docker', 'inspect', '-f', '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}',con_id], 
                           stdout=PIPE,
                           universal_newlines=True)
    return(process.stdout.readline()[:-1])

def print_ping(con1,con2_ip):
    p = Popen(['docker', 'exec', con1, 'ping','-c', '3', con2_ip], 
            stdout=PIPE,
            stderr=PIPE,
            shell=False)
    p.wait()
    return(p.stdout.read().decode())

def print_ping2(con1,con2_ip):
    p = Popen(['docker', 'exec', con1, 'ping','-c', '3', con2_ip], 
                        stdout=PIPE,
                        shell=True)
    return p.communicate()[0]

#build image
run("docker build -t ubuntu_con .")

con1 = create_u_con()
con2 = create_u_con()
run("docker ps")

con1_ip = get_con_ip(con1)
con2_ip = get_con_ip(con2)
""" 
print('\n')
print("con1: ping -c 3 con2",'\n')
print(print_ping(con1,con2_ip))
print('\n')
print("con1: ping -c 3 con2",'\n')
print(print_ping(con2,con1_ip)) """



print('\n')
print("con1: ping -c 3 con2",'\n')
print(print_ping2(con1,con2_ip))
print('\n')
print("con1: ping -c 3 con2",'\n')
print(print_ping2(con2,con1_ip))



""" result = sys("docker exec -it "+ con1 + " ping -c 3 " + con2_ip)
print('\n')
result = sys("docker exec -it "+ con2 + " ping -c 3 " + con1_ip)
print(str(result.stdout)) """

run("docker stop "+con1)
run("docker stop "+con2)