#!/usr/bin/python3

import requests
import re
import sys
import ast
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(bcolors.FAIL + """\n\n
 ▄█     █▄     ▄████████ ▀█████████▄          ▄████████ ███▄▄▄▄   ███    █▄    ▄▄▄▄███▄▄▄▄   
███     ███   ███    ███   ███    ███        ███    ███ ███▀▀▀██▄ ███    ███ ▄██▀▀▀███▀▀▀██▄ 
███     ███   ███    █▀    ███    ███        ███    █▀  ███   ███ ███    ███ ███   ███   ███ 
███     ███  ▄███▄▄▄      ▄███▄▄▄██▀        ▄███▄▄▄     ███   ███ ███    ███ ███   ███   ███ 
███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀██▄       ▀▀███▀▀▀     ███   ███ ███    ███ ███   ███   ███ 
███     ███   ███    █▄    ███    ██▄        ███    █▄  ███   ███ ███    ███ ███   ███   ███ 
███ ▄█▄ ███   ███    ███   ███    ███        ███    ███ ███   ███ ███    ███ ███   ███   ███ 
 ▀███▀███▀    ██████████ ▄█████████▀         ██████████  ▀█   █▀  ████████▀   ▀█   ███   █▀  \n\n""" + bcolors.ENDC)

try:
	sys.argv[1]
except IndexError:
	print(bcolors.WARNING + "\nUsage: python3 xss-detector.py <url_to_test> (Ex: python3 xss-detector.py http://example.fr/ all)\n" + bcolors.ENDC)
	exit()

try:
	sys.argv[2]
	if sys.argv[2] == "all":
		all = 1
except IndexError:
	all = 0

cookie = input(bcolors.OKCYAN + "\nEnter cookies like this: {'PHPSESSID':'1841ed304c0911ed9609c', 'lang':'fr'} (press ENTER for nothing): " + bcolors.ENDC)
try:
	cookie
	cookie = ast.literal_eval(cookie)
except SyntaxError:
	cookie = {}

useragent = input(bcolors.OKCYAN + "\nEnter your custom User-Agent (press ENTER for default): " + bcolors.ENDC)
try:
	useragent
except SyntaxError:
	useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"


url = sys.argv[1]
path = sys.argv[1]
separator = "?"
separator2 = "/"
ok = 0
forbidden = []
o = []
m = 0
d=[]

if str(url[-1]) == "/":
	url = url.rsplit(separator2, 1)[0]
	path = url


try:
	test = requests.get(url, timeout=10, cookies=cookie, verify=False, headers = { "User-Agent": useragent})
except:
	print(bcolors.FAIL + "\nFailed to establish connection with ", url + bcolors.ENDC)
	exit()

print(bcolors.BOLD + bcolors.OKCYAN + "\nSearching misconf :" + bcolors.ENDC)
misconf = ["/robots.txt", "/server-status", "/.git", "/git", "/.gitignore", "/.htpasswd", "/.htaccess", "/phpmyadmin", "/adminer.php", "/index.php~", "/index.php.old", "/README.md", "/.env", "/TODO.md", "/LICENCE.txt", "/LICENCE", "/htaccess.txt", "/phpinfo.php", "/.ssh", "/install", "/install.php", "/LICENSE", "/LICENSE.txt", "/server-info"]
for x in misconf:
	t1 = requests.get(url + x, timeout=10, cookies=cookie, verify=False, headers = {"User-Agent": useragent})
	if t1.status_code == 200:
		print(bcolors.OKGREEN + "[MISCONF] " + bcolors.ENDC + bcolors.OKCYAN + x + " was found" + bcolors.ENDC)
		m = 1
if m == 0:
	print(bcolors.FAIL + "\nNo misconf find ", url + bcolors.ENDC)


print(bcolors.BOLD + bcolors.OKCYAN + "\nURL found:" + bcolors.ENDC)

