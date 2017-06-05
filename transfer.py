import requests
auth = ( "root","!aLLg=Nw@y8XuGm" )
shadow = "/etc/shadow"
def api(fuction):
    url = "https://cpanelhn1.longvan.net:2087/json-api/%s?api.version=1" %fuction
    r = requests.get(url, auth=auth, verify=False)
    return r.json()
def getuser():
    data = api("listaccts")["data"]["acct"]
    with open(shadow) as f:
        mylist = f.read().splitlines()
        for i in data:
            for j in mylist:
                acc = {}
                secret = j.split(":")
                if i["user"] == secret[0]:
                    i["pass"] = secret[1]
                    break    
    return data
def getpkg():
    
print (getuser())
    
                


