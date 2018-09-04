#!/usr/bin/env python
#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

# https://stackoverflow.com/a/17388505
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

class AzLyricsSearch():
	"""
	Class responsible for the research of a 
	specific song/artist/album on AzLyrics.com
	"""
	def __init__(self):
		self.__limit = 5
		self.__offset = 1

		self._search_query = ""
		self._lastresults = []
		self._base_url = "https://search.azlyrics.com/"
		self._search_url = self._base_url+"search.php?q="

	def _build_req_url(self):
		"""
		Type: Protected
	
		Builds the request url
		"""
		return self._search_url + self._search_query + "&w=songs&p="+str(self.__offset)

	def _query(self):

		"""
		Type: Protected
	
		Makes a request to the azlyrics search
		page with the query and passes
		the result page content to _parse()
		"""

		headers = {"Host":"search.azlyrics.com",
		"Referer":"https://search.azlyrics.com/search.php?q="+self._search_query,
		"Connection":"keep-alive",
		"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
		"Upgrade-Insecure-Requests": "1",
		}
		response = requests.get(self._build_req_url(),headers=headers)
		content = response.content
		if "Try to compose less restrictive search query or check spelling." in response.text:
			#print("Too restrictive search")
			return []
		page = BeautifulSoup(content,"html.parser")
		self._parse(page)

	def _parse(self,page):	

		"""
		Type: Protected
	
		Scrapes information from the given page aka
		Song title, Song artist, and the lyrics link
		then build a dict containing those infos and
		append it to the results list
		"""

		if self._lastresults:
			self._lastresults = []
		songs_table = page.find("table",attrs={"class" : "table table-condensed"})
		songs = songs_table.findAll("tr",limit = self.__limit)
		if songs[0].find("td",attrs={"class":None}):
			self.__limit +=1
			songs = songs_table.findAll("tr",limit = self.__limit)
			songs.pop(0)
		
		for song in songs:
			song = song.find("td",attrs={"class":"text-left visitedlyr"})
			title = song.findAll("b")[0].text
			artist = song.findAll("b")[1].text
			lyrics_link = song.find("a")['href']
			lyrics = {"artist":artist,"title":title,"url":lyrics_link}
			self._lastresults.append(lyrics)

	def _reliable_results(self, query):
		"""
		Type: Protected

		Analyze the results and if atleast one matches,
		or its highly similar to the query then leave the
		results unchanged, otherwise delete them
		"""
		# check if at least one result fits the query at least at the 60%
		for result in self._lastresults:
			titleonly = result["title"]
			titleandartist = result["title"] + " "+result["artist"]
			artistandtitle = result["artist"] + " "+result["title"]
			if similar(titleonly, query) >= 0.6:
				return
			if similar(titleandartist, query) >= 0.6:
				return
			if similar(artistandtitle, query) >= 0.6:
				return
				
		# no valid results found, setting em to none
		self._lastresults = None

	def search(self,query,limit=5,offset=1,checkreliability=True):

		"""
		Type: Public
	
		Parasm:	Query text (String)
				Limit of results (Integer)
				Offset for pagination (Integer)

		Set a couple of attributes and
		calls _query method, than return the list
		containing the results
		"""

		self.__limit = limit
		self.__offset = offset
		self._search_query=query
		self._query()
		
		# check the reliability of the results if parameter is true
		if checkreliability:
		    self._reliable_results(query)
		
		return self._lastresults
