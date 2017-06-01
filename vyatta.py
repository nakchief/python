import  urllib2, time, warnings,argparse,sys
import requests, re
# Vyatta Configuration
vyatta_ip = '192.168.123.90'
auth=('username', 'password')
headers = {'Accept': 'application/json' , 'Vyatta-Specification-Version': '0.1' }
delimiter = "##############################"
id = ""
def start():
	print (delimiter)
	print ("Connecting to Vyatta")
	conf_url = 'https://%s/rest/conf' %vyatta_ip
	warnings.filterwarnings("ignore")
	r = requests.post(conf_url, auth=auth, headers=headers, verify=False)
	id = r.headers['location'].split('/')[2]
	conf_url = 'https://%s/rest/conf' %vyatta_ip
	requests.get(conf_url, auth=auth, headers=headers, verify=False)
	print ("Connection is established")
	print (delimiter)
	return id

def get_ip_file(file_path):
	list_ip = []
	count = 0
	with open(file_path) as f:
		mylist = f.read().splitlines()
		for line in mylist:
			if line.startswith(";") or line.startswith("#") or not line.strip():
				continue
			regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})(?:\/[\d]{1,2})?',line)
			if regex != []:
				list_ip.append(regex[0])
				count = count + 1
	print ("Path of file: %s\nTotal IP: %s"  %(file_path,count))
	return list_ip

def get_ip_url(url):
	start_time = time.time()
	print (delimiter)
	print ("Adding IP List from URL %s is processing.\nPlease wait!" %(url))
	list_ip = []
	count = 0
	for line in urllib2.urlopen(url):
		line = line.rstrip().decode("utf-8")
		if line.startswith(";") or line.startswith("#") or not line.strip():
			continue
		regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})(?:\/[\d]{1,2})?',line)
		if regex != []:
			count = count + 1
			list_ip.append(regex[0])
	elapsed_time = time.time() - start_time
	print ("Total IP: %s"  %(count))
	print ("Elapsed Time:%s seconds." %(elapsed_time))
	print (delimiter)
	return list_ip


def add_ip(list_ip,group_ip):
	global id
        id = start()
	start_time = time.time()
	print ("Adding IP List to Vyatta address-group %s is processing.\nPlease wait!" %(group_ip))
	for ip in list_ip:
		ip = ip.replace('/', '%2F')
		url = 'https://%s/rest/conf/%s/set/resources/group/address-group/%s/address/%s' %(vyatta_ip,id,group_ip,ip)
		requests.put(url, auth=auth, headers=headers, verify=False)        
	elapsed_time = time.time() - start_time
	print ("Elapsed Time:%s seconds." %(elapsed_time))

def commit():
	commit_url = 'https://%s/rest/conf/%s/commit' %(vyatta_ip,id)
	requests.post(commit_url, auth=auth, headers=headers, verify=False)
	return

def save():
	save_url = 'https://%s/rest/conf/%s/save' %(vyatta_ip,id)
	requests.post(save_url, auth=auth, headers=headers, verify=False)
	return

def exit():
	exit_url = 'https://%s/rest/conf/%s' %(vyatta_ip,id)
	requests.delete(exit_url, auth=auth, headers=headers, verify=False)
	return

# Get argruments
commandList = argparse.ArgumentParser(sys.argv[0])
commandList.add_argument('-f', '--file',
                  action="store",
                  dest="filepath",
                  help="Path of file",
                  )
commandList.add_argument('-u', '--url',
                  action="store",
                  dest="url",
                  help="Insert URL",
                  )
commandList.add_argument('-g', '--group',
                  action="store",
		  dest="group",
                  help="Name of Vyatta address-group",
                  )
options = commandList.parse_args()
if options.filepath and not  options.url and options.group:
	list_ip = get_ip_file(options.filepath)
	add_ip(list_ip,options.group)

elif not options.filepath and options.url and options.group:
	list_ip = get_ip_url(options.url)
	add_ip(list_ip,options.group)
else:
	commandList.print_help()
	sys.exit(1)	

commit()
exit()
