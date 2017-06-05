import requests
import urlparse
class User():
    paras =   { 'username': None,
                'passwd':None, 
                'passwd2': None,
                'email':None,
                'package':None,
                'ip':None }
    def __init__(self,username,passwd,passwd2,email,domain,package,ip):
        self.paras['username'] = username
        self.paras['passwd'] = passwd
        self.paras['passwd2'] = passwd2
        self.paras['email'] = email
        self.paras['package'] = package
        self.paras['ip'] = ip
        self.paras['domain'] = domain
    def get_paras(self):
        return self.paras

class DA():
    def __init__(self,ip,port,username,passwd):
        self.ip = ip
        self.port = port
        self.username = username
        self.passwd = passwd

    def query(self,cmd,paras=None):
        url = "http://%s:%s/%s" %(self.ip,self.port,cmd)
        data = requests.post(url, auth=(self.username,self.passwd),data=paras, verify=False).text
        if "error=1" in data:
            return data
        else:
            res = urlparse.parse_qs(data)
            return res['list[]']

    def listAll(self):
        return self.query("CMD_API_SHOW_ALL_USERS")      
          
    def createUser(self,user):
        paras = {'action':'create',
                 'add': 'Submit',
                 'notify': 'yes'}
        paras.update(user.get_paras())
        #print (paras)
        return self.query("CMD_API_ACCOUNT_USER", paras)
    
                


