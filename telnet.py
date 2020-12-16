import telnetlib



class Telnet:
  test_user = "hadoop"
  test_passwd = "0"

  HOST = "172.19.241.171"
  
  R = ''
  S1 = ''
  S2 = ''
  S3 = ''

  tn = None

  def __init__(self) -> None:
      super().__init__()
      # self.tn = self.login(self.HOST, self.test_user, self.test_passwd)

  def get_tn(self):
    return self.tn

  def login(self,ip, user, passwd):
    self.tn = telnetlib.Telnet(self.HOST)

    self.tn.read_until(b"login: ")
    self.tn.write(user.encode('ascii') + b"\n")
    if passwd:
        self.tn.read_until(b"Password: ")
        self.tn.write(passwd.encode('ascii') + b"\n")
        
    return self.tn

  def get_connection(self):
    tn = self.login(1,"hadoop",'0')
    print(tn.read_until(b'hadoop@Slave2:~$',1).decode('ascii'),end=' ')

    
    while True:
      cmd = input() + '\n'
      tn.write(cmd.encode('utf-8'))

      print(tn.read_until(b'hadoop@Slave2:~$',1).decode('ascii'),end=' ')

      if cmd == 'exit':
        break

if __name__ == "__main__":
    TN = Telnet()
    TN.get_connection()