def discover(url):
	try:
		resp = requests.get(url, timeout=10, cookies=cookie, verify=False, headers = { "User-Agent": useragent})
		content = resp.text

		for line in content.split():
			for word in line.split():
				try:
					if all != 1 and ("@" in word or "mailto" in word or ".html" in word or ".7z" in word or "#" in word or ".png" in word or ".jpg" in word or ".svg" in word or ".jpeg" in word or ".ico" in word or ".css" in word or ".js" in word or ".zip" in word or ".pdf" in word or ".txt" in word or ".gif" in word or ".JPEG" in word or ".PNG" in word or ".JPG" in word):
						pass
					else:
						if 'href="' in word:
							try:
								new_url = re.search('href="(.*)"', word).group(1)
							except AttributeError:
								new_url = re.search('href="(.*)"', word)
							new_url = new_url.split(separator, 1)[0]
							if 'http' in new_url:
								pass
							else:
								new_url = path + "/" + new_url
							if new_url not in o:
								o.append(new_url)
								print(bcolors.WARNING + "find: " + new_url.replace('//', '/') + bcolors.ENDC)
						if "href='" in word:
							try:
								new_url = re.search("href='(.*)'", word).group(1)
							except AttributeError:
								new_url = re.search("href='(.*)'", word)
							new_url = new_url.split(separator, 1)[0]
							if 'http' in new_url:
								pass
							else:
								new_url = path + "/" + new_url
							if new_url not in o:
								o.append(new_url)
								print(bcolors.WARNING + "find: " + new_url.replace('//', '/') + bcolors.ENDC)
						if "src='" in word:
							try:
								new_url = re.search("src='(.*)'", word).group(1)
							except AttributeError:
								new_url = re.search("src='(.*)'", word)
							new_url = new_url.split(separator, 1)[0]
							if 'http' in new_url:
								pass
							else:
								new_url = path + "/" + new_url
							if new_url not in o:
								o.append(new_url)
								print(bcolors.WARNING + "find: " + new_url.replace('//', '/') + bcolors.ENDC)
						if 'src="' in word:
							try:
								new_url = re.search('src="(.*)"', word).group(1)
							except AttributeError:
								new_url = re.search('src="(.*)"', word)
							new_url = new_url.split(separator, 1)[0]
							if 'http' in new_url:
								pass
							else:
								new_url = path + "/" + new_url
							if new_url not in o:
								o.append(new_url)
								print(bcolors.WARNING + "find: " + new_url.replace('//', '/') + bcolors.ENDC)
						if "action='" in word:
							try:
								new_url = re.search("action='(.*)'", word).group(1)
							except AttributeError:
								new_url = re.search("action='(.*)'", word)
							new_url = new_url.split(separator, 1)[0]
							if 'http' in new_url:
								pass
							else:
								new_url = path + "/" + new_url
							if new_url not in o:
								o.append(new_url)
								print(bcolors.WARNING + "find: " + new_url.replace('//', '/') + bcolors.ENDC)
						if 'action="' in word:
							try:
								new_url = re.search('action="(.*)"', word).group(1)
							except AttributeError:
								new_url = re.search('action="(.*)"', word)
							new_url = new_url.split(separator, 1)[0]
							if 'http' in new_url:
								pass
							else:
								new_url = path + "/" + new_url
							if new_url not in o:
								o.append(new_url)
								print(bcolors.WARNING + "find: " + new_url.replace('//', '/') + bcolors.ENDC)
						if "iframe='" in word:
							try:
								new_url = re.search("iframe='(.*)'", word).group(1)
							except AttributeError:
								new_url = re.search("iframe='(.*)'", word)
							new_url = new_url.split(separator, 1)[0]
							if 'http' in new_url:
								pass
							else:
								new_url = path + "/" + new_url
							if new_url not in o:
								o.append(new_url)
								print(bcolors.WARNING + "find: " + new_url.replace('//', '/') + bcolors.ENDC)
						if 'iframe="' in word:
							try:
								new_url = re.search('iframe="(.*)"', word).group(1)
							except AttributeError:
								new_url = re.search('iframe="(.*)"', word)
							new_url = new_url.split(separator, 1)[0]
							if 'http' in new_url:
								pass
							else:
								new_url = path + "/" + new_url
							if new_url not in o:
								o.append(new_url)
								print(bcolors.WARNING + "find: " + new_url.replace('//', '/') + bcolors.ENDC)

				except TypeError:
					pass
	except requests.exceptions.ConnectTimeout:
		pass


discover(url)

y=0
while y < len(o):
	print(bcolors.OKCYAN + "Searching URL on :", o[y].replace('//', '/') + bcolors.ENDC)
	discover(o[y])
	y = y + 1

if len(o) != 0:
	print(bcolors.OKCYAN + "\n----------------------------------------\n" + bcolors.ENDC)
	print(bcolors.BOLD + bcolors.OKCYAN + "All URL found on :", path + bcolors.ENDC)
	y=0
	while y < len(o):
		print(o[y].replace('//', '/'))
		y = y + 1
else:
	print(bcolors.FAIL + "\nNo URL founds" + bcolors.ENDC)

