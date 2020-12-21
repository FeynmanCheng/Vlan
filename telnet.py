import telnetlib



class Telnet:
  test_user = "hadoop"
  test_passwd = "0"

  user = "cisco"
  passwd = "cisco"

  T = "172.19.241.171" 

  R = '192.168.10.4'
  S1 = '192.168.10.1'
  S2 = '192.168.10.2'
  S3 = '192.168.10.3'

  host_ip = {'T':T,'R':R,'S1':S1,'S2':S2,'S3':S3}

  hosts = [T,R,S1,S2,S3]

  ip_tn_dict = {}

  def __init__(self) -> None:
      super().__init__()

  def get_tn(self,ip):
    return self.ip_tn_dict[ip]   


  def login_no_passwd(self, hostname):

    if hostname == 'T':
      return self.login_with_passwd(hostname, self.test_user, self.test_passwd)
    
    ip = self.host_ip[hostname]

    user = self.user
    passwd = self.passwd
    return self.login(ip, user, passwd)

  def login_with_passwd(self, hostname, user, passwd):
    ip = self.host_ip[hostname]
    return self.login(ip, user, passwd)


  def login(self,ip, user, passwd):
    print(ip)

    if ip in self.ip_tn_dict.keys():
      self.logout(ip)
      self.ip_tn_dict.pop(ip)

    try:
      tn = telnetlib.Telnet(ip, timeout= 3)
    except:
      return {'data': None},400
      

    output = tn.read_until(b":",1).decode('ascii')

    if 'Password' not in output:
      print('Server')
      tn.write(user.encode('ascii') + b"\n")
      
      tn.read_until(b":")
      tn.write(passwd.encode('ascii') + b"\n")
      
    else:
      print("Switcher and Router")
      tn.write(passwd.encode('ascii') + b'\n')
    
    if ip not in self.ip_tn_dict.keys():
        self.ip_tn_dict[ip] = tn


    return tn.read_until(b'$',1).decode('ascii')

  def logout(self,ip):

    tn = self.get_tn(ip)
    tn.write(b'exit\n')
    return tn.read_all().decode('ascii')

  def run_cmd(self,ip,cmd):
    cmd += '\n'
    tn = self.get_tn(ip)
    tn.write(cmd.encode('utf-8'))

    resp = tn.read_until(b'#',1).decode('ascii')
    
    return resp


  def test(self):
    msg = self.login_with_passwd('T',self.test_user,self.test_passwd)
    print(msg)
    tn = self.get_tn(self.T)
    print(tn.read_until(b'#',1).decode('ascii'),end=' ')

    
    while True:
      cmd = input() + '\n'
      tn.write(cmd.encode('utf-8'))

      print(tn.read_until(b'hadoop@Slave2:~$',1).decode('ascii'),end=' ')

      if cmd == 'exit':
        self.logout(self.T)
        break

  def enable(self, ip):
    self.run_cmd(ip, 'en')
    self.run_cmd(ip, self.passwd)



  

if __name__ == "__main__":
    TN = Telnet()
    TN.test()
