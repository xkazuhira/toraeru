#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""
	*booru general file.
	For now, there's working Gelbooru downloader for loli content,
	but soon I'll add danbooru, etc.
"""

import spam
import os
import datetime
import urllib.request
import http.cookiejar
import xml.etree.ElementTree as eltree
import json

global jsonAPI_GET_link

#loli_spam.execute_spam()
cache_dir = "cache/"

class Gelbooru(object):
	"""docstring for Gelbooru"""
	
	def __init__(self, url="http://gelbooru.com/"):
		# gets gelbooru homepage by default
		super(Gelbooru, self).__init__() 
		self.url = url

		gelbooru_loli = urllib.request.urlopen(url,timeout=5)
		read_gel_loli = gelbooru_loli.read()

		# save to gel.html file
		name_gel_loli = "gel.html"
		file_gel_loli = open(cache_dir+name_gel_loli,"wb")
		file_gel_loli.write(read_gel_loli)
	
	def gel_rssatom(url="http://gelbooru.com/index.php?page=atom", 
					by_tag_loli = False,limit = 100,download = True):
		"""gel_rssatom:

		by_tag_loli: 
			If you want to get feed for tag 'loli', you need to switch 
			by_tag_loli to True.
		limit: 
			limit is variable that stores maximum number of loli entries. 
			maximum number of entries that can be loaded is 100 (limited 
			by gelbooru API). When I was testing it, there was some problem
			with loading less than 5-10 urls.
		"""

		def filetype_check(cond_i, cond_d, *ftype):
			# cond_i - include file types
			if cond_i == True:
				pass
			# cond_d - exclude file types
			elif cond_d == True:
				pass

		if by_tag_loli == True:
			url = "http://gelbooru.com/index.php?page=dapi&s=post&q=index&limit={0}&tags=loli".format(str(limit))

		# gets gelbooru atom rss feed	
		gelbooru_atom = urllib.request.urlopen(url,timeout=5)
		read_gel_atom = gelbooru_atom.read()

		# save to atom.xml file
		if by_tag_loli == True:
			name_gel_atom = "atom_loli.xml"
		else: name_gel_atom = "atom.xml"
		file_gel_atom = open(cache_dir+name_gel_atom,"wb")
		file_gel_atom.write(read_gel_atom)

		# XML parsing 
		tree = eltree.parse(cache_dir+name_gel_atom)
		root = tree.getroot()

		# gets urls to images from post form
		for imgurl in root.iter('post'):
			url = imgurl.attrib.get('file_url')
			print(url)

			# gets picture file name
			f_url = url.replace(url[0:37],"")

			if download == True and os.path.exists(cache_dir+f_url) == False:
				# if file is already downloaded, it will skip it 
				urllib.request.urlretrieve(url,cache_dir+f_url)
				print(f_url)

class Danbooru(object):
	"""docstring for Danbooru"""
	def __init__(self, url="http://gelbooru.com/"):
		super(Danbooru, self).__init__()
		self.url = url

	def dan_jsonGET(url="http://gelbooru.com/",tag="loli",limit=100):
		# sends request to json API on danbooru and saves in variable 'json_r'
		json_g = urllib.request.urlopen(url+"posts.json?limit={0}?search[tags]={1}".format(str(limit), tag))
		json_r = json_g.read()

		# opens file following new filename format, and writes json data to it
		file_dan = open(cache_dir+"danbooru-"+date+"-T-"+str(hour)+"-"+str(minute)+"-"+str(second)+".json", "wb")	
		file_dan.write(json_r) 		

		"""Filename new format: 
		example: danbooru-2013-10-08-T-19-11-12.json
			1st place: Object name
			2nd place: Date in iso format
			3rd place: (starting with "-T-") Time: hour - minute - second
		"""

class FourChan(object):
	"""docstring for FourChan"""

	def __init__(self, board, pagenumber):
		super(FourChan, self).__init__()
		
		self.board = board
		self.pagenumber = pagenumber

		global board

		jsonAPI_address = "https://api.4chan.org/{0}/{1}.json".format(board, pagenumber)

		FourChan.chan_jsonGET(jsonAPI_address)

	def chan_jsonGET(url = "", download = True):

		chan_json = urllib.request.urlopen(url,timeout=5)
		r_chan_json = chan_json.read()

		f_chan_json = open(cache_dir+"4chan-"+spam.get_time()+".json", "wb")
		f_chan_json.write(r_chan_json)

		#f_chan_json_indent = open(cache_dir+"4chan-"+spam.get_time()+"-i.json", "wb")
		#d_chan_json_indent = json.dumps(r_chan_json, sort_keys=True, indent=2)
		#f_chan_json_indent.write(d_chan_json_indent)

		#json.loads(r_chan_json)

		# Trying to iter by force
		fchansrc = "images.4chan.org/{0}/src/".format(board)
		img_tim = [] # Lists of image tim 
		img_ext = [] # and file type


		while True:
			i = 0
			for tim in r_chan_json.iter("tim"):
				img_tim.append(img_tim)
		
			for ext in r_chan_json.iter("ext"):
				img_ext.append(img_ext)	
		
			for i in range(len(img_tim)):
				img_a = str(img_tim[i])+'.'+img_ext[i]
				img_fchansrc = fchansrc + img_a
				i += 1

		if download == True and os.path.exists(cache_dir+img_a) == False:
			# if file is already downloaded, it will skip it 
			urllib.request.urlretrieve(img_fchansrc,cache_dir+img_a)
			print(img_a)

def exhentai_try():
	# I need to came up with other idea
	# problem is with deleting cookies
	# -> getting rid of sadpanda stuff

	exhentai_home = urllib.request.urlopen("http://exhentai.org/",timeout=5)
	cj = http.cookiejar.CookieJar.clear(exhentai_home) # clears cookies of exhentai_site
	exhentai_site = urllib.request.urlopen("http://exhentai.org/g/456745/626c55332f/",cj,timeout=5)
	read_ex = exhentai_site.read()

	file_1 = open(cache_dir+"site.html","wb")
	file_1.write(read_ex)

def execute_gel(take_limit=100):
	# auto get a page, and put into "gel.html" file
	Gelbooru("http://gelbooru.com/index.php?page=post&s=list&tags=loli")
	maigah = Gelbooru.gel_rssatom(by_tag_loli=True,limit=take_limit)

def execute_dan(take_limit=100):
	# calls dan_jsonGET -> saving 100 entries with tag "loli"
	# to file following format in Danbooru init()
	omgomg = Danbooru.dan_jsonGET(tag="loli",limit=take_limit)

def execute_fchan():
	getget = FourChan('g','0')