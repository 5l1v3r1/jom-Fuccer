# Joomla! Plugins/Exploits Auto-Updating Scanner 
# Author: @D35m0nd142, <d35m0nd142@gmail.com>
# Official Repository: https://github.com/D35m0nd142/Joomla-Components-Exploits-Auto-Updating-Scanner

# This is a simple auto-updating Joomla! Plugins Scanner which is able to find exploits related to previously found components. 
# It uses the csv file provided by the Exploit-DB team and an extra plugins' list from Metasploit, but it is totally indipendent from this last one. 
# TOR Proxy tunnel is available.

# [FLOODING] If the target is protected by flooding requests the script won't be successful clearly.

# Script's Programming Language support: Python 2.7.* 

# *******************************************************************************************************************************************
# WARNING: You could have not installed some of the required libraries but it will install them for you PROVIDED you run the script as root.
#      	   Besides you need to install pip in order to get missing libraries quickly.
# *******************************************************************************************************************************************
#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv
import sys
import time
import urllib

try:
	import requests
except ImportError:
	print "[!] 'requests' library not found. Installing it automatically using pip.."
	time.sleep(0.5)
	os.system("pip install requests")
	import requests

import codecs

try:
	import socks
except ImportError:
	print "[!] socks.pyc not found. Downloading it automatically.."
	time.sleep(0.5)
	urllib.urlretrieve ("https://github.com/alyssafrazee/randomcalendars/blob/master/httplib2/socks.pyc?raw=true", "socks.pyc")
	import socks
	
import socket

try:
	import shutil
except ImportError:
	print "[!] 'shutil' library not found. Installing it automatically using pip.."
	time.sleep(0.5)
	os.system("pip install shutil")
	import shutil

import urllib2
import argparse

try:
	from termcolor import colored
except ImportError:
	print "[!] 'termcolor' library not found. Installing it automatically using pip.."
	time.sleep(0.5)
	os.system("pip install termcolor")
	from termcolor import colored

useTor   = False
Update   = True
tor_port = 9150
tor_addr = "127.0.0.1"
compFile = "comptotest.txt"
expFile  = "exp-db_files.csv"
csvURL = "https://raw.githubusercontent.com/offensive-security/exploit-database/master/files.csv"
metasploitURL = "https://raw.githubusercontent.com/rapid7/metasploit-framework/master/data/wordlists/joomla.txt"
found = []

def getComponents():
	global found

	with open(expFile,"r") as f:
		for line in f:
			if("com_" in line and "Joomla" in line):
				split = line.split(" ")
				for w in split:
					w = w.strip()
					if((w.startswith("com_") or w.startswith("'com_")) and w not in found):
						if(w[0] == '\''):
							w = w[1:len(w)-1]
						found.append(w)
						break

	found = set(found)
	of = open(compFile,"w")
	i = 0
	for f in found:
		i += 1
		print "[%s] %s" %(i,f)
		of.write(f+"\n")
	of.close()

def getExploitDbList():
	response = urllib2.urlopen(csvURL)
	of = open(expFile,"w")
	cr = csv.reader(response)
	for row in cr:
		of.write(str(row)+"\n")
	of.close()

def getMetasploitList():
	global found

	try:
		response = requests.get(metasploitURL).text
	except:
		return
		
	nlsplit = response.split("\n")
	for s in nlsplit:
		if("com_" in s):
			start = s.find('com_') 
			compToAdd = ""
			for x in range(start,len(s)):
				if(CharOrNumber(s[x])):
					compToAdd = "%s%s" %(compToAdd,s[x])
				else:
					break
			found.append(compToAdd)

def CharOrNumber(c):
	if(c.isalpha() or str(c).isdigit() or c == '_'):
		return True
	return False

def extractExploits(foundComp):
	exploits = []

	with open(expFile,"r") as f:
		for line in f:
			for comp in foundComp:
				if(comp in line and "Joomla" in line and CharOrNumber(line[line.find(comp)+len(comp)]) is False):
					exploits.append(line.strip())

	exploits = set(exploits)
	return exploits

def checkTor(inp):
	global tor_addr
	global tor_port

	if(":" not in inp and "." not in inp):
		print "\n[!] Invalid TOR proxy syntax (it must be 'tor_addr:tor_port'). Using '%s:%s' as default." %(tor_addr,tor_port)
		time.sleep(1)
		return 

	split = inp.split(":")
	tor_addr = split[0]
	tor_port = split[1]