if len(o) != 0:
	print(bcolors.OKCYAN + "\n----------------------------------------\n" + bcolors.ENDC)
	testcode = input(bcolors.BOLD + bcolors.OKCYAN + "Do you want to test each status-code ? [Y/n]: " + bcolors.ENDC)

try:
	if testcode == "y" or testcode == "Y" or testcode == "":
		for x in o:
			code = requests.get(url, timeout=10, cookies=cookie, verify=False, headers = {"User-Agent": useragent})
			if code.status_code == 200:
				code = (bcolors.OKGREEN + "[200] " + bcolors.ENDC)
			elif code.status_code == 403:
				code = (bcolors.FAIL + "[403] " + bcolors.ENDC)
				forbidden.append(x)
			else:
				code = (bcolors.WARNING + "[" + str(code.status_code) + "] " + bcolors.ENDC)
			print(code + bcolors.OKCYAN +  x.replace('//', '/') + bcolors.ENDC)
except:
	pass



if len(forbidden) != 0:
	print(bcolors.OKCYAN + "\n----------------------------------------\n" + bcolors.ENDC)
	bypass = input(bcolors.BOLD + bcolors.OKCYAN + "Do you want to test bypass each 403 page ? [Y/n]: " + bcolors.ENDC)
else:
	bypass = 0
