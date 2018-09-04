#!/usr/bin/env python
#-*- coding: utf-8 -*-
import requests,re
from bs4 import BeautifulSoup

class Lyrics():
	"""
	Class containing every lyrics info
	"""
	def __init__(self,artist,text,title,writers=None,album=None,url=None,added_by=None,corrected_by=None):
		self._artist = artist
		self._title = title
		self._text = text
		self._album = album
		self._url = url
		self._writers = writers
		self._added_by = added_by
		self._corrected_by = corrected_by

	def __iter__(self):
		"""
		Just a generator that makes the object iterable
		"""
		yield "artist",self._artist
		yield "title",self._title
		yield "text",self._text
		yield "album",self._album
		yield "url",self._url
		yield "writers",self._writers
		yield "added_by",self._added_by
		yield "corrected_by",self._corrected_by

	def lyrics_dict(self):
		"""
		Params: None

		Returns: A dict containing every object information
		"""
		return dict(self.__iter__())

class AzLyricsParser():
	"""
	Class responsible for the parsing of
	the lyrics information
	"""
	def __init__(self):
		self._url = ""
		self._lyrics = Lyrics(None,None,None)

	def _query(self):
		"""	
		Type: Protected
	
		Makes a request to the lyrics page, and pass
		the bs object containing the page source
        to the _parse function
		"""

		headers = {"Host":"www.azlyrics.com",
		"Connection":"keep-alive",
		"Referer":"https://www.azlyrics.com/w/west.html",
		"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
		"Upgrade-Insecure-Requests": "1",
		}

		response = requests.get(self._url,headers=headers)
		content = response.content
		page = BeautifulSoup(content,"html.parser")
		self._parse(page)

	def _parse_credits(self,item):
		"""
		Type: Protected

		Params: Item (Bs object)

		Returns: Dict with credits ( Dict)
	
		This method gets the credits from
		a slice of the lyrics page
		just made to keep _parse method cleaner
		"""
		try:
			added_by = item.find("small").text
			added_by = re.findall("Thanks to (.*?) ",added_by)
		except:
			added_by = None
		try:
			tmp_corrected_by = item.findAll("small").pop(0)
			corrected_by = []
			for correction in tmp_corrected_by:
				res = (re.findall("Thanks to (.*?) ",correction))
				corrected_by.extend(res.split(","))
		except:
			corrected_by = None
		return {"added_by":added_by,"corrected_by":corrected_by}

	def _parse(self,page):	
		"""
		Type: Protected

		Params: Page Contet (Bs Object)
	
		This method scrapes every information
		it finds about the given url's lyrics
		and builds the Lyrics object
		"""
		lyrics = page.find("div",attrs={"class":"col-xs-12 col-lg-8 text-center"})
		title = lyrics.findAll("b")[1].text
		if title.startswith('"') and title.endswith('"'):
			title = title[1:-1]
		text = lyrics.find("div",attrs={"class":None}).text
		try:
			album = lyrics.find("div",attrs={"class":"panel album-panel noprint"}).text.strip("\n")
		except:
			album = None
		try:
			credits = self._parse_credits(lyrics.findAll("div",attrs={"class":"smt"})[1])
		except:
			credits = None
		try:
			writers = lyrics.findAll("div",attrs={"class":"smt"})[2].text.strip("\n").replace("Writer(s):","").split(",")
		except:
			writers = None
		artist = lyrics.find("div",attrs={"class":"lyricsh"}).text.replace(" Lyrics","").strip("\n")
		
		self._lyrics = Lyrics(artist,text,title,writers,album,self._url,credits["added_by"],credits["corrected_by"])

	def lyrics(self,url):
		"""
		Type: Public

		Params: Lyrics Url (String)
	
		Calls _query method and just 
		returns the Lyrics object after
		processing.
		"""
		self._url = url
		self._query()
		return self._lyrics