print "\nJoomla! Components/Exploits Auto-Updating Scanner"
print "Author: Elb4Ron, <Zokomk69@outlook.fr>\n"
print " \n"
print "              ``;`                         "    
print "           `,+@@@+                         "    
print "         .+@@@@@@@;                        "    
print "      `;@@@@@@@@@@@                        "    
print "     +@@@@@@@@@@@@@:                       "    
print "   ;@@@@@@@@@@@@@@@@                       "    
print " `@@@@@@@@@@@@@@@@@@`                      "    
print " `@@@@@@@@@@@@@@@@@@#                      "    
print "  .@@@@@@@@@@@@@@@@@@,                     "    
print "    :@@@@@@@@@@@@@@@@@@      .'@@           "    
print "    #@@@@@@@@@@@@@@@@+;  .+@@@@@            "    
print "     `@@@@@@@@@@@@@#;;+@+#@@@#:`            "    
print "      #@@@@@@@@@@';'@@@@@@@:`               "    
print "      `@@@@@@@+;;+@@@@@##`                  "    
print "       .@@@#;;+@@@@@#+',.,'.                "    
print "       +;;'#@@@@#+;`      ,:                "    
print "        .#@@@@#++:  @.    ...`             "    
print "     `'@@@@#++'. +  .#++;;+  +             "    
print "  ,@@@@@#++:``::+   `',:+,. ,              "    
print " `@@@@#, #+` ',.`'.   +` ``  `,  .+         "    
print "  @@:`  ,+. ,`:``.:   '. .',+++   #           "  
print "  ``    #+`++,.`:,``    :`+@@'@@@@'    ````   "  
print "        #'`#+:`.,`:` .@@@+@#  +`.      :  `:   *** CLayTeam*** "
print "        #:: +.`,.., `@@,#@':. +        :   '  "  
print "        #: ` ',:`,, @#``    + +        ' `,;  "  
print "        #: ` `:''`  @` #:.. , '        #+++:           Cod3D By ELB4Ron"  
print "        #: ,     ;#'#  + :   `:         #++   "  
print "        #; '     `''         ,          '.    " 
print "        ;' '                 #         `@#    "  
print "        #.;                ;`       ,#.:;     "
print "         `+;               '.        @   `    "  
print "          :#;            `@:        :`  `,   "  
print "           .#+;        `'+.'        +        "    
print "             .@++#'+@+@++` ;@.     '      "      
print "              `' ., ` #:`# `+.#+  :.   "        
print "               ., :  @#;.`;`:  `#@. "            
print "                +``,.;`@+,. '#     "            
print "                @' ' ;`@:+`#`;`    "              
print "               `#+  ,'`#  :.  '    "              
print "               ' #.  :`#` '`. +    "              
print "               # +.  .:+: :`. .    "              
print "              `, +,   ..+ '`   :  "              
print "              ;` #+@:,:#.;``   '  "              
print "              #'##:#+.  : `;   ;  "              
print "              #. #:      `'`   :  "              
print "                 #,        `   . \n"
time.sleep(0.7)

parser = argparse.ArgumentParser(description="")
parser.add_argument("--target", type=str, help="Enter the target to scan",required=True)
parser.add_argument("--tor_proxy", type=str, help="Enable the tool to use the TOR proxy",default="None")
parser.add_argument("--no_update",help="Disable the update from github. You need to provide your own comptotest.txt and exp-db_files.csv files",
	action='store_true',default=False)
args = parser.parse_args()

target = args.target

if(args.tor_proxy != "None"):
	checkTor(args.tor_proxy)

	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, tor_addr, tor_port)
	socket.socket = socks.socksocket

if("http" not in target[:4]):
	target = "http://%s" %target
if(target[len(target)-1] != '/'):
	target = "%s/" %target

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'}
toCheck = ["<h1>Not Found</h1>","<title> 404 - Page not found</title>","\"center error-404\""]
foundComp = []

if(args.no_update is False):
	print "Downloading Metasploit list.."
	getMetasploitList()
	print "Downloading Exploit-db csv list.."
	getExploitDbList()

	time.sleep(1) 
	print "\nUpdating Joomla! components.."
	getComponents()
	print ""

else:
	if(os.path.isfile("comptotest.txt") is False):
		print "\n[-] '%s' not found. You must provide a file containing the Joomla! components to scan for." %compFile
		compFile = raw_input("[*] Components List file -> ")
	if(os.path.isfile("exp-db_files.csv") is False):
		print "\n[-] '%s not found. You must provide a csv file containing the exploit-db list." %expFile
		expFile = raw_input("[*] Exploit-db list file -> ")

bad_resp = requests.get("%scomponents/impo5sIblexXxD35" %target).text
i = 0

with open(compFile,"r") as f:
	for line in f: 
		i += 1
		line = line.strip()
		if(len(line) > 0 and line != "com_"):
			print "[%s] Testing '%s'" %(i,line)
			url = "%scomponents/%s" %(target,line)	
			#print url
			try:
				r = requests.get(url,headers=headers,timeout=10)
				Valid = True
				for c in toCheck:
					if(c in r.text):
						Valid = False
						break
				if(r.status_code != 404 and Valid and (r.url == url or r.url == "%s/" %url) 
					and len(r.text) < 5000 and r.text != bad_resp):
					foundComp.append(line)
					print "%s [FOUND]" %line
			except:
				pass

print "\nJoomla! components found [%s]: \n" %len(foundComp)
print "----------------------------"
for comp in foundComp:
	print comp
print "----------------------------\n"

exploits = extractExploits(foundComp)
print "\nJoomla! exploits found [%s]: \n" %len(exploits)

for comp in foundComp:
	print colored("\n%s:\n" %comp,"red")
	for exp in exploits:
		if(comp in exp):
			split = exp.split(",")
			code = split[1].split("/")
			code = code[len(code)-1].split(".")[0]
			output = "%s  [https://www.exploit-db.com/exploits/%s/]" %(split[2],code)
			print '-' * len(output) 
			print output
			print '-' * len(output)

if(len(foundComp) == 0):
	print "\n[-] Probably the website has some kind of Flooding protection or it redirects all the requests we send to /components!"

print ""
 
if(Update):
	os.remove("%s" %compFile)
	os.remove("%s" %expFile)