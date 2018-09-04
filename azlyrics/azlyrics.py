#!/usr/bin/env python
#-*- coding: utf-8 -*-
from .objects.search import AzLyricsSearch
from .objects.lyrics import AzLyricsParser

class AzLyrics():
    """
    Simple interface to the end user
    """
    def __init__(self):
        self.azsearch = AzLyricsSearch()
        self.azlyricsparser = AzLyricsParser()

    def search(self,query,limit=5,offset=1):
        """
        Params: Query to search for (String)
                        Limit of results (Integer)
                        Offset for pagination (Integer)
        Returns: List of dictionaries containing every found lyrics

        This method scrapes every lyrics results
        with the given settings and returns dictionaries
        like:
                {
                "artist":artist,
                "title":title,
                "url":lyrics_link
                }
        """
        return self.azsearch.search(query)

    def lyrics(self,url):
        """
        Params: Url to get lyrics from (String)

        Returns: A Lyrics Object

        This method scrapes every information
        it finds about the given url's lyrics
        and returns you the lyrics object
        """
        return self.azlyricsparser.lyrics(url)
