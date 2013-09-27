#!/usr/bin/python

# using: https://github.com/MarioVilas/google

from google import search
import urllib.request
import webbrowser
import os, os.path
import platform
import sys

cache_dir = "cache/" # default

lolicon_search = []

common_finds = ['wikipedia', 'yahoo', 'urbandictionary', 'facebook']
common_sites = ['gelbooru']

# common_finds => sites without lolicon content
# common_sites => sites with lolicon content

class Cache(object):
	"""docstring for Cache"""

	def __init__(self):
		super(Cache, self).__init__()
		
		# Check path - existance of a file
		if not os.path.exists("cache") == True:
			os.mkdir("cache")

		# handling filesystem
		if 'Linux' in platform.platform():
			sys.path.append('cache/')
			cache_dir = "cache/"
		if 'Windows' in platform.platform():
			sys.path.append('cache\\')
			cache_dir = "cache\\"
			os.path.abspath(cache_dir)

def filter_search(search_list=[],file_name="lolicon.url"):
	file_name = cache_dir + file_name # adds path to cache folder

	# Check path - existance of a file
	if os.path.exists(file_name):
		f = open(file_name, "r+")
	else:
		f = open(file_name, "wt")

	for url in search('lolicon loli pictures', stop=128):
		for x in range(0,len(common_finds)-1):
			if common_finds[x] in url:
				url = ""
			# checks common finds without lolicon content

		f_url = url + "\n" 			# newline added - f=formated
		f.write(f_url) 				# saves url to file
		search_list.append(url) 	# add a url to search list

#execute
Cache_init = Cache()
filter_search(lolicon_search)
