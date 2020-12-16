import telnetlib

HOST = "172.19.241.171"
user = "hadoop"
password = " "

def login():
  tn = telnetlib.Telnet(HOST)

  tn.read_until(b"login: ")
  tn.write(user.encode('ascii') + b"\n")
  if password:
      tn.read_until(b"Password: ")
      tn.write(password.encode('ascii') + b"\n")
      
  return tn

def get_connection():
  tn = login()
  print(tn.read_until(b'hadoop@Slave2:~$',1).decode('ascii'),end=' ')

  
  while True:
    cmd = input() + '\n'
    tn.write(cmd.encode('utf-8'))

    print(tn.read_until(b'hadoop@Slave2:~$',1).decode('ascii'),end=' ')

    if cmd == 'exit':
      break

if __name__ == "__main__":
    get_connection()