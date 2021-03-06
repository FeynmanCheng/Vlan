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

  host_ip_dict = {'T':T,'R':R,'S1':S1,'S2':S2,'S3':S3}

  ip_tn_dict = {}

  def __init__(self) -> None:
      super().__init__()

  def get_tn(self,ip):
    return self.ip_tn_dict[ip]       

  def login_no_passwd(self, hostname):

    if hostname == 'T':
      return self.login_with_passwd(hostname, self.test_user, self.test_passwd)
    
    ip = self.get_ip_by_hostname(hostname)

    user = self.user
    passwd = self.passwd
    return self.__login(ip, user, passwd)

  def login_with_passwd(self, hostname, user, passwd):
    ip = self.get_ip_by_hostname(hostname)
    return self.__login(ip, user, passwd)


  def __login(self,ip, user, passwd):
    print("logging into " + ip)

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
    tn.close()
    return tn.read_all().decode('ascii')

  def run_cmd(self,hostname,cmd):
    cmd += '\n'
    ip = self.get_ip_by_hostname(hostname)
    tn = self.get_tn(ip)
    tn.write(cmd.encode('utf-8'))

    resp = tn.read_until(b'#',1).decode('ascii')
    
    return resp

  def run_cmds(self, hostname, cmds):
    output = ''
       
    for cmd in cmds:
      try:
        output += self.run_cmd(hostname,cmd)
      except :
        print("Command: " + cmd + " Failed")
        return output, -1


    return output,0
    


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


  def get_ip_by_hostname(self, hostname):
    return self.host_ip_dict[hostname]

  def config(self, hostname):
    if hostname == 'R':
      return self.config_R()
    elif hostname == 'S1':
      return self.config_S1()
    elif hostname == 'S2':
      return self.config_S2()
    elif hostname == 'S3':
      return self.config_S3()
    elif hostname == 'T':
      return self.config_T()
    else:
      return 'Wrong Hostname',-1

  def config_S1(self):
    commands = []
    with open('./scripts/S1.txt') as f:
      commands = f.readlines()
      commands = [i.split('\n')[0] for i in commands]

    return self.run_cmds('S1', commands)
    

  def config_S2(self):
    commands = []
    with open('./scripts/S2.txt') as f:
      commands = f.readlines()
      commands = [i.split('\n')[0] for i in commands]

    return self.run_cmds('S2', commands)

  
  def config_S3(self):
    commands = []
    with open('./scripts/S3.txt') as f:
      commands = f.readlines()
      commands = [i.split('\n')[0] for i in commands]

    return self.run_cmds('S3', commands)

  def config_R(self):
    commands = []
    with open('./scripts/R.txt') as f:
      commands = f.readlines()
      commands = [i.split('\n')[0] for i in commands]

    return self.run_cmds('R', commands)
  
  
  # Test
  def config_T(self):
    self.login_no_passwd('T')

    commands = [
      'ls',
      'cd /',
      'ls'
    ]

    return self.run_cmds('T', commands)


if __name__ == "__main__":
    TN = Telnet()
    # TN.test()
    output, code = TN.config_T()
    print(output)
