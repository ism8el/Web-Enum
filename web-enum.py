#!/usr/bin/python3

import requests
import re
import sys

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

try:
	sys.argv[1]
except IndexError:
	print(bcolors.WARNING + "\nUsage: python3 xss-detector.py <url_to_test> (Ex: python3 xss-detector.py http://example.fr/)\n" + bcolors.ENDC)
	exit()

url = sys.argv[1]
path = sys.argv[1]

o = []

print(bcolors.OKCYAN + "URL found:" + bcolors.ENDC)


def discover(url):
	try:
		resp = requests.get(url, timeout=10, headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"})
		content = resp.text

		for line in content.split():
			for word in line.split():
				try:
					if "@" in word or "mailto" in word or ".html" in word or ".7z" in word or "#" in word or ".png" in word or ".jpg" in word or ".svg" in word or ".jpeg" in word or ".ico" in word or ".css" in word or ".js" in word or ".zip" in word or ".pdf" in word or ".txt" in word or ".gif" in word or ".JPEG" in word or ".PNG" in word or ".JPG" in word:
						pass
					else:
						if 'href="' in word:
							try:
								new_url = re.search('href="(.*)"', word).group(1)
							except AttributeError:
								new_url = re.search('href="(.*)"', word)
							if 'http' in new_url:
								pass
							else:
								new_url = path + new_url
							if new_url in o:
								pass
							else:
								o.append(new_url)
								print(bcolors.WARNING + "find: " + new_url + bcolors.ENDC)
						if "href='" in word:
							try:
								new_url = re.search("href='(.*)'", word).group(1)
							except AttributeError:
								new_url = re.search("href='(.*)'", word)
							if 'http' in new_url:
								pass
							else:
								new_url = path + new_url
							if new_url in o:
								pass
							else:
								o.append(new_url)
								print(bcolors.WARNING + "find: " + new_url + bcolors.ENDC)
						if "src='" in word:
							try:
								new_url = re.search("src='(.*)'", word).group(1)
							except AttributeError:
								new_url = re.search("src='(.*)'", word)
							if 'http' in new_url:
								pass
							else:
								new_url = path + new_url
							if new_url in o:
								pass
							else:
								o.append(new_url)
								print(bcolors.WARNING + "find: " + new_url + bcolors.ENDC)
						if 'src="' in word:
							try:
								new_url = re.search('src="(.*)"', word).group(1)
							except AttributeError:
								new_url = re.search('src="(.*)"', word)
							if 'http' in new_url:
								pass
							else:
								new_url = path + new_url
							if new_url in o:
								pass
							else:
								o.append(new_url)
								print(bcolors.WARNING + "find: " + new_url + bcolors.ENDC)
						if "action='" in word:
							try:
								new_url = re.search("action='(.*)'", word).group(1)
							except AttributeError:
								new_url = re.search("action='(.*)'", word)
							if 'http' in new_url:
								pass
							else:
								new_url = path + new_url
							if new_url in o:
								pass
							else:
								o.append(new_url)
								print(bcolors.WARNING + "find: " + new_url + bcolors.ENDC)
						if 'action="' in word:
							try:
								new_url = re.search('action="(.*)"', word).group(1)
							except AttributeError:
								new_url = re.search('action="(.*)"', word)
							if 'http' in new_url:
								pass
							else:
								new_url = path + new_url
							if new_url in o:
								pass
							else:
								o.append(new_url)
								print(bcolors.WARNING + "find: " + new_url + bcolors.ENDC)
						if "iframe='" in word:
							try:
								new_url = re.search("iframe='(.*)'", word).group(1)
							except AttributeError:
								new_url = re.search("iframe='(.*)'", word)
							if 'http' in new_url:
								pass
							else:
								new_url = path + new_url
							if new_url in o:
								pass
							else:
								o.append(new_url)
								print(bcolors.WARNING + "find: " + new_url + bcolors.ENDC)
						if 'iframe="' in word:
							try:
								new_url = re.search('iframe="(.*)"', word).group(1)
							except AttributeError:
								new_url = re.search('iframe="(.*)"', word)
							if 'http' in new_url:
								pass
							else:
								new_url = path + new_url
							if new_url in o:
								pass
							else:
								o.append(new_url)
								print(bcolors.WARNING + "find: " + new_url + bcolors.ENDC)

				except TypeError:
					pass
	except requests.exceptions.ConnectTimeout:
		pass


discover(url)

y=0
while y < len(o):
	print(bcolors.OKCYAN + "URL found on :", o[y] + bcolors.ENDC)
	discover(o[y])
	y = y + 1

