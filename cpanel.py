import requests

class Whm():
    shadow = "/etc/shadow"
    def __init__(self,ip,port,username,passwd):
        self.username = username
        self.passwd = passwd
        self.ip = ip
        self.port = port

    def query(self,cmd,paras=None):
        url = "https://%s:%s/json-api/%s?api.version=1" %(self.ip,self.port,cmd)
        r = requests.get(url, auth=(self.username,self.passwd),data=paras,verify=False)
        return r.json()

    def listUser(self):
        data = self.query("listaccts")["data"]["acct"]
        with open(self.shadow) as f:
            mylist = f.read().splitlines()
            for i in data:
                for j in mylist:
                    acc = {}
                    secret = j.split(":")
                    if i["user"] == secret[0]:
                        i["pass"] = secret[1]
                        break    
        return data
    def listPkg(self):
        data =  self.query("listpkgs")["data"]["pkg"]
        return data
    
                