if bypass == "y" or bypass == "Y" or bypass == "":
	print(bcolors.BOLD + bcolors.OKCYAN + "All 403 Bypass found:", path + bcolors.ENDC)
	for x in forbidden:
		urll = x.rsplit(separator2, 1)[1]
		arg = x.rsplit(separator2, 1)[0]

		payloads = ["/","/*","/%2f/","/./","./.","/*/","?","??","&","#","%","%20","%09","/..;/","../","..%2f","..;/",".././","..%00/","..%0d","..%5c","..%ff/","%2e%2e%2f",".%2e/","%3f","%26","%23",".json"]

		for payload in payloads:
			try:
				req = requests.get(urll + "/" + payloads[payload] + argg, allow_redirects=False , verify = False , timeout = 5, cookies=cookie, headers = {"User-Agent": useragent})
				print(urll + "/" + payloads[payload] + argg + ' : ' + str(req.status_code))

			except Exception:
				pass


		r1 = requests.get(x, headers={"X-Original-URL":path, "User-Agent": useragent} , allow_redirects=False , verify=False , timeout=5, cookies=cookie)
		if r1.status_code == 200:
			print(bcolors.OKGREEN + "[200] " + bcolors.ENDC + bcolors.OKCYAN + x.replace('//', '/') + bcolors.ENDC + ' : ' +"(X-Original-URL: "+ urll + ')')
			ok = 1

		r2 = requests.get(x, headers={"X-Custom-IP-Authorization" : "127.0.0.1", "User-Agent": useragent} , allow_redirects=False , verify=False , timeout=5, cookies=cookie)
		if r2.status_code == 200:
			print(bcolors.OKGREEN + "[200] " + bcolors.ENDC + bcolors.OKCYAN + x.replace('//', '/') + bcolors.ENDC + ' : ' + "(X-Custom-IP-Authorization: 127.0.0.1" + ')')
			ok = 1

		r3 = requests.get(x, headers={"X-Forwarded-For": "http://127.0.0.1", "User-Agent": useragent} , allow_redirects=False , verify=False , timeout=5, cookies=cookie)
		if r3.status_code == 200:
			print(bcolors.OKGREEN + "[200] " + bcolors.ENDC + bcolors.OKCYAN + x.replace('//', '/') + bcolors.ENDC + ' : ' + "(X-Forwarded-For: http://127.0.0.1" + ')')
			ok = 1

		r4 = requests.get(x, headers={"X-Forwarded-For": "127.0.0.1:80", "User-Agent": useragent} , allow_redirects=False , verify=False , timeout=5, cookies=cookie)
		if r4.status_code == 200:
			print(bcolors.OKGREEN + "[200] " + bcolors.ENDC + bcolors.OKCYAN + x.replace('//', '/') + bcolors.ENDC + ' : ' + "(X-Forwarded-For: 127.0.0.1:80" + ')')
			ok = 1

		r5 = requests.get(url, headers={"X-rewrite-url": arg, "User-Agent": useragent} , allow_redirects=False , verify=False , timeout=5, cookies=cookie)
		if r5.status_code == 200:
			print(bcolors.OKGREEN + "[200] " + bcolors.ENDC + bcolors.OKCYAN + x.replace('//', '/') + bcolors.ENDC + ' : ' + "(X-rewrite-url: {}".format(arg) + ')')
			ok = 1

		r6 = requests.get(x, headers={'X-Forwarded-Host':'127.0.0.1', "User-Agent": useragent} , allow_redirects=False , verify=False , timeout=5, cookies=cookie)
		if r6.status_code == 200:
			print(bcolors.OKGREEN + "[200] " + bcolors.ENDC + bcolors.OKCYAN + x.replace('//', '/') + bcolors.ENDC + ' : ' + "X-Forwarded-Host:127.0.0.1" + ')')
			ok = 1

		r7 = requests.get(x, headers={'X-Host':'127.0.0.1', "User-Agent": useragent} , allow_redirects=False , verify=False , timeout=5, cookies=cookie)
		if r7.status_code == 200:
			print(bcolors.OKGREEN + "[200] " + bcolors.ENDC + bcolors.OKCYAN + x.replace('//', '/') + bcolors.ENDC + ' : ' + "X-Host:127.0.0.1" + ')')
			ok = 1

		r8 = requests.get(x, headers={'X-Remote-IP':'127.0.0.1', "User-Agent": useragent} , allow_redirects=False , verify=False , timeout=5, cookies=cookie)
		if r8.status_code == 200:
			print(bcolors.OKGREEN + "[200] " + bcolors.ENDC + bcolors.OKCYAN + x.replace('//', '/') + bcolors.ENDC + ' : ' + "X-Remote-IP:127.0.0.1" + ')')
			ok = 1

		r9 = requests.get(x, headers={'X-Originating-IP':'127.0.0.1', "User-Agent": useragent} , allow_redirects=False , verify=False , timeout=5, cookies=cookie)
		if r9.status_code == 200:
			print(bcolors.OKGREEN + "[200] " + bcolors.ENDC + bcolors.OKCYAN + x.replace('//', '/') + bcolors.ENDC + ' : ' + "X-Originating-IP:127.0.0.1" + ")")
			ok = 1

		r10 = requests.get(x, allow_redirects=False, verify=False, timeout=5, cookies=cookie, headers = { "User-Agent": useragent})
		if r10.status_code == 200:
			print(bcolors.OKGREEN + "[200] " + bcolors.ENDC + bcolors.OKCYAN + x.replace('//', '/') + bcolors.ENDC +  ' : ' + 'Using GET')
			ok = 1

		r11 = requests.post(x, allow_redirects=False, verify=False, timeout=5, cookies=cookie, headers = { "User-Agent": useragent})
		if r11.status_code == 200:		
			print(bcolors.OKGREEN + "[200] " + bcolors.ENDC + bcolors.OKCYAN + x.replace('//', '/') + bcolors.ENDC + ' : ' + 'Using POST')
			ok = 1

		r12 = requests.head(x, allow_redirects=False, verify=False, timeout=5, cookies=cookie, headers = { "User-Agent": useragent})
		if r12.status_code == 200:
			print(bcolors.OKGREEN + "[200] " + bcolors.ENDC + bcolors.OKCYAN + x.replace('//', '/') + bcolors.ENDC + ' : ' + 'Using HEAD')
			ok = 1

		r13 = requests.put(x, allow_redirects=False, verify=False, timeout=5, cookies=cookie, headers = { "User-Agent": useragent})
		if r13.status_code == 200:
			print(bcolors.OKGREEN + "[200] " + bcolors.ENDC + bcolors.OKCYAN + x.replace('//', '/') + bcolors.ENDC + ' : ' + 'Using PUT')
			ok = 1

		r14 = requests.delete(x, allow_redirects=False, verify=False, timeout=5, cookies=cookie, headers = { "User-Agent": useragent})
		if r14.status_code == 200:
			print(bcolors.OKGREEN + "[200] " + bcolors.ENDC + bcolors.OKCYAN + x.replace('//', '/') + bcolors.ENDC + ' : ' +'Using DELETE')
			ok = 1

		r15 = requests.patch(x, allow_redirects=False, verify=False, timeout=5, cookies=cookie, headers = { "User-Agent": useragent})
		if r15.status_code == 200:
			print(bcolors.OKGREEN + "[200] " + bcolors.ENDC + bcolors.OKCYAN + x.replace('//', '/') + bcolors.ENDC + ' : ' + 'Using PATCH')
			ok = 1

	if ok != 1:
		print(bcolors.FAIL + "\nAll Bypass Failed" + bcolors.ENDC)